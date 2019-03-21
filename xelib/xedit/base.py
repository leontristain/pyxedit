from contextlib import contextmanager

from xelib.xelib import Xelib


class XEditError(Exception):
    pass


class XEditAttribute:
    '''
    A descriptor class that can be used to quickly declare any sub-field of
    a record as an xedit object property. This encapsulates the logic for
    getting and setting a value at a subpath from the object.
    '''
    def __init__(self, path, enum=None, read_only=False, create=True):
        self.path = path
        self.enum = enum
        self.read_only = read_only
        self.create = create

    def __get__(self, obj, type=None):
        value = obj.get_value(path=self.path)
        if self.enum:
            return self.enum(value)
        return value

    def __set__(self, obj, value):
        if self.read_only:
            raise XEditError(f'Cannot set read-only attribute to {value}')
        if self.enum:
            value = value.value
        return obj.set_value(value, path=self.path, create_node=self.create)


class XEditBase:
    SIGNATURE = None
    Games = Xelib.Games
    ElementTypes = Xelib.ElementTypes
    DefTypes = Xelib.DefTypes
    SmashTypes = Xelib.SmashTypes
    ValueTypes = Xelib.ValueTypes

    # initializer
    def __init__(self, xelib, handle, handle_group):
        '''
        Initializer
        '''
        # each XEditBase-derived object wraps an xedit-lib handle
        self.handle = handle

        # we keep a reference to the handle group (from the xelib object)
        # containing the handle, in order to keep tabs on whether the handle
        # is still valid. The Xelib object is responsible for depopulating
        # the group as handles are released; if the group has been emptied,
        # we should be able to detect that here
        self._handle_group = handle_group

        # we keep a reference to the overarching xelib object; this is the
        # gateway to the xelib API that lets us do just about everything.
        self._xelib = xelib

    # xelib-related methods
    @property
    def xelib(self):
        '''
        A property for gating the access of _xelib attribute with a check to
        see whether the handle associated with this object has already been
        released. Since all functionality within this class ultimately comes
        down to a xelib library call with this attribute; an invalid handle
        effectively renders the class unusable.

        @return: self._xelib attribute, but only if handle is still valid
                 (i.e. still exists in the handle group it's supposed to be in)
        '''
        if self.handle and self.handle not in self._handle_group:
            raise XEditError(f'Accessing XEdit object of handle {self.handle} '
                             f'which has already been released from the '
                             f'xelib session')
        return self._xelib

    def xelib_run(self, method, *args, **kwargs):
        '''
        Helper that invokes a xelib method, passing into the method the object's
        handle as the first parameter. There are many xelib methods like this,
        which makes this helper very useful.

        @param method: name of the method to invoke on xelib
        @param *args, **kwargs: any positional or keyword arguments to pass to
                                the method, _other_ than the first positional
                                argument, which is expected to be `self.handle`
        '''
        return getattr(self.xelib, method)(self.handle, *args, **kwargs)

    # dunderbar methods, implement native object functionalities
    def __eq__(self, other):
        '''
        Implements equality behavior (`==` operator)

        Two xedit objects are equal if xelib.element_equals on the two handles
        return true.
        '''
        return self.xelib_run('element_equals', other.handle)

    def __getitem__(self, path):
        '''
        Implements indexing behavior (`[]` operator)

        Indexing should be the same thing as a strict version of the `.get`
        method. This mirrors python dictionary functionality.
        '''
        return self.get(path, ex=True)

    def __iter__(self):
        '''
        Implements iteration behavior (`for item in <obj>`)

        Iterating over an object should produce each of the child objects
        next-level down, by objectifying the handles returned with a
        `xelib.get_elements` call.

        Handles should be yielded one by one via an iterator within a handle
        management context, with only the yielded handles promoted to parent
        scope, such that any handles not yielded before the scope exits (e.g.
        via a `break` by the caller) are automatically released.
        '''
        with self.manage_handles():
            for handle in self.xelib_run('get_elements'):
                obj = self.objectify(handle)
                obj.promote()
                yield obj

    @contextmanager
    def manage_handles(self):
        '''
        Forwards the .manage_handles context manager available on xelib. This
        can be used to create sub-contexts for handle management, where
        handles created within the context, if not promoted to parent scope,
        will be released on exiting the context.
        '''
        with self.xelib.manage_handles():
            yield self

    def promote(self):
        '''
        Promote the handle associated with the current object to the parent
        handle management scope. If this is invoked at the top scope, it should
        harmlessly do nothing.
        '''
        parent_handles = self.xelib.promote_handle(self.handle)
        if parent_handles:
            self._handle_group = parent_handles

    # basic type properties, these should be safely accessible and return
    # a falsey value if inapplicable
    @property
    def element_type(self):
        '''
        Returns the element type
        '''
        return self.xelib_run('element_type', ex=False)

    @property
    def def_type(self):
        '''
        Returns the def type
        '''
        return self.xelib_run('def_type', ex=False)

    @property
    def smash_type(self):
        '''
        Returns the smash type
        '''
        return self.xelib_run('smash_type', ex=False)

    @property
    def value_type(self):
        '''
        Returns the value type
        '''
        return self.xelib_run('value_type', ex=False)

    def objectify(self, handle):
        '''
        Given a handle, create an appropriate object to wrap around the handle.

        During initialization, we run a staticmethod stored on the class to
        explicitly import all possible object classes. We then choose the
        object class to use depending on the def type, the value type, and
        the signature of the handle. Any xedit object will be able to call
        this method to create objects of any appropriate xedit subclass to
        match for a given handle.

        @param handle: a xelib handle
        @return: an object of some class derived from this base class, that
                 wraps around the handle
        '''
        # first create a generic object out of it so we can easily inspect it
        generic_obj = XEditGenericObject.from_xedit_object(handle, self)

        # if object is a plugin, use the XEditPlugin class
        if generic_obj.element_type == self.ElementTypes.etFile:
            return XEditPlugin.from_xedit_object(handle, self)

        # if object is a top-level group, use the generic class as-is, since
        # it's going to have a signature that is same as the records in the
        # group, but won't have anything of substance
        if generic_obj.element_type == self.ElementTypes.etGroupRecord:
            return generic_obj

        # if object is an array or subrecord array, use the collection class
        if generic_obj.element_type in (self.ElementTypes.etArray,
                                        self.ElementTypes.etSubRecordArray):
            return XEditCollection.from_xedit_object(handle, self)

        # otherwise, see if we can find a subclass of XEditBase
        # corresponding to the signature; if so, use the subclass to make
        # the object, otherwise just use the generic object
        if generic_obj.signature:
            for subclass in XEditBase.get_imported_subclasses():
                if subclass.SIGNATURE == generic_obj.signature:
                    return subclass.from_xedit_object(handle, self)

        return generic_obj

    def get(self, path, default=None, ex=False):
        '''
        Return a descendent xedit object to the current object with a given
        path.

        This function can be likened to a dictionary's `.get` method. A default
        can be provided which defaults to None, which also makes the method
        harmless to call. We also support an `ex` switch that raises exception
        on error, so that we can reuse the same code for __getitem__.

        @param path: the path to access
        @param default: the default value to return of something cannot be
                        accessed at the given path
        @param ex: if set to True, failure to access at given path will raise
                   an exception
        @return: the xedit object at the path from the current object, or
                 the default value if failed to access
        '''
        handle = self.xelib_run('get_element', path=path, ex=ex)
        if handle:
            return self.objectify(handle)
        elif ex:
            raise XEditError(f'No object can be obtained at path {path} from '
                             f'{self.long_path}')
        else:
            return default

    def add(self, path):
        '''
        Adds an element at the given path and return it as an xedit object

        @param path: the path to add element at
        @return: xedit object of the element added
        '''
        with self.manage_handles():
            if self.get(path):
                raise XEditError(f'Cannot add object at path {path}; an object '
                                 f'already exists there')
        handle = self.xelib_run('add_element', path=path)
        if handle:
            return self.objectify(handle)

    def get_or_add(self, path):
        '''
        Return object at given path, object will be created if it does not
        exist.

        @param path: the path to get or create element at
        @return: the gotten or created element as an xedit object
        '''
        return self.get(path) or self.add(path)

    def delete(self, path=''):
        '''
        Delete the element at the given path. If the given path is an empty
        string, the element associated with this object itself will be deleted.

        @param path: path of element to delete
        '''
        self.xelib_run('remove_element', path=path)

    # other basic properties; these should all be safely retrievable where a
    # falsey value is returned if inapplicable
    @property
    def name(self):
        '''
        Returns the element name
        '''
        return self.xelib_run('name', ex=False)

    @property
    def long_name(self):
        '''
        Returns the element long name
        '''
        return self.xelib_run('long_name', ex=False)

    @property
    def display_name(self):
        '''
        Returns the element display name
        '''
        return self.xelib_run('display_name', ex=False)

    @property
    def path(self):
        '''
        Returns the element path
        '''
        return self.xelib_run('path', ex=False)

    @property
    def long_path(self):
        '''
        Returns the element long path
        '''
        return self.xelib_run('long_path', ex=False)

    @property
    def local_path(self):
        '''
        Returns the element local path
        '''
        return self.xelib_run('local_path', ex=False)

    @property
    def signature(self):
        '''
        Returns the element signature
        '''
        return self.xelib_run('signature', ex=False)

    @property
    def signature_name(self):
        '''
        Returns any known human-readable name for the element's signature
        '''
        signature = self.signature
        return (self.xelib.name_from_signature(signature, ex=False)
                if signature else '')

    @property
    def num_children(self):
        '''
        Returns the number of direct child elements this element has
        '''
        return self.xelib_run('element_count')

    @classmethod
    def get_imported_subclasses(cls):
        '''
        Recursively produces the subclasses that are derived from this class;
        a subclass would only get yielded here if it has already been imported
        into the global python namespace.
        '''
        for subclass in cls.__subclasses__():
            yield from subclass.get_imported_subclasses()
            yield subclass

    @classmethod
    def from_xedit_object(cls, handle, xedit_obj):
        '''
        Create an object of this class from another xedit object. This is the
        primary method in which new xedit objects are instantiated, which means
        all objects are ultimately instantiated from the root xedit object the
        user would use to enter the xedit context.

        When new objects are created "off" of the existing object, the new
        object inherit the xelib attribute pointing to the current overarching
        xelib context. When each new object is created, it also saves the
        xelib context's current handle group onto itself, in order to track its
        own handle's validity against.

        @param handle: the handle to create the new obj with
        @param xedit_obj: the xedit object to create the new object "off" of;
                          a handle to the xelib context can be "inherited" from
                          it.
        '''
        if not handle or handle not in xedit_obj._xelib._current_handles:
            raise XEditError(f'Attempting to create XEdit object from invalid '
                             f'handle {handle} with respect to source object '
                             f'{xedit_obj}; handle not managed by the current '
                             f'manage_handles context of the object')
        return cls(xedit_obj.xelib, handle, xedit_obj._xelib._current_handles)

    @staticmethod
    def import_all_object_classes():
        '''
        A staticmethod that simply imports all object classes into the python
        namespace. When xelib handles are objectified into xedit objects,
        one of the below object classes might be used, and thus must be
        imported onto the namespace prior.
        '''
        from xelib.xedit.object_classes.ARMA import XEditArmature  # NOQA
        from xelib.xedit.object_classes.ARMO import XEditArmor  # NOQA
        from xelib.xedit.object_classes.HDPT import XEditHeadPart  # NOQA
        from xelib.xedit.object_classes.NPC_ import XEditNPC  # NOQA
        from xelib.xedit.object_classes.TXST import XEditTextureSet  # NOQA


class XEditPlugin(XEditBase):
    @property
    def author(self):
        return self.xelib_run('get_file_author')

    @author.setter
    def author(self, value):
        return self.xelib_run('set_file_author', value)

    @property
    def description(self):
        return self.xelib_run('get_description')

    @description.setter
    def description(self, value):
        return self.xelib_run('set_description', value)

    @property
    def is_esm(self):
        return self.xelib_run('get_is_esm')

    @is_esm.setter
    def is_esm(self, value):
        return self.xelib_run('set_is_esm', value)

    @property
    def next_object(self):
        return self.objectify(self.xelib_run('get_next_object_id'))

    @next_object.setter
    def next_object(self, value):
        return self.xelib_run('set_next_object_id', value.handle)

    def save(self):
        return self.xelib_run('save_file')

    def save_as(self, file_path):
        return self.xelib_run('save_file', file_path=file_path)


class XEditGenericObject(XEditBase):
    @property
    def value(self):
        def_type = self.def_type
        if def_type is None or def_type in (
                self.DefTypes.dtRecord,
                self.DefTypes.dtSubRecord,
                self.DefTypes.dtSubRecordArray,
                self.DefTypes.dtSubRecordStruct,
                self.DefTypes.dtSubRecordUnion,
                self.DefTypes.dtFlag,
                self.DefTypes.dtArray,
                self.DefTypes.dtStruct,
                self.DefTypes.dtUnion,
                self.DefTypes.dtEmpty,
                self.DefTypes.dtStructChapter):
            return
        elif def_type in (self.DefTypes.dtString,
                          self.DefTypes.dtLString):
            return self.xelib.get_value(self.handle)
        elif def_type == self.DefTypes.dtInteger:
            if self.value_type == self.ValueTypes.vtReference:
                referenced = self.xelib.get_links_to(self.handle, ex=False)
                return self.objectify(referenced) if referenced else None
            else:
                return self.xelib.get_int_value(self.handle)
        elif def_type == self.DefTypes.dtFloat:
            return self.xelib.get_float_value(self.handle)
        else:
            raise NotImplementedError(f'Just encountered {def_type}, which is '
                                      f'not yet supported as a gettable value; '
                                      f'we should check it out and add it')

    @value.setter
    def value(self, value):
        def_type = self.def_type
        if def_type is None or def_type in (
                self.DefTypes.dtRecord,
                self.DefTypes.dtSubRecord,
                self.DefTypes.dtSubRecordArray,
                self.DefTypes.dtSubRecordStruct,
                self.DefTypes.dtSubRecordUnion,
                self.DefTypes.dtFlag,
                self.DefTypes.dtArray,
                self.DefTypes.dtStruct,
                self.DefTypes.dtUnion,
                self.DefTypes.dtEmpty,
                self.DefTypes.dtStructChapter):
            return
        elif def_type in (self.DefTypes.dtString,
                          self.DefTypes.dtLString):
            return self.xelib.set_value(self.handle, str(value))
        elif def_type == self.DefTypes.dtInteger:
            if self.value_type == self.ValueTypes.vtReference:
                if isinstance(value, XEditBase):
                    return self.xelib.set_links_to(self.handle, value.handle)
                else:
                    raise XEditError(f'Setting a value for an object of type '
                                     f'{self.ValueTypes.vtReference} requires '
                                     f'another xedit object')
            else:
                return self.xelib.set_int_value(self.handle, int(value))
        elif def_type == self.DefTypes.dtFloat:
            return self.xelib.set_float_value(self.handle, float(value))
        else:
            raise NotImplementedError(f'Just encountered {def_type}, which is '
                                      f'not yet supported as a settable value; '
                                      f'we should check it out and add it')

    def get_value(self, path=''):
        with self.manage_handles():
            obj = self.get(path) if path else self
            if obj:
                return obj.value

    def set_value(self, value, path='', create_node=True):
        with self.manage_handles():
            if value is None:
                if not path or self.get(path=path):
                    self.delete(path=path)
            else:
                if path and not self.get(path=path):
                    if create_node:
                        self.add(path=path)
                    else:
                        raise XEditError(
                            f'Cannot set value at {path} from {self.long_path}; '
                            f'node does not exist; you can specify '
                            f'create_node=True to create one; just make sure '
                            f'you have not misspelled anything')
                (self[path] if path else self).value = value

    data_size = XEditAttribute('Record Header\\Data Size', read_only=True)
    form_version = XEditAttribute('Record Header\\Form Version', read_only=True)
    editor_id = XEditAttribute('EDID', read_only=True)

    @property
    def form_id(self):
        return self.xelib_run('get_int_value', path='Record Header\\FormID')


class XEditCollection(XEditGenericObject):
    def __len__(self):
        return self.num_children

    def __getitem__(self, index):
        # implements `parts[2]`
        len_ = len(self)

        # support negative indexing
        if index < 0:
            index += len_

        # raise IndexError on out of range resolved index
        if not 0 <= index < len_:
            raise IndexError(f'XEditCollection has {len_} items; resolved '
                             f'index {index} is out of range')

        # in range, get and objectify the array element
        return self.objectify(
                   self.xelib.get_element(self.handle, path=f'[{index}]'))

    def __iter__(self):
        # implements `for part in parts`
        for index in range(len(self)):
            yield self[index]

    def index(self, item):
        with self.manage_handles():
            for i, my_item in enumerate(self):
                if item == my_item:
                    return i
        raise ValueError(f'item equivalent to {item} is not in the list')

    def add_item_with(self, value, subpath=''):
        return self.objectify(
                   self.xelib.add_array_item(self.handle, '', subpath, value))

    def has_item_with(self, value, subpath=''):
        return self.xelib.has_array_item(
                   self.handle, '', subpath, value, ex=False)

    def find_item_with(self, value, subpath=''):
        item_handle = self.xelib.get_array_item(
                          self.handle, '', subpath, value, ex=False)
        if item_handle:
            return self.objectify(item_handle)

    def remove_item_with(self, value, subpath=''):
        return self.xelib.remove_array_item(self.handle, '', subpath, value)

    def move_item(self, sub_item, to_index):
        return self.xelib.move_array_item(sub_item.handle, to_index)

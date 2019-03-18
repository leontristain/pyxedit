from contextlib import contextmanager

from xelib.xelib import Xelib


class XEditError(Exception):
    pass


class XEditAttribute:
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

    def __init__(self, xelib, handle, handle_group):
        self.handle = handle
        self._handle_group = handle_group
        self._xelib = xelib

    @property
    def xelib(self):
        if self.handle and self.handle not in self._handle_group:
            raise XEditError(f'Accessing XEdit object of handle {self.handle} '
                             f'which has already been released from the '
                             f'xelib session')
        return self._xelib

    def xelib_run(self, method, *args, **kwargs):
        '''
        Invokes a xelib method with the current handle
        '''
        return getattr(self.xelib, method)(self.handle, *args, **kwargs)

    def __eq__(self, other):
        return self.xelib_run('element_equals', other.handle)

    def __getitem__(self, path):
        return self.get(path, ex=True)

    def __iter__(self):
        for handle in self.xelib_run('get_elements'):
            yield self.objectify(handle)

    @contextmanager
    def manage_handles(self):
        with self.xelib.manage_handles():
            yield self

    @property
    def element_type(self):
        return self.xelib_run('element_type', ex=False)

    @property
    def def_type(self):
        return self.xelib_run('def_type', ex=False)

    @property
    def smash_type(self):
        return self.xelib_run('smash_type', ex=False)

    @property
    def value_type(self):
        return self.xelib_run('value_type', ex=False)

    def objectify(self, handle):
        # first create a generic object out of it so we can inspect it
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
        handle = self.xelib_run('get_element', path=path, ex=ex)
        if handle:
            return self.objectify(handle)
        elif ex:
            raise XEditError(f'No object can be obtained at path {path} from '
                             f'{self.long_path}')
        else:
            return default

    def add(self, path):
        with self.manage_handles():
            if self.get(path):
                raise XEditError(f'Cannot add object at path {path}; an object '
                                 f'already exists there')
        handle = self.xelib_run('add_element', path=path)
        if handle:
            return self.objectify(handle)

    def get_or_add(self, path):
        return self.get(path) or self.add(path)

    def delete(self, path=''):
        self.xelib_run('remove_element', path=path)

    @property
    def name(self):
        return self.xelib_run('name', ex=False)

    @property
    def long_name(self):
        return self.xelib_run('long_name', ex=False)

    @property
    def display_name(self):
        return self.xelib_run('display_name', ex=False)

    @property
    def path(self):
        return self.xelib_run('path', ex=False)

    @property
    def long_path(self):
        return self.xelib_run('long_path', ex=False)

    @property
    def local_path(self):
        return self.xelib_run('local_path', ex=False)

    @property
    def signature(self):
        return self.xelib_run('signature', ex=False)

    @property
    def signature_name(self):
        signature = self.signature
        return (self.xelib.name_from_signature(signature, ex=False)
                if signature else '')

    @property
    def num_children(self):
        return self.xelib_run('element_count')

    @classmethod
    def get_imported_subclasses(cls):
        for subclass in cls.__subclasses__():
            yield from subclass.get_imported_subclasses()
            yield subclass

    @classmethod
    def from_xedit_object(cls, handle, xedit_obj):
        if not handle or handle not in xedit_obj._xelib._current_handles:
            raise XEditError(f'Attempting to create XEdit object from invalid '
                             f'handle {handle} with respect to source object '
                             f'{xedit_obj}; handle not managed by the current '
                             f'manage_handles context of the object')
        return cls(xedit_obj.xelib, handle, xedit_obj._xelib._current_handles)

    @staticmethod
    def import_all_object_classes():
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

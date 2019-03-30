from contextlib import contextmanager
from pathlib import Path

from xedit.xelib import Xelib
from xedit.xedit.misc import XEditError, XEditTypes


class XEditBase:
    SIGNATURE = None
    Games = Xelib.Games
    Types = XEditTypes
    ElementTypes = Xelib.ElementTypes
    DefTypes = Xelib.DefTypes
    SmashTypes = Xelib.SmashTypes
    ValueTypes = Xelib.ValueTypes

    # initializer
    def __init__(self, xelib, handle, handle_group, auto_release=True):
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

        # if this is set to True (and it should be set to True most of the
        # time), then it enables the handle to be automatically released
        # whenever this object goes out of scope.
        #
        # exceptions for when we may want to disable this behavior include
        # when we are creating another object to inherit a handle, in which
        # case the previous object need to set auto_release to False before
        # handing the handle over to the new object. This usually happens
        # when we want to switch to a different subclass of XEditBase to
        # start managing this handle
        self.auto_release = auto_release

    # finalizer
    def __del__(self):
        '''
        Finalizer. It should release the handle and remove the handle from
        any tracked handle groups (this is what Xelib.release_handle does).
        Respects an auto-release switch that can be used to disable it.
        '''
        if self.auto_release:
            self._xelib.release_handle(self.handle)

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

    @contextmanager
    def manage_handles(self):
        '''
        Forwards the .manage_handles context manager available on xelib. This
        can be used to create sub-contexts for handle management, where
        handles created within the context, if not promoted to parent scope,
        will be released on exiting the context.

        NOTE: usage of this is now deprecated since the handle management
              based on __del__ seems to be working very well
        '''
        with self.xelib.manage_handles():
            yield self

    def promote(self):
        '''
        Promote the handle associated with the current object to the parent
        handle management scope. If this is invoked at the top scope, it should
        harmlessly do nothing.
        '''
        if self.handle:
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

    @property
    def type(self):
        '''
        Resolve an XEditType value for this element based on the various
        other types.
        '''
        if self.def_type in (self.DefTypes.dtString,
                             self.DefTypes.dtLString,
                             self.DefTypes.dtLenString,
                             self.DefTypes.dtByteArray,
                             self.DefTypes.dtInteger,
                             self.DefTypes.dtIntegerFormater,
                             self.DefTypes.dtIntegerFormaterUnion,
                             self.DefTypes.dtFlag,
                             self.DefTypes.dtFloat):
            if (self.def_type == self.DefTypes.dtInteger and
                    self.value_type == self.ValueTypes.vtReference):
                return self.Types.Ref
            else:
                return self.Types.Value
        else:
            return self.Types.Container

    @property
    def is_modified(self):
        '''
        Returns whether element has been modified in the current session
        '''
        return self.xelib_run('get_is_modified')

    @property
    def is_removable(self):
        '''
        Returns whether element is removable
        '''
        return self.xelib_run('get_is_removable')

    @property
    def can_add(self):
        '''
        Returns whether elements can be added to this element
        '''
        return self.xelib_run('get_can_add')

    @property
    def is_sorted(self):
        '''
        Returns whether elements is a sorted array
        '''
        return self.xelib_run('is_sorted')

    @property
    def is_flags(self):
        '''
        Returns whether element is a flag element containing flags
        '''
        return self.xelib_run('is_flags')

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
        # import the following at runtime; they are only needed at method
        # runtime, and putting these imports at the top of this module would
        # result in circular imports
        from xedit.xedit.generic import XEditGenericObject
        from xedit.xedit.array import XEditArray
        from xedit.xedit.plugin import XEditPlugin

        # first create a generic object out of it so we can easily inspect it;
        # this object may not be the final produced object, so make sure it does
        # not enable auto-release until we're sure it is the final produced
        # object
        generic_obj = XEditGenericObject.from_xedit_object(
                                              handle, self, auto_release=False)

        # if object is a plugin, use the XEditPlugin class
        if generic_obj.element_type == self.ElementTypes.etFile:
            return XEditPlugin.from_xedit_object(handle, self)

        # if object is a top-level group, use the generic class as-is, since
        # it's going to have a signature that is same as the records in the
        # group, but won't have anything of substance
        if generic_obj.element_type == self.ElementTypes.etGroupRecord:
            generic_obj.auto_release = True
            return generic_obj

        # if object is an array or subrecord array, use the collection class
        if generic_obj.element_type in (self.ElementTypes.etArray,
                                        self.ElementTypes.etSubRecordArray):
            return XEditArray.from_xedit_object(handle, self)

        # otherwise, see if we can find a subclass of XEditBase
        # corresponding to the signature; if so, use the subclass to make
        # the object, otherwise just use the generic object
        if generic_obj.signature:
            for subclass in XEditBase.get_imported_subclasses():
                if subclass.SIGNATURE == generic_obj.signature:
                    return subclass.from_xedit_object(handle, self)

        generic_obj.auto_release = True
        return generic_obj

    def get(self, path, default=None, ex=False, absolute=False):
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
        @param absolute: if set to True, will query for the element from the
                         root, expecting the given path to be an absolute path
        @return: the xedit object at the path from the current object, or
                 the default value if failed to access
        '''
        if absolute:
            handle = self.xelib.get_element(0, path=path, ex=ex)
        else:
            handle = self.xelib_run('get_element', path=path, ex=ex)

        if handle:
            return self.objectify(handle)
        elif ex:
            if absolute:
                raise XEditError(f'No object can be obtained with absolute '
                                 f'path {path} from the root')
            else:
                raise XEditError(f'No object can be obtained at path {path} '
                                 f'from {self.long_path}')
        else:
            return default

    def add(self, path):
        '''
        Adds an element at the given path and return it as an xedit object

        @param path: the path to add element at
        @return: xedit object of the element added
        '''
        if self.get(path):
            raise XEditError(f'Cannot add object at path {path}; an object '
                                f'already exists there')
        handle = self.xelib_run('add_element', path=path)
        if handle:
            return self.objectify(handle)

    def has(self, path):
        '''
        Checks whether a sub-element exists at the given path
        @param path: the subpath to check for element existence at
        @return: boolean of whether something is there
        '''
        return bool(self.get(path))

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
        return self.xelib_run('element_count', ex=False)

    @property
    def children(self):
        '''
        Produces each of the child objects next-level down by objectifying the
        handles returned with a `xelib.get_elements` call.
        '''
        for handle in self.xelib_run('get_elements', ex=False):
            obj = self.objectify(handle)
            yield obj

    @property
    def descendants(self):
        if self.num_children:
            for child in self.children:
                yield child
                yield from child.descendants

    @property
    def parent(self):
        '''
        Produces an object of the element that contains this one.

        There doesn't seem to be a xelib method for this, so implementation
        is done by treating the `long_path` as a windows path object and
        running a global `.get` on the parent path. This might not be the
        best solution.
        '''
        if self.long_path:
            return self.get(str(Path(self.long_path).parent), absolute=True)

    @property
    def ls(self):
        '''
        Prints a list of children to stdout; this can be useful when browsing
        the xedit session. This isn't actually a property; instead it's meant
        to be similar to a shell `ls` command in a python interpreter.
        '''
        children = list(self.children)
        longest_name_length = max([len(child.name) for child in children])
        for child in self.children:
            print(f'{child.name.rjust(longest_name_length)}: {child}')

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
    def from_xedit_object(cls, handle, xedit_obj, auto_release=True):
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
        return cls(xedit_obj.xelib,
                   handle,
                   xedit_obj._xelib._current_handles,
                   auto_release=auto_release)

    @staticmethod
    def import_all_object_classes():
        '''
        A staticmethod that simply imports all object classes into the python
        namespace. When xelib handles are objectified into xedit objects,
        one of the below object classes might be used, and thus must be
        imported onto the namespace prior.
        '''
        from xedit.xedit.object_classes.ARMA import XEditArmature  # NOQA
        from xedit.xedit.object_classes.ARMO import XEditArmor  # NOQA
        from xedit.xedit.object_classes.HDPT import XEditHeadPart  # NOQA
        from xedit.xedit.object_classes.NPC_ import XEditNPC  # NOQA
        from xedit.xedit.object_classes.OBND import XEditObjectBounds # NOQA
        from xedit.xedit.object_classes.TXST import XEditTextureSet  # NOQA

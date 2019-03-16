from contextlib import contextmanager
from pathlib import Path


class XEditError(Exception):
    pass


class XEditBase:
    SIGNATURE = None

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

    def __getitem__(self, path):
        return self.get(path, ex=True)

    @contextmanager
    def manage_handles(self):
        with self.xelib.manage_handles():
            yield self

    def get(self, path, default=None, ex=False):
        handle = self.xelib.get_element(self.handle, path=path, ex=ex)

        # got a valid handle
        if handle:
            # first create a generic object out of it so we ca inspect it
            generic_obj = XEditGenericObject.from_xedit_object(handle, self)

            # if object is a plugin, use the XEditPlugin class
            if generic_obj.is_plugin:
                return XEditPlugin.from_xedit_object(handle, self)

            # if object is a top-level group, use the generic class as-is, since
            # it's going to have a signature that is same as the records in the
            # group, but won't have anything of substance
            if generic_obj.is_toplevel_group:
                return generic_obj

            # otherwise, see if we can find a subclass of XEditBase
            # corresponding to the signature; if so, use the subclass to make
            # the object, otherwise just use the generic object
            if generic_obj.signature:
                for subclass in XEditBase.get_imported_subclasses():
                    if subclass.SIGNATURE == generic_obj.signature:
                        return subclass.from_xedit_object(handle, self)
            return generic_obj

        # no valid handle, if ex is enabled, raise an exception; otherwise just
        # return the default
        if ex:
            raise XEditError(f'No object can be obtained at path {path} from '
                             f'{self.long_path}')
        return default

    def add(self, path):
        with self.manage_handles():
            if self.get(path):
                raise XEditError(f'Cannot add object at path {path}; an object '
                                 f'already exists there')
            self.xelib.add_element(self.handle, path=path)

    def delete(self, path=''):
        self.xelib.remove_element(self.handle, path=path)


    @property
    def name(self):
        return self.xelib.name(self.handle)

    @property
    def long_name(self):
        return self.xelib.long_name(self.handle)

    @property
    def display_name(self):
        return self.xelib.display_name(self.handle)

    @property
    def path(self):
        return self.xelib.path(self.handle)

    @property
    def long_path(self):
        return self.xelib.long_path(self.handle)

    @property
    def local_path(self):
        return self.xelib.local_path(self.handle)

    @property
    def is_plugin(self):
        return len(Path(self.long_path).parts) == 1

    @property
    def is_toplevel_group(self):
        return len(Path(self.long_path).parts) == 2

    @property
    def signature(self):
        return self.xelib.signature(self.handle, ex=False)

    @property
    def signature_name(self):
        signature = self.signature
        return self.xelib.name_from_signature(signature) if signature else None

    @classmethod
    def get_imported_subclasses(cls):
        for subclass in cls.__subclasses__():
            yield from subclass.get_imported_subclasses()
            yield subclass

    @classmethod
    def from_xedit_object(cls, handle, xedit_obj):
        if not handle or handle not in xedit_obj._xelib._current_handles:
            raise XEditError(f'Attempting to create XEdit object from invalid '
                             f'handle {handle}')
        return cls(xedit_obj.xelib, handle, xedit_obj._xelib._current_handles)

    @staticmethod
    def import_all_object_classes():
        from xelib.xedit.object_classes.NPC_ import XEditNPC  # NOQA
        from xelib.xedit.object_classes.TXST import XEditTextureSet  # NOQA


class XEditPlugin(XEditBase):
    @property
    def author(self):
        return self.xelib.get_file_author(self.handle)

    @author.setter
    def author(self, value):
        self.xelib.set_file_author(self.handle, value)

    @property
    def description(self):
        return self.xelib.get_description(self.handle)

    @description.setter
    def description(self, value):
        self.xelib.set_description(self.handle, value)

    @property
    def is_esm(self):
        return self.xelib.get_is_esm(self.handle)

    @is_esm.setter
    def is_esm(self, value):
        self.xelib.set_is_esm(self.handle, value)

    @property
    def next_object_id(self):
        return self.xelib.get_next_object_id(self.handle)

    @next_object_id.setter
    def next_object_id(self, value):
        self.xelib.set_next_object_id(self.handle, value)

    def save(self):
        return self.xelib.save_file(self.handle)

    def save_as(self, file_path):
        return self.xelib.save_file(self.handle, file_path=file_path)


class XEditGenericObject(XEditBase):
    def get_value(self, path='', type_=str, unsigned=False):
        if type_ == int:
            if unsigned:
                return self.xelib.get_uint_value(self.handle, path=path)
            else:
                return self.xelib.get_int_value(self.handle, path=path)
        elif type_ == float:
            return self.xelib.get_float_value(self.handle, path=path)
        elif type_ == str:
            return self.xelib.get_value(self.handle, path=path)
        else:
            raise XEditError(f'getting value of type {type_} is not supported')

    def set_value(self, value, path='', type_=str, unsigned=False):
        if type_ == int:
            if unsigned:
                return self.xelib.set_uint_value(self.handle, int(value), path=path)
            else:
                return self.xelib.set_int_value(self.handle, int(value), path=path)
        elif type_ == float:
            return self.xelib.set_float_value(self.handle, float(value), path=path)
        elif type_ == str:
            return self.xelib.set_value(self.handle, str(value), path=path)
        else:
            raise XEditError(f'setting value of type {type_} is not supported')

    @property
    def data_size(self):
        with self.manage_handles():
            return self['Record Header']['Data Size'].get_value(type_=int)

    @property
    def form_id(self):
        with self.manage_handles():
            return self['Record Header']['FormID'].get_value(
                                                      type_=int, unsigned=True)

    @property
    def form_version(self):
        with self.manage_handles():
            return self['Record Header']['Form Version'].get_value(type_=int)

    @property
    def editor_id(self):
        return self.xelib.editor_id(self.handle)

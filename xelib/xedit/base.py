from contextlib import contextmanager
from pathlib import Path

from xelib.xelib import Xelib


class XEditError(Exception):
    pass


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

    def __eq__(self, other):
        return self.xelib.element_equals(self.handle, other.handle)

    def __getitem__(self, path):
        return self.get(path, ex=True)

    @contextmanager
    def manage_handles(self):
        with self.xelib.manage_handles():
            yield self

    @property
    def element_type(self):
        return self.xelib.element_type(self.handle, ex=False)

    @property
    def def_type(self):
        return self.xelib.def_type(self.handle, ex=False)

    @property
    def smash_type(self):
        return self.xelib.smash_type(self.handle, ex=False)

    @property
    def value_type(self):
        return self.xelib.value_type(self.handle, ex=False)

    def objectify(self, handle):
        # first create a generic object out of it so we ca inspect it
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
        handle = self.xelib.get_element(self.handle, path=path, ex=ex)
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
                             f'handle {handle} with respect to source object '
                             f'{xedit_obj}; handle not managed by the current '
                             f'manage_handles context of the object')
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
        with self.manage_handles():
            if not path or self.get(path):
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
                    raise XEditError(f'getting value of type {type_} is not '
                                     f'supported')

    def set_value(self,
                  value,
                  path='',
                  type_=str,
                  unsigned=False,
                  create_node=False):
        # a helper function to create the node if it doesn't exist; gated by
        # the method's create_node parameter
        def create_node_if_not_exist():
            if path and not self.get(path):
                if create_node:
                    self.add(path=path)
                else:
                    raise XEditError(f'Cannot set value at {path} from '
                                     f'{self.long_path}; node does not exist; '
                                     f'you can specify create_node=True to '
                                     f'create one; just make sure you have not '
                                     f'misspelled anything')
        with self.manage_handles():
            if value is None:
                # a None given as a value means we should delete the node
                if not path or self.get(path=path):
                    self.delete(path=path)
            else:
                # otherwise, we set the value on the node; remember to run the
                # create_node_if_not_exist function only when we're about to
                # set the value
                if type_ == int:
                    if unsigned:
                        create_node_if_not_exist()
                        return self.xelib.set_uint_value(
                                   self.handle, int(value), path=path)
                    else:
                        create_node_if_not_exist()
                        return self.xelib.set_int_value(
                                   self.handle, int(value), path=path)
                elif type_ == float:
                    create_node_if_not_exist()
                    return self.xelib.set_float_value(
                               self.handle, float(value), path=path)
                elif type_ == str:
                    create_node_if_not_exist()
                    return self.xelib.set_value(
                               self.handle, str(value), path=path)
                else:
                    raise XEditError(f'setting value of type {type_} is not '
                                     f'supported')

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


class XEditCollection(XEditGenericObject):
    def __len__(self):
        # implements `len(parts)`
        return self.xelib.element_count(self.handle)

    def __getitem__(self, index):
        # implements `parts[2]`
        len_ = len(self)
        if index >= len_:
            raise IndexError(f'XEditCollection has only {len_} items; list '
                             f'index {index} is out of range')
        return self.objectify(
                   self.xelib.get_element(self.handle, path=f'[{index}]'))

    def __iter__(self):
        # implements `for part in parts`
        for index in range(len(self)):
            yield self[index]

    def add_item_with(self, value, subpath=''):
        return self.objectify(
                   self.xelib.add_array_item(self.handle, '', subpath, value))

    def has_item_with(self, value, subpath=''):
        return self.xelib.has_array_item(self.handle, '', subpath, value)

    def find_item_with(self, value, subpath=''):
        item_handle = self.xelib.get_array_item(
                          self.handle, '', subpath, value, ex=False)
        if item_handle:
            return self.objectify(item_handle)

    def remove_item_with(self, value, subpath=''):
        return self.xelib.remove_array_item(self.handle, '', subpath, value)

    def move_item(self, sub_item, to_index):
        return self.xelib.move_array_item(sub_item.handle, to_index)

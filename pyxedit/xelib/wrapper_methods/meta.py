from enum import Enum, unique

from pyxedit.xelib.wrapper_methods.base import WrapperMethodsBase


@unique
class SortBy(Enum):
    None_ = 0
    FormID = 1
    EditorID = 2
    Name = 3


class MetaMethods(WrapperMethodsBase):
    SortBy = SortBy

    def initialize(self):
        self.raw_api.InitXEdit()

    def finalize(self):
        self.raw_api.CloseXEdit()

    def get_global(self, key, ex=True):
        return self.get_string(
            lambda len_: self.raw_api.GetGlobal(key, len_),
            error_msg=f'GetGlobal failed',
            ex=ex)

    def get_globals(self, ex=True):
        return self.get_string(
            lambda len_: self.raw_api.GetGlobals(len_),
            error_msg=f'GetGlobals failed',
            ex=ex)

    def set_sort_mode(self, mode, reverse=False, ex=True):
        return self.verify_execution(
            self.raw_api.SetSortMode(mode.value, reverse),
            error_msg=f'Failed to set sort mode to {mode} '
                      f'{"ASC" if reverse else "DESC"}',
            ex=ex)

    def release(self, id_, ex=True):
        return self.verify_execution(
            self.raw_api.Release(id_),
            error_msg=f'Failed to release handle {id_}',
            ex=ex)

    def release_nodes(self, id_, ex=True):
        return self.verify_execution(
            self.raw_api.ReleaseNodes(id_),
            error_msg=f'Failed to release nodes {id_}',
            ex=ex)

    def switch(self, id_, id2, ex=True):
        return self.verify_execution(
            self.raw_api.Switch(id_, id2),
            error_msg=f'Failed to switch interface #{id_} and #{id2}',
            ex=ex)

    def get_duplicate_handles(self, id_, ex=True):
        return self.get_array(
            lambda len_: self.raw_api.GetDuplicateHandles(id_, len_),
            error_msg=f'Failed to get duplicate handles for {id_}',
            ex=ex)

    def clean_store(self, ex=True):
        return self.verify_execution(
            self.raw_api.CleanStore(),
            error_msg=f'Failed to clean interface store',
            ex=ex)

    def reset_store(self, ex=True):
        return self.verify_execution(
            self.raw_api.ResetStore(),
            error_msg=f'Failed to reset interface store',
            ex=ex)

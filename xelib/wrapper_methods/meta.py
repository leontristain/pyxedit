from enum import Enum, unique

from xelib.wrapper_methods.base import WrapperMethodsBase


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

    def get_global(self, key):
        return self.get_string(
            lambda len_: self.raw_api.GetGlobal(key, len_),
            error_msg=f'GetGlobal failed')

    def get_globals(self):
        return self.get_string(
            lambda len_: self.raw_api.GetGlobals(len_),
            error_msg=f'GetGlobals failed')

    def set_sort_mode(self, mode, reverse):
        return self.verify_execution(
            self.raw_api.SetSortMode(mode.value, reverse),
            error_msg=f'Failed to set sort mode to {mode} '
                      f'{"ASC" if reverse else "DESC"}')

    def release(self, id_):
        return self.verify_execution(
            self.raw_api.Release(id_),
            error_msg=f'Failed to release handle {id_}')

    def release_nodes(self, id_):
        return self.verify_execution(
            self.raw_api.ReleaseNodes(id_),
            error_msg=f'Failed to release nodes {id_}')

    def switch(self, id_, id2):
        return self.verify_execution(
            self.raw_api.Switch(id_, id2),
            error_msg=f'Failed to switch interface #{id_} and #{id2}')

    def get_duplicate_handles(self, id_):
        return self.get_array(
            lambda len_: self.raw_api.GetDuplicateHandles(id_, len_),
            error_msg=f'Failed to get duplicate handles for {id_}')

    def clean_store(self):
        return self.verify_execution(
            self.raw_api.CleanStore(),
            error_msg=f'Failed to clean interface store')

    def reset_store(self):
        return self.verify_execution(
            self.raw_api.ResetStore(),
            error_msg=f'Failed to reset interface store')

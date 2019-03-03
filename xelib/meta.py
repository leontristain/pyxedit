from enum import Enum, unique

from xelib.lib import raw_api
from xelib.helpers import validate, get_string, get_array


@unique
class SortBy(Enum):
    None_ = 0
    FormID = 1
    EditorID = 2
    Name = 3


def initialize(lib_path):
    raw_api.InitXEdit(lib_path)


def finalize():
    raw_api.CloseXEdit()


def get_global(key):
    return get_string(lambda len_: raw_api.GetGlobal(key, len_),
                      error_msg=f'GetGlobal failed')


def get_globals():
    return get_string(lambda len_: raw_api.GetGlobals(len_),
                      error_msg=f'GetGlobals failed')


def set_sort_mode(mode, reverse):
    validate(raw_api.SetSortMode(mode.value, reverse),
             f'Failed to set sort mode to {mode} '
             f'{"ASC" if reverse else "DESC"}')


def release(id_):
    validate(raw_api.Release(id_), f'Failed to release handle {id_}')


def release_nodes(id_):
    validate(raw_api.ReleaseNodes(id_), f'Failed to release nodes {id_}')


def switch(id_, id2):
    validate(raw_api.Switch(id_, id2),
             f'Failed to switch interface #{id_} and #{id2}')


def get_duplicate_handles(id_):
    return get_array(lambda len_: raw_api.GetDuplicateHandles(id_, len_),
                     error_msg=f'Failed to get duplicate handles for {id_}')


def clean_store():
    validate(raw_api.CleanStore(), f'Failed to clean interface store')


def reset_store():
    validate(raw_api.ResetStore(), f'Failed to reset interface store')


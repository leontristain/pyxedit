from enum import Enum, unique

from xelib.lib import raw_api
from xelib.helpers import get_string, get_array, verify_execution


@unique
class SortBy(Enum):
    None_ = 0
    FormID = 1
    EditorID = 2
    Name = 3


def initialize():
    raw_api.InitXEdit()


def finalize():
    raw_api.CloseXEdit()


def get_global(key):
    return get_string(
        lambda len_: raw_api.GetGlobal(key, len_),
        error_msg=f'GetGlobal failed')


def get_globals():
    return get_string(
        lambda len_: raw_api.GetGlobals(len_),
        error_msg=f'GetGlobals failed')


def set_sort_mode(mode, reverse):
    verify_execution(
        raw_api.SetSortMode(mode.value, reverse),
        error_msg=f'Failed to set sort mode to {mode} '
                  f'{"ASC" if reverse else "DESC"}')


def release(id_):
    verify_execution(
        raw_api.Release(id_),
        error_msg=f'Failed to release handle {id_}')


def release_nodes(id_):
    verify_execution(
        raw_api.ReleaseNodes(id_),
        error_msg=f'Failed to release nodes {id_}')


def switch(id_, id2):
    verify_execution(
        raw_api.Switch(id_, id2),
        error_msg=f'Failed to switch interface #{id_} and #{id2}')


def get_duplicate_handles(id_):
    return get_array(
        lambda len_: raw_api.GetDuplicateHandles(id_, len_),
        error_msg=f'Failed to get duplicate handles for {id_}')


def clean_store():
    verify_execution(
        raw_api.CleanStore(),
        error_msg=f'Failed to clean interface store')


def reset_store():
    verify_execution(
        raw_api.ResetStore(),
        error_msg=f'Failed to reset interface store')


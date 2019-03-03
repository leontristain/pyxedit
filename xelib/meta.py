from xelib.lib import raw_api
from xelib.helpers import validate


def initialize(lib_path):
    raise NotImplementedError


def finalize():
    raise NotImplementedError


def get_global(key):
    raise NotImplementedError


def get_globals():
    raise NotImplementedError


def set_sort_mode(mode, reverse):
    raise NotImplementedError


def release(id_):
    validate(raw_api.Release(id_), f'Failed to release handle {id_}')

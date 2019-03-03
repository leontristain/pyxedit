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


def release_nodes(id_):
    raise NotImplementedError


def switch(id_, id2):
    raise NotImplementedError


def get_duplicate_handles(id_):
    raise NotImplementedError


def clean_store():
    raise NotImplementedError


def reset_store():
    raise NotImplementedError


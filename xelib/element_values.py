from xelib.helpers import get_string, get_string_value
from xelib.lib import raw_api


def name(id_):
    return get_string_value(id_, 'Name')

def long_name(id_):
    return get_string_value(id_, 'LongName')

def display_name(id_):
    return get_string_value(id_, 'DisplayName')

# ToImplement: PlacementName

def path(id_):
    return get_string(
        lambda len_: raw_api.Path(id_, True, False, len_),
        error_msg=f'Path failed on {id_}')

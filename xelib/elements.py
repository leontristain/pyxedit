from xelib.lib import raw_api
from xelib.handles import handle_managed
from xelib.helpers import XelibError, get_array, get_string

# ================
# element value method wrappers
# ================

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

# ================
# elements handling methods
# ================

def has_element(id_, path=''):
    raise NotImplementedError

def get_element(id_, path=''):
    raise NotImplementedError

def get_element_ex(id_, path=''):
    raise NotImplementedError

def add_element(id_, path=''):
    raise NotImplementedError

def add_element_value(id_, path, value):
    raise NotImplementedError

def remove_element(id_, path=''):
    raise NotImplementedError

def remove_element_ex(id_, path=''):
    raise NotImplementedError

def set_element(id1, id2):
    raise NotImplementedError

@handle_managed
def get_elements(id_=0, path='', sort=False, filter=False):
    return get_array(
        lambda len_: raw_api.GetElements(id_, path, sort, filter, len_),
        error_msg=f'Failed to get child elements at '
                  f'{element_context(id_, path)}')

# ================
# Helpers
# ================
def safe_element_path(id_):
    '''
    Safely return a representative string of the given element path; protects
    from api errors (as this is typically used in output strings which may
    include error message strings)
    '''
    try:
        return path(id_)
    except XelibError:
        return str(id_)


def element_context(id_, path=None):
    if path:
        return f'{safe_element_path(id_)}, "{path}"'
    else:
        return safe_element_path(id_)


def get_string_value(id_, method, error_msg=''):
    '''
    Retrieve a string value from an element given via its id
    '''
    return get_string(lambda len_: method(id_, len_), error_msg=error_msg)
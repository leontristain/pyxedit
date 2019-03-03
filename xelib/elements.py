from xelib.lib import raw_api
from xelib.handles import handle_managed
from xelib.helpers import get_array, element_context

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

from xelib.lib import raw_api
from xelib.handles import handle_managed
from xelib.helpers import (XelibError,
                           get_array,
                           get_bool,
                           get_double,
                           get_dictionary,
                           get_handle,
                           get_integer,
                           get_string,
                           get_unsigned_integer,
                           validate)


# ================
# element value method wrappers
# ================


def name(id_):
    return get_string(
        lambda len_: raw_api.Name(id_, len_),
        error_msg=f'Name failed on {id_}')


def long_name(id_):
    return get_string(
        lambda len_: raw_api.LongName(id_, len_),
        error_msg=f'LongName failed on {id_}')


def display_name(id_):
    return get_string(
        lambda len_: raw_api.DisplayName(id_, len_),
        error_msg=f'DisplayName failed on {id_}')


def placement_name(id_):
    with get_links_to(id_, 'NAME') as rec:
        return rec > 0 and f'Places {name(rec)}'


def path(id_):
    return get_string(
        lambda len_: raw_api.Path(id_, True, False, len_),
        error_msg=f'Path failed on {id_}')


def long_path(id_):
    return get_string(
        lambda len_: raw_api.Path(id_, False, False, len_),
        error_msg=f'Path failed on {id_}')


def local_path(id_):
    return get_string(
        lambda len_: raw_api.Path(id_, False, True, len_),
        error_msg=f'Path failed on {id_}')


def signature(id_):
    return get_string(
        lambda len_: raw_api.Signature(id_, len_),
        error_msg=f'Signature failed on {id_}')


def sort_key(id_):
    return get_string(
        lambda len_: raw_api.SortKey(id_, len_),
        error_msg=f'SortKey failed on {id_}')


def get_value(id_, path=''):
    return get_string(
        lambda len_: raw_api.GetValue(id_, path, len_),
        error_msg=f'Failed to get element value at '
                  f'{element_context(id_, path)}')


def get_value_ex(id_, path=''):
    raise NotImplementedError(
        "purposely not supporting 'ex' methods until I figure out why they're"
        "even needed; they seem to be ones that throw exceptions, but why"
        "shouldn't we want everything to behave in the same way?")


def set_value(id_, value, path=''):
    validate(raw_api.SetValue(id_, path, value),
             f'Failed to set element value at {element_context(id_, path)}')


def get_int_value(id_, path=''):
    return get_integer(
        lambda res: raw_api.GetIntValue(id_, path, res),
        error_msg=f'Failed to get int value at {element_context(id_, path)}')


def get_int_value_ex(id_, path=''):
    raise NotImplementedError(
        "purposely not supporting 'ex' methods until I figure out why they're"
        "even needed; they seem to be ones that throw exceptions, but why"
        "shouldn't we want everything to behave in the same way?")


def set_int_value(id_, value, path=''):
    validate(raw_api.SetIntValue(id_, path, value),
             f'Failed to set int value at {element_context(id_, path)}')


def get_uint_value(id_, path=''):
    return get_unsigned_integer(
        lambda res: raw_api.GetUIntValue(id_, path, res),
        error_msg=f'Failed to get uint value at {element_context(id_, path)}')


def get_uint_value_ex(id_, path=''):
    raise NotImplementedError(
        "purposely not supporting 'ex' methods until I figure out why they're"
        "even needed; they seem to be ones that throw exceptions, but why"
        "shouldn't we want everything to behave in the same way?")


def set_uint_value(id_, value, path=''):
    validate(raw_api.SetUIntValue(id_, path, value),
             f'Failed to set uint value at {element_context(id_, path)}')


def get_float_value(id_, path=''):
    return get_double(
        lambda res: raw_api.GetFloatValue(id_, path, res),
        error_msg=f'Failed to get float value at {element_context(id_, path)}')


def get_float_value_ex(id_, path=''):
    raise NotImplementedError(
        "purposely not supporting 'ex' methods until I figure out why they're"
        "even needed; they seem to be ones that throw exceptions, but why"
        "shouldn't we want everything to behave in the same way?")


def set_float_value(id_, value, path=''):
    validate(raw_api.SetFloatValue(id_, path, value),
             f'Failed to set uint value at {element_context(id_, path)}')


def set_flag(id_, path, name, state):
    validate(raw_api.SetFlag(id_, path, name, state),
             f'Failed to set flag value at {flag_context(id_, path, name)} '
             f'to {state}')


def get_flag(id_, path, name):
    return get_bool(
        lambda res: raw_api.GetFlag(id_, path, name, res),
        error_msg=f'Failed to get flag value at: '
                  f'{flag_context(id_, path, name)}')


def get_enabled_flags(id_, path=''):
    return get_string(
        lambda len_: raw_api.GetEnabledFlags(id_, path, len_),
        error_msg=f'Failed to get enabled flags at: '
                  f'{element_context(id_, path)}').split(',')


def set_enabled_flags(id_, path, flags):
    validate(raw_api.SetEnabledFlags(id_, path, ','.join(flags)),
             f'Failed to set enabled flags at {element_context(id_, path)}')


def get_all_flags(id_, path=''):
    return get_string(
        lambda len_: raw_api.GetAllFlags(id_, path, len_),
        error_msg=f'Failed to get all flags at: {element_context(id_, path)}')


def get_enum_options(id_, path=''):
    return get_string(
        lambda len_: raw_api.GetEnumOptions(id_, path, len_),
        error_msg=f'Failed to get all enum options at '
                  f'{element_context(id_, path)}').split(',')


def signature_from_name(name):
    return get_string(
        lambda len_: raw_api.SignatureFromName(name, len_),
        error_msg=f'Failed to get signature from name: {name}')


def name_from_signature(sig):
    return get_string(
        lambda len_: raw_api.NameFromSignature(sig, len_),
        error_msg=f'Failed to get name from signature: {sig}')


def get_signature_name_map():
    return get_dictionary(
        lambda len_: raw_api.GetSignatureNameMap(len_),
        error_msg=f'Failed to get signature name map')


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


def get_def_names(id_):
    raise NotImplementedError


def get_add_list(id):
    raise NotImplementedError


@handle_managed
def get_links_to(id_, path=''):
    return get_handle(
        lambda res: raw_api.GetLinksTo(id_, path, res))


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


def flag_context(id_, path, name):
    return f'{safe_element_path(id_)}, "{path}\\{name}"'

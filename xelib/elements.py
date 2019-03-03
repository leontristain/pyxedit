from enum import Enum, unique

from xelib.lib import raw_api
from xelib.handles import handle_managed
from xelib.helpers import (XelibError,
                           get_array,
                           get_bool,
                           get_byte,
                           get_double,
                           get_dictionary,
                           get_handle,
                           get_integer,
                           get_string,
                           get_string_array,
                           get_unsigned_integer,
                           validate)


@unique
class ElementTypes(Enum):
    File = 'etFile'
    MainRecord = 'etMainRecord'
    GroupRecord = 'etGroupRecord'
    SubRecord = 'etSubRecord'
    SubRecordStruct = 'etSubRecordStruct'
    SubRecordArray = 'etSubRecordArray'
    SubRecordUnion = 'etSubRecordUnion'
    Array = 'etArray'
    Struct = 'etStruct'
    Value = 'etValue'
    Flag = 'etFlag'
    StringListTerminator = 'etStringListTerminator'
    Union = 'etUnion'
    StructChapter = 'etStructChapter'


@unique
class DefTypes(Enum):
    Record = 'dtRecord'
    SubRecord = 'dtSubRecord'
    SubRecordArray = 'dtSubRecordArray'
    SubRecordStruct = 'dtSubRecordStruct'
    SubRecordUnion = 'dtSubRecordUnion'
    String = 'dtString'
    LString = 'dtLString'
    LenString = 'dtLenString'
    ByteArray = 'dtByteArray'
    Integer = 'dtInteger'
    IntegerFormater = 'dtIntegerFormater'
    IntegerFormaterUnion = 'dtIntegerFormaterUnion'
    Flag = 'dtFlag'
    Float = 'dtFloat'
    Array = 'dtArray'
    Struct = 'dtStruct'
    Union = 'dtUnion'
    Empty = 'dtEmpty'
    StructChapter = 'dtStructChapter'


@unique
class SmashTypes(Enum):
    Unknown = 'stUnknown'
    Record = 'stRecord'
    String = 'stString'
    Integer = 'stInteger'
    Flag = 'stFlag'
    Float = 'stFloat'
    Struct = 'stStruct'
    UnsortedArray = 'stUnsortedArray'
    UnsortedStructArray = 'stUnsortedStructArray'
    SortedArray = 'stSortedArray'
    SortedStructArray = 'stSortedStructArray'
    ByteArray = 'stByteArray'
    Union = 'stUnion'


@unique
class ValueTypes(Enum):
    Unknown = 'vtUnknown'
    Bytes = 'vtBytes'
    Number = 'vtNumber'
    String = 'vtString'
    Text = 'vtText'
    Reference = 'vtReference'
    Flags = 'vtFlags'
    Enum = 'vtEnum'
    Color = 'vtColor'
    Array = 'vtArray'
    Struct = 'vtStruct'


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
    return get_bool(
        lambda res: raw_api.HasElement(id_, path, res),
        error_msg=f'Failed to check if element exists at '
                  f'{element_context(id, path)}')


@handle_managed
def get_element(id_, path=''):
    return get_handle(
        lambda res: raw_api.GetElement(id_, path, res),
        error_msg=f'Failed to get element at {element_context(id_, path)}')


def get_element_ex(id_, path=''):
    raise NotImplementedError(
        "purposely not supporting 'ex' methods until I figure out why they're"
        "even needed; they seem to be ones that throw exceptions, but why"
        "shouldn't we want everything to behave in the same way?")


@handle_managed
def add_element(id_, path=''):
    return get_handle(
        lambda res: raw_api.AddElement(id_, path, res),
        error_msg=f'Failed to create new element at '
                  f'{element_context(id_, path)}')


@handle_managed
def add_element_value(id_, path, value):
    return get_handle(
        lambda res: raw_api.AddElementValue(id_, path, value, res),
        error_msg=f'Failed to create new element at '
                  f'{element_context(id_, path)}, with value: {value}')


def remove_element(id_, path=''):
    validate(raw_api.RemoveElement(id_, path),
             f'Failed to remove element at {element_context(id_, path)}')


def remove_element_ex(id_, path=''):
    raise NotImplementedError(
        "purposely not supporting 'ex' methods until I figure out why they're"
        "even needed; they seem to be ones that throw exceptions, but why"
        "shouldn't we want everything to behave in the same way?")


def remove_element_or_parent(id_):
    validate(raw_api.RemoveElementOrParent(id_),
             f'Failed to remove element {element_context(id_)}')


def set_element(id1, id2):
    validate(raw_api.SetElement(id1, id2),
             f'Failed to remove element at {element_context(id2)} to '
             f'{element_context(id1)}')


@handle_managed
def get_elements(id_=0, path='', sort=False, filter=False):
    return get_array(
        lambda len_: raw_api.GetElements(id_, path, sort, filter, len_),
        error_msg=f'Failed to get child elements at '
                  f'{element_context(id_, path)}')


def get_def_names(id_):
    return get_string_array(
        lambda len_: raw_api.GetDefNames(id_, len_),
        error_msg=f'Failed to get def names for {element_context(id_)}')


def get_add_list(id_):
    return get_string_array(
        lambda len_: raw_api.GetAddList(id_, len_),
        error_msg=f'Failed to get add list for {element_context(id_)}')


@handle_managed
def get_links_to(id_, path=''):
    return get_handle(
        lambda res: raw_api.GetLinksTo(id_, path, res),
        error_msg=f'Failed to get reference at {element_context(id_, path)}')


def set_links_to(id_, id2, path=''):
    validate(raw_api.SetLinksTo(id_, path, id2),
             f'Failed to set reference at {element_context(id_, path)}')


def get_links_to_ex(id_, path=''):
    raise NotImplementedError(
        "purposely not supporting 'ex' methods until I figure out why they're"
        "even needed; they seem to be ones that throw exceptions, but why"
        "shouldn't we want everything to behave in the same way?")


@handle_managed
def get_container(id_):
    return get_handle(
        lambda res: raw_api.GetContainer(id_, res),
        error_msg=f'Failed to get container for {element_context(id_)}')


def get_container_ex(id_):
    raise NotImplementedError(
        "purposely not supporting 'ex' methods until I figure out why they're"
        "even needed; they seem to be ones that throw exceptions, but why"
        "shouldn't we want everything to behave in the same way?")


@handle_managed
def get_element_file(id_):
    return get_handle(
        lambda res: raw_api.GetElementFile(id_, res),
        error_msg=f'Failed to get element file for {element_context(id_)}')


@handle_managed
def get_element_group(id_):
    return get_handle(
        lambda res: raw_api.GetElementGroup(id_, res),
        error_msg=f'Failed to get element group for: {element_context(id_)}')


@handle_managed
def get_element_record(id_):
    return get_handle(
        lambda res: raw_api.GetElementRecord(id_, res),
        error_msg=f'Failed to get element record for: {element_context(id_)}')


def element_count(id_):
    return get_integer(
        lambda res: raw_api.ElementCount(id_, res),
        error_msg=f'Failed to get element count for {element_context(id_)}')


def element_equals(id_, id2):
    return get_bool(
        lambda res: raw_api.ElementEquals(id_, id2, res),
        error_msg=f'Failed to check element equality for '
                  f'{element_context(id_)} and {element_context(id2)}')


def element_matches(id_, path, value):
    return get_bool(
        lambda res: raw_api.ElementMatches(id_, path, value, res),
        error_msg=f'Failed to check element matches for '
                  f'{element_context(id_, path)},{value}')


def has_array_item(id_, path, subpath, value):
    return get_bool(
        lambda res: raw_api.HasArrayItem(id_, path, subpath, value, res),
        error_msg=f'Failed to check if array has item for '
                  f'{array_item_context(id_, path, subpath, value)}')


@handle_managed
def get_array_item(id_, path, subpath, value):
    return get_handle(
        lambda res: raw_api.GetArrayItem(id_, path, subpath, value, res),
        error_msg=f'Failed to get array item for '
                  f'{array_item_context(id_, path, subpath, value)}')


@handle_managed
def add_array_item(id_, path, subpath, value):
    return get_handle(
        lambda res: raw_api.AddArrayItem(id_, path, subpath, value, res),
        error_msg=f'Failed to add array item to '
                  f'{array_item_context(id_, path, subpath, value)}')


def remove_array_item(id_, path, subpath, value):
    validate(raw_api.RemoveArrayItem(id_, path, subpath, value),
             f'Failed to remove array item '
             f'{array_item_context(id_, path, subpath, value)}')


def move_array_item(id_, index):
    validate(raw_api.MoveArrayItem(id_, index),
             f'Failed to move array item {element_context(id_)} to {index}')


@handle_managed
def copy_element(id_, id2, as_new=False):
    return get_handle(
        lambda res: raw_api.CopyElement(id_, id2, as_new, res),
        error_msg=f'Failed to copy element {element_context(id_)} to {id2}')


@handle_managed
def find_next_element(id_, search, by_path, by_value):
    return get_handle(
        lambda res:
            raw_api.FindNextElement(id_, search, by_path, by_value, res),
        error_msg=f'Failed to find next element from {id_} via '
                  f'search={search}, by_path={by_path}, by_value={by_value}')


@handle_managed
def find_previous_element(id_, search, by_path, by_value):
    return get_handle(
        lambda res:
            raw_api.FindPreviousElement(id_, search, by_path, by_value, res),
        error_msg=f'Failed to find previous element from {id_} via '
                  f'search={search}, by_path={by_path}, by_value={by_value}')


def get_signature_allowed(id_, signature):
    return get_bool(
        lambda res: raw_api.GetSignatureAllowed(id_, signature, res),
        error_msg=f'Failed to check if signature {signature} is allowed on '
                  f'{element_context(id_)}')


def get_allowed_signatures(id_):
    return get_string_array(
        lambda len_: raw_api.GetAllowedSignatures(id_, len_),
        error_msg=f'Failed to get allowed signatures for '
                  f'{element_context(id_)}')


def get_is_modified(id_):
    return get_bool(
        lambda res: raw_api.GetIsModified(id_, res),
        error_msg=f'Failed to get is modified for {element_context(id_)}')


def get_is_editable(id_):
    return get_bool(
        lambda res: raw_api.GetIsEditable(id_, res),
        error_msg=f'Failed to get is editable for {element_context(id_)}')


def set_is_editable(id_, bool_):
    validate(raw_api.SetIsEditable(id_, bool_),
             f'Failed to set is editable for {element_context(id_)}')


def get_is_removable(id_):
    return get_bool(
        lambda res: raw_api.GetIsRemovable(id_, res),
        error_msg=f'Failed to get is removable for {element_context(id_)}')


def get_can_add(id_):
    return get_bool(
        lambda res: raw_api.GetCanAdd(id_, res),
        error_msg=f'Failed to get can add for {element_context(id_)}')


def element_type(id_):
    return get_byte(
        lambda res: raw_api.ElementType(id_, res),
        error_msg=f'Failed to get element type for {element_context(id_)}')


def def_type(id_):
    return get_byte(
        lambda res: raw_api.DefType(id_, res),
        error_msg=f'Failed to get def type for {element_context(id_)}')


def smash_type(id_):
    return get_byte(
        lambda res: raw_api.SmashType(id_, res),
        error_msg=f'Failed to get smash type for {element_context(id_)}')


def value_type(id_):
    return get_byte(
        lambda res: raw_api.ValueType(id_, res),
        error_msg=f'Failed to get value type for {element_context(id_)}')


def is_sorted(id_):
    return get_bool(
        lambda res: raw_api.IsSorted(id_, res),
        error_msg=f'Failed to get is sorted for {element_context(id_)}')


def is_fixed(id_):
    return get_bool(
        lambda res: raw_api.IsFixed(id_, res),
        error_msg=f'Failed to get is fixed for {element_context(id_)}')


def is_flags(id_):
    return value_type(id_) == ValueTypes.Flags.value


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


def array_item_context(id_, path, subpath, value):
    return f'{safe_element_path(id_)}, {path}, {subpath}, {value}'

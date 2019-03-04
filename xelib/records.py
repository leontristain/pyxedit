from enum import Enum, unique

from xelib.lib import raw_api
from xelib.helpers import get_unsigned_integer, validate, build_flags
from xelib.elements import (element_context,
                            get_value,
                            get_links_to,
                            get_element,
                            get_float_value,
                            set_float_value,
                            get_flag,
                            set_flag,
                            get_handle,
                            get_array,
                            get_bool,
                            get_string_array,
                            get_two_bytes)


@unique
class ConflictThis(Enum):
    Unknown = 'ctUnknown'
    Ignored = 'ctIgnored'
    NotDefined = 'ctNotDefined'
    IdenticalToMaster = 'ctIdenticalToMaster'
    OnlyOne = 'ctOnlyOne'
    HiddenByModGroup = 'ctHiddenByModGroup'
    Master = 'ctMaster'
    ConflictBenign = 'ctConflictBenign'
    Override = 'ctOverride'
    IdenticalToMasterWinsConflict = 'ctIdenticalToMasterWinsConflict'
    ConflictWins = 'ctConflictWins'
    ConflictLoses = 'ctConflictLoses'


@unique
class ConflictAll(Enum):
    Unknown = 'caUnknown'
    OnlyOne = 'caOnlyOne'
    NoConflict = 'caNoConflict'
    ConflictBenign = 'caConflictBenign'
    Override = 'caOverride'
    Conflict = 'caConflict'
    ConflictCritical = 'caConflictCritical'


@unique
class GetRefrsFlags(Enum):
    excludeDeleted = 1
    excludeDisabled = 2
    excludeXESP = 4


# ================
# record value method wrappers
# ================


def editor_id(id_):
    return get_value(id_, 'EDID')


def full_name(id_):
    return get_value(id_, 'FULL')


def get_ref_editor_id(id_, path):
    with get_links_to(id_, path) as linked:
        return editor_id(linked) if linked else ''


def translate(id_, vector):
    position = get_element(id_, 'DATA\\Position')
    for coord in ('X', 'Y', 'Z'):
        translate_value = vector.get(coord)
        if translate_value:
            new_value = get_float_value(position, coord) + translate_value
            set_float_value(position, 'X', new_value)


def rotate(id_, vector):
    rotation = get_element(id_, 'DATA\\Rotation')
    for coord in ('X', 'Y', 'Z'):
        rotation_value = vector.get(coord)
        if rotation_value:
            new_value = get_float_value(rotation, coord) + rotation_value
            set_float_value(rotation, coord, new_value)


def get_record_flag(id_, name):
    return get_flag(id_, 'Record Header\\Record Flags', name)


def set_record_flag(id_, name, state):
    set_flag(id_, 'Record Header\\Record Flags', name, state)


# ================
# records handling methods
# ================


def get_form_id(id_, native=False, local=False):
    form_id = get_unsigned_integer(
        lambda res: raw_api.GetFormID(id_, res, native),
        error_msg=f'Failed to get FormID for {element_context(id_)}')
    return form_id & 0xFFFFFF if local else form_id


def get_hex_form_id(id_, native=False, local=False):
    form_id = get_form_id(id_, native, local)
    return f'{form_id:0>6X}' if local else f'{form_id:0>6X}'


def set_form_id(id_, new_form_id, native=False, fix_references=True):
    validate(raw_api.SetFormId(id_, new_form_id, native, fix_references),
             f'Failed to set FormID on {element_context(id_)} to '
             f'{new_form_id}')


def get_record(id_, form_id, search_masters=True):
    return get_handle(
        lambda res: raw_api.GetRecord(id_, form_id, search_masters, res),
        error_msg=f'Failed to get record at {element_context(id_)}, {form_id}')


def get_records(id_, search='', include_overrides=False):
    return get_array(
        lambda len_: raw_api.GetRecords(id_, search, include_overrides, len_),
        error_msg=f'Failed to get {search} records from {element_context(id_)}')


def get_refrs(id_, search, opts=None):
    opts = opts or {}
    return get_array(
        lambda len_: raw_api.GetREFRs(id_, search, build_flags(opts), len_),
        error_msg=f'Failed to get {search} REFRs from {element_context(id_)}')


def get_overrides(id_):
    return get_array(
        lambda len_: raw_api.GetOverrides(id_, len),
        error_msg=f'Failed to get overrides for {element_context(id_)}')


def get_master_record(id_):
    return get_handle(
        lambda res: raw_api.GetMasterRecord(id_, res),
        error_msg=f'Failed to get master record for {element_context(id_)}')


def get_previous_override(id_, id2):
    return get_handle(
        lambda res: raw_api.GetPreviousOverride(id_, id2, res),
        error_msg=f'Failed to get previous override record for '
                  f'{element_context(id_)}, targetting file '
                  f'{element_context(id2)}')


def get_winning_override(id_):
    return get_handle(
        lambda res: raw_api.GetWinningOverride(id_, res),
        error_msg=f'Failed to get winning override record for '
                  f'{element_context(id_)}')


def get_injection_target(id_):
    return get_handle(
        lambda res: raw_api.GetInjectionTarget(id_, res),
        error_msg=f'Failed to get injection target for {element_context(id_)}')


def find_next_record(id_, search, by_edid, by_name):
    return get_handle(
        lambda res: raw_api.FindNextRecord(id_, search, by_edid, by_name, res))


def find_previous_record(id_, search, by_edid, by_name):
    return get_handle(
        lambda res: raw_api.FindPreviousRecord(id_,
                                               search,
                                               by_edid,
                                               by_name,
                                               res))


def find_valid_references(id_, signature, search, limit_to):
    return get_string_array(
        lambda len_: raw_api.FindValidReferences(id_,
                                                 signature,
                                                 search,
                                                 limit_to,
                                                 len_),
        error_msg=f'Failed to find valid {signature} references on '
                  f'{element_context(id_)} searching for {search}')


def get_referenced_by(id_):
    return get_array(
        lambda len_: raw_api.GetReferencedBy(id_, len_),
        error_msg=f'Failed to get referenced by for: {element_context(id_)}')


def exchange_references(id_, old_form_id, new_form_id):
    validate(raw_api.ExchangeReferences(id_, old_form_id, new_form_id),
             f'Failed to exchange references on {element_context(id_)} from '
             f'{old_form_id} to {new_form_id}')


def is_master(id_):
    return get_bool(lambda res: raw_api.IsMaster(id_, res))


def is_injected(id_):
    return get_bool(lambda res: raw_api.IsInjected(id_, res))


def is_override(id_):
    return get_bool(lambda res: raw_api.IsOverride(id_, res))


def is_winning_override(id_):
    return get_bool(lambda res: raw_api.IsWinningOverride(id_, res))


def get_nodes(id_):
    return get_handle(
        lambda res: raw_api.GetNodes(id_, res),
        error_msg=f'Failed to get nodes for {element_context(id_)}')


def get_conflict_data(id1, id2, as_string=False, ex=False):
    conflict_all, conflict_this = get_two_bytes(
        lambda res1, res2: raw_api.GetConflictData(id1, id2, res1, res2),
        error_msg=f'GetConflictData failed on {id1}, {id2}',
        ex=ex)
    if as_string:
        raise NotImplementedError
    else:
        return conflict_all, conflict_this


def get_conflict_data_ex(id1, id2, as_string=False):
    raise NotImplementedError


def get_record_conflict_data(id_):
    raise NotImplementedError


def get_node_elements(id1, id2):
    raise NotImplementedError


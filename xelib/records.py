from enum import Enum, unique


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
    raise NotImplementedError


def full_name(id_):
    raise NotImplementedError


def get_ref_editor_id(id_, path):
    raise NotImplementedError


def translate(id_, vector):
    raise NotImplementedError


def rotate(id_, vector):
    raise NotImplementedError


def get_record_flag(id_, name):
    raise NotImplementedError


def set_record_flag(id_, name, state):
    raise NotImplementedError


# ================
# records handling methods
# ================


def get_form_id(id_, native=False, local=False):
    raise NotImplementedError


def get_hex_form_id(id_, native=False, local=False):
    raise NotImplementedError


def set_form_id(id_, new_form_id, native=False, fix_references=True):
    raise NotImplementedError


def get_record(id_, form_id, search_masters=True):
    raise NotImplementedError


def get_records(id_, search='', include_overrides=False):
    raise NotImplementedError


def get_refrs(id_, search, opts=None):
    opts = opts or {}
    raise NotImplementedError


def get_overrides(id_):
    raise NotImplementedError


def get_master_record(id_):
    raise NotImplementedError


def get_previous_override(id_, id2):
    raise NotImplementedError


def get_winning_override(id_):
    raise NotImplementedError


def get_injection_target(id_):
    raise NotImplementedError


def find_next_record(id_, search, by_edid, by_name):
    raise NotImplementedError


def find_previous_record(id_, search, by_edid, by_name):
    raise NotImplementedError


def find_valid_references(id_, signature, search, limit_to):
    raise NotImplementedError


def get_referenced_by(id_):
    raise NotImplementedError


def exchange_references(id_, old_form_id, new_form_id):
    raise NotImplementedError


def is_master(id_):
    raise NotImplementedError


def is_injected(id_):
    raise NotImplementedError


def is_override(id_):
    raise NotImplementedError


def is_winning_override(id_):
    raise NotImplementedError


def get_nodes(id_):
    raise NotImplementedError


def get_conflict_data(id1, id2, as_string=False):
    raise NotImplementedError


def get_conflict_data_ex(id1, id2, as_string=False):
    raise NotImplementedError


def get_record_conflict_data(id_):
    raise NotImplementedError


def get_node_elements(id1, id2):
    raise NotImplementedError


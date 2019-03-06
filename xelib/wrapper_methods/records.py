from enum import Enum, unique

from xelib.wrapper_methods.base import WrapperMethodsBase


@unique
class ConflictThis(Enum):
    ctUnknown = 0
    ctIgnored = 1
    ctNotDefined = 2
    ctIdenticalToMaster = 3
    ctOnlyOne = 4
    ctHiddenByModGroup = 5
    ctMaster = 6
    ctConflictBenign = 7
    ctOverride = 8
    ctIdenticalToMasterWinsConflict = 9
    ctConflictWins = 10
    ctConflictLoses = 11


@unique
class ConflictAll(Enum):
    caUnknown = 0
    caOnlyOne = 1
    caNoConflict = 2
    caConflictBenign = 3
    caOverride = 4
    caConflict = 5
    caConflictCritical = 6


@unique
class GetRefrsFlags(Enum):
    excludeDeleted = 1
    excludeDisabled = 2
    excludeXESP = 4


class RecordsMethods(WrapperMethodsBase):
    ConflictThis = ConflictThis
    ConflictAll = ConflictAll
    GetRefrsFlags = GetRefrsFlags

    def get_form_id(self, id_, native=False, local=False):
        form_id = self.get_unsigned_integer(
            lambda res: self.raw_api.GetFormID(id_, res, native),
            error_msg=f'Failed to get FormID for {self.element_context(id_)}')
        return form_id & 0xFFFFFF if local else form_id

    def get_hex_form_id(self, id_, native=False, local=False):
        form_id = self.get_form_id(id_, native, local)
        return f'{form_id:0>6X}' if local else f'{form_id:0>6X}'

    def set_form_id(self, id_, new_form_id, native=False, fix_references=True):
        self.verify_execution(
            self.raw_api.SetFormId(id_, new_form_id, native, fix_references),
            error_msg=f'Failed to set FormID on {self.element_context(id_)} to '
                      f'{new_form_id}')

    def get_record(self, id_, form_id, search_masters=True):
        return self.get_handle(
            lambda res: self.raw_api.GetRecord(id_, form_id, search_masters, res),
            error_msg=f'Failed to get record at {self.element_context(id_)}, '
                      f'{form_id}')

    def get_records(self, id_, search='', include_overrides=False):
        return self.get_array(
            lambda len_:
                self.raw_api.GetRecords(id_, search, include_overrides, len_),
            error_msg=f'Failed to get {search} records from '
                      f'{self.element_context(id_)}')

    def get_refrs(self, id_, search, opts=None):
        opts = opts or {}
        return self.get_array(
            lambda len_:
                self.raw_api.GetREFRs(id_, search, self.build_flags(opts), len_),
            error_msg=f'Failed to get {search} REFRs from '
                      f'{self.element_context(id_)}')

    def get_overrides(self, id_):
        return self.get_array(
            lambda len_: self.raw_api.GetOverrides(id_, len),
            error_msg=f'Failed to get overrides for '
                      f'{self.element_context(id_)}')

    def get_master_record(self, id_):
        return self.get_handle(
            lambda res: self.raw_api.GetMasterRecord(id_, res),
            error_msg=f'Failed to get master record for '
                      f'{self.element_context(id_)}')

    def get_previous_override(self, id_, id2):
        return self.get_handle(
            lambda res: self.raw_api.GetPreviousOverride(id_, id2, res),
            error_msg=f'Failed to get previous override record for '
                      f'{self.element_context(id_)}, targetting file '
                      f'{self.element_context(id2)}')

    def get_winning_override(self, id_):
        return self.get_handle(
            lambda res: self.raw_api.GetWinningOverride(id_, res),
            error_msg=f'Failed to get winning override record for '
                      f'{self.element_context(id_)}')

    def get_injection_target(self, id_):
        return self.get_handle(
            lambda res: self.raw_api.GetInjectionTarget(id_, res),
            error_msg=f'Failed to get injection target for '
                      f'{self.element_context(id_)}')

    def find_next_record(self, id_, search, by_edid, by_name):
        return self.get_handle(
            lambda res:
                self.raw_api.FindNextRecord(id_, search, by_edid, by_name, res))

    def find_previous_record(self, id_, search, by_edid, by_name):
        return self.get_handle(
            lambda res: self.raw_api.FindPreviousRecord(id_,
                                                        search,
                                                        by_edid,
                                                        by_name,
                                                        res))

    def find_valid_references(self, id_, signature, search, limit_to):
        return self.get_string_array(
            lambda len_: self.raw_api.FindValidReferences(id_,
                                                          signature,
                                                          search,
                                                          limit_to,
                                                          len_),
            error_msg=f'Failed to find valid {signature} references on '
                      f'{self.element_context(id_)} searching for {search}')

    def get_referenced_by(self, id_):
        return self.get_array(
            lambda len_: self.raw_api.GetReferencedBy(id_, len_),
            error_msg=f'Failed to get referenced by for: '
                      f'{self.element_context(id_)}')

    def exchange_references(self, id_, old_form_id, new_form_id):
        self.verify_execution(
            self.raw_api.ExchangeReferences(id_, old_form_id, new_form_id),
            error_msg=f'Failed to exchange references on '
                      f'{self.element_context(id_)} from {old_form_id} to '
                      f'{new_form_id}')

    def is_master(self, id_):
        return self.get_bool(
            lambda res: self.raw_api.IsMaster(id_, res))

    def is_injected(self, id_):
        return self.get_bool(
            lambda res: self.raw_api.IsInjected(id_, res))

    def is_override(self, id_):
        return self.get_bool(
            lambda res: self.raw_api.IsOverride(id_, res))

    def is_winning_override(self, id_):
        return self.get_bool(
            lambda res: self.raw_api.IsWinningOverride(id_, res))

    def get_nodes(self, id_):
        return self.get_handle(
            lambda res: self.raw_api.GetNodes(id_, res),
            error_msg=f'Failed to get nodes for {self.element_context(id_)}')

    def get_conflict_data(self, id1, id2, as_string=False, ex=False):
        conflict_all, conflict_this = self.get_two_bytes(
            lambda res1, res2:
                self.raw_api.GetConflictData(id1, id2, res1, res2),
            error_msg=f'GetConflictData failed on {id1}, {id2}',
            ex=ex)
        if as_string:
            return (ConflictAll(conflict_all).name,
                    ConflictThis(conflict_this).name)
        else:
            return conflict_all, conflict_this

    def get_record_conflict_data(self, id_):
        return self.get_conflict_data(0, id_)

    def get_node_elements(self, id1, id2):
        return self.get_array(
            lambda len_: self.raw_api.GetNodeElements(id1, id2, len_),
            error_msg=f'GetNodeElements failed on {self.element_context(id1)}, '
                      f'{self.element_context(id2)}')

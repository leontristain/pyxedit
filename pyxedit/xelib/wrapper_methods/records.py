from enum import Enum, unique

from pyxedit.xelib.wrapper_methods.base import WrapperMethodsBase


@unique
class ConflictThis(Enum):
    Unknown = 0
    Ignored = 1
    NotDefined = 2
    IdenticalToMaster = 3
    OnlyOne = 4
    HiddenByModGroup = 5
    Master = 6
    ConflictBenign = 7
    Override = 8
    IdenticalToMasterWinsConflict = 9
    ConflictWins = 10
    ConflictLoses = 11


@unique
class ConflictAll(Enum):
    Unknown = 0
    OnlyOne = 1
    NoConflict = 2
    ConflictBenign = 3
    Override = 4
    Conflict = 5
    ConflictCritical = 6


@unique
class GetRefrsFlags(Enum):
    excludeDeleted = 1
    excludeDisabled = 2
    excludeXESP = 4


class RecordsMethods(WrapperMethodsBase):
    ConflictThis = ConflictThis
    ConflictAll = ConflictAll
    GetRefrsFlags = GetRefrsFlags

    def get_form_id(self, id_, native=False, local=False, ex=True):
        '''
        Returns the FormID of the record

        Args:
            id\\_ (``int``)
                id handle of record
            local (``bool``)
                whether to return the 'local' FormID, with the load order
                bits masked to to 00

        Returns:
            (``int``) FormID as an integer, use `xelib.get_hex_form_id` to turn
            it into a hex string for representational purposes
        '''
        form_id = self.get_unsigned_integer(
            lambda res: self.raw_api.GetFormID(id_, res, native),
            error_msg=f'Failed to get FormID for {self.element_context(id_)}',
            ex=ex)
        if form_id and local:
            return form_id & 0xFFFFFF
        return form_id

    def get_hex_form_id(self, id_, native=False, local=False, ex=True):
        '''
        Returns the FormID of the record as a hexadecimal string

        Args:
            id\\_ (``int``)
                id handle of record
            local (``bool``)
                whether to only return the lower 6 hex digits (ignore the upper
                2 which are for representing load order)

        Returns:
            (``str``) FormID in hex string form
        '''
        form_id = self.get_form_id(id_, native, local, ex=ex)
        return f'{form_id:0>6X}' if local else f'{form_id:0>8X}'

    def set_form_id(self,
                    id_,
                    new_form_id,
                    native=False,
                    fix_references=True,
                    ex=True):
        '''
        Sets the FormID of a record to a new FormID

        Args:
            id\\_ (``int``)
                id handle of record
            new_form_id (``int``)
                the new FormID to set the record to
            native (``bool``)
                TODO: figure out what this does, it probably means a 'local'
                FormID without the load order bits is given
            fix_references (``bool``)
                Adjust all references of this FormID to match within the current
                xEdit session (I think... xEdit does this by default after all)
        '''
        return self.verify_execution(
            self.raw_api.SetFormId(id_, new_form_id, native, fix_references),
            error_msg=f'Failed to set FormID on {self.element_context(id_)} to '
                      f'{new_form_id}',
            ex=ex)

    def get_record(self, id_, form_id, search_masters=True, ex=True):
        '''
        Finds and returns the record with the given FormID

        Args:
            id\\_ (``int``)
                id handle of file to start from. This can be passed a ``0``
                to search all loaded files.
            form_id (``int``)
                the FormID to search for, if searching all files, this should
                be a "global" FormID with the load order bits included; if
                searching a particular file, this should be a "local" FormID
                without the load order bits.
        '''
        return self.get_handle(
            lambda res: self.raw_api.GetRecord(id_, form_id, search_masters, res),
            error_msg=f'Failed to get record at {self.element_context(id_)}, '
                      f'{form_id}',
            ex=ex)

    def get_records(self, id_, search='', include_overrides=False, ex=True):
        '''
        Returns a list of all records matching ``search`` found in ``id_``.

        Args:
            id\\_ (``int``)
                id handle of file to search. Pass ``0`` to search all loaded
                files
            search (``str``)
                string to search for, if left empty, all records will be
                returned. Strings like ``'ARMO'``, ``'COBJ'``,
                ``'ARMO,WEAP,MISC'``, or
                ``'Constructible Object,Non-Player Character (Actor)'`` may
                be passed to filter down results.
            include_overrides (``bool``)
                whether to include override records that originate from master
                plugins

        Returns:
            (``List[int]``) a list of id handles for found records
        '''
        return self.get_array(
            lambda len_:
                self.raw_api.GetRecords(id_, search, include_overrides, len_),
            error_msg=f'Failed to get {search} records from '
                      f'{self.element_context(id_)}',
            ex=ex)

    def get_refrs(self, id_, search, opts=None, ex=True):
        '''
        Returns an array of all REFR records referencing base records with
        signatures in ``search`` found within ``id_``.

        Args:
            id\\_ (``int``)
                id handle to start from
            search (``str``)
                string to search for, Strings like ``'DOOR'`` can be passed
            opts (``List[pyxedit.xelib.GetRefrsFlags]``)
                list of options to further tweak behavior

        Returns:
            (``List[int]``) a list of id handles for found references
        '''
        opts = opts or []
        return self.get_array(
            lambda len_:
                self.raw_api.GetREFRs(id_, search, self.build_flags(opts), len_),
            error_msg=f'Failed to get {search} REFRs from '
                      f'{self.element_context(id_)}',
            ex=ex)

    def get_overrides(self, id_, ex=True):
        '''
        Returns an array of handles corresponding to the overrides of given
        record.

        Args:
            id\\_ (``int``)
                id handle of record to get overrides for

        Returns:
            (``List[int]``) id handles for override records
        '''
        return self.get_array(
            lambda len_: self.raw_api.GetOverrides(id_, len_),
            error_msg=f'Failed to get overrides for '
                      f'{self.element_context(id_)}',
            ex=ex)

    def get_master_record(self, id_, ex=True):
        '''
        Returns the master record of given record.

        Args:
            id\\_ (``int``)
                id handle of record to get master record for

        Returns:
            (``int``) id handle for master record; if given record is already
            a master record, a new id handle will be returned
        '''
        return self.get_handle(
            lambda res: self.raw_api.GetMasterRecord(id_, res),
            error_msg=f'Failed to get master record for '
                      f'{self.element_context(id_)}',
            ex=ex)

    def get_previous_override(self, id_, id2, ex=True):
        '''
        Returns a handle for the winning override of the given record
        in the masters of a given file.

        Args:
            id\\_ (``int``)
                id handle of record to get previous override for
            id2 (``int``)
                id handle to the given file

        Returns:
            (``int``) id handle to the winning override on the record
            among the given file's master files
        '''
        return self.get_handle(
            lambda res: self.raw_api.GetPreviousOverride(id_, id2, res),
            error_msg=f'Failed to get previous override record for '
                      f'{self.element_context(id_)}, targetting file '
                      f'{self.element_context(id2)}',
            ex=ex)

    def get_winning_override(self, id_, ex=True):
        '''
        Returns a handle for the winning override of given record

        Args:
            id\\_ (``int``)
                id handle of record to get winning override for

        Returns:
            (``int``) id handle to the winning override record
        '''
        return self.get_handle(
            lambda res: self.raw_api.GetWinningOverride(id_, res),
            error_msg=f'Failed to get winning override record for '
                      f'{self.element_context(id_)}',
            ex=ex)

    def get_injection_target(self, id_, ex=True):
        '''
        Returns a handle for the file that the given record is injected into.

        Args:
            id\\_ (``int``)
                id handle of record to get injection target for

        Returns:
            (``int``) id handle of file the record is injected into.
        '''
        return self.get_handle(
            lambda res: self.raw_api.GetInjectionTarget(id_, res),
            error_msg=f'Failed to get injection target for '
                      f'{self.element_context(id_)}',
            ex=ex)

    def find_next_record(self, id_, search, by_edid, by_name, ex=True):
        '''
        Returns the next record after the given record which matches ``search``.

        Args:
            id\\_ (``int``)
                id handle of record to find the next record for
            search (``str``)
                search filter to limit the search to
            by_edid (``bool``)
                TODO: figure out what this does
            by_name (``bool``)
                TODO: figure out what this does

        Returns:
            (``int``) id handle of next record
        '''
        return self.get_handle(
            lambda res:
                self.raw_api.FindNextRecord(id_, search, by_edid, by_name, res),
            error_msg=f'Failed to find next record for '
                      f'{self.element_context(id_)}',
            ex=ex)

    def find_previous_record(self, id_, search, by_edid, by_name, ex=True):
        '''
        Returns the previous record after the given record which matches
        ``search``.

        Args:
            id\\_ (``int``)
                id handle of record to find the previous record for
            search (``str``)
                search filter to limit the search to
            by_edid (``bool``)
                TODO: figure out what this does
            by_name (``bool``)
                TODO: figure out what this does

        Returns:
            (``int``) id handle of previous record
        '''
        return self.get_handle(
            lambda res: self.raw_api.FindPreviousRecord(id_,
                                                        search,
                                                        by_edid,
                                                        by_name,
                                                        res),
            error_msg=f'Failed to find previous record for '
                      f'{self.element_context(id_)}',
            ex=ex)

    def find_valid_references(self, id_, signature, search, limit_to, ex=True):
        '''
        Returns up to ``limit_to`` records matching ``signature``, which can be
        referenced by the file containing the given record. Exclude results
        which do not contain ``search`` in their long names.

        Args:
            id\\_ (``int``)
                find valid references for the file containing this record
            signature (``str``)
                return valid referenceable results matching this signature
            search (``str``)
                limit the search to referenceable results that match this search
                string
            limit_to (``int``)
                limit to this many search results

        Returns:
            (``List[int]``) a list of referenceable records by the file of the
            given record
        '''
        return self.get_string_array(
            lambda len_: self.raw_api.FindValidReferences(id_,
                                                          signature,
                                                          search,
                                                          limit_to,
                                                          len_),
            error_msg=f'Failed to find valid {signature} references on '
                      f'{self.element_context(id_)} searching for {search}',
            ex=ex)

    def get_referenced_by(self, id_, ex=True):
        '''
        Returns an array of the records that reference the given record.
        References must be built with ``xelib.build_references`` to be returned.

        Args:
            id\\_ (``int``)
                id handle of record to find references for

        Returns:
            (``List[int]``) a list of records that reference it
        '''
        return self.get_array(
            lambda len_: self.raw_api.GetReferencedBy(id_, len_),
            error_msg=f'Failed to get referenced by for: '
                      f'{self.element_context(id_)}',
            ex=ex)

    def exchange_references(self, id_, old_form_id, new_form_id, ex=True):
        '''
        Exchanges all references to ``old_form_id`` with references to
        ``new_form_id`` on the given record.

        Args:
            id\\_ (``int``)
                id handle of record to exchange references on
            old_form_id (``int``)
                exchange references from this FormID
            new_form_id (``int``)
                exchange references to this FormID
        '''
        return self.verify_execution(
            self.raw_api.ExchangeReferences(id_, old_form_id, new_form_id),
            error_msg=f'Failed to exchange references on '
                      f'{self.element_context(id_)} from {old_form_id} to '
                      f'{new_form_id}',
            ex=ex)

    def is_master(self, id_, ex=True):
        '''
        Returns true if given record is a master record

        Args:
            id\\_ (``int``)
                id handle of record

        Returns:
            (``bool``) whether record is master record
        '''
        return self.get_bool(
            lambda res: self.raw_api.IsMaster(id_, res),
            ex=ex)

    def is_injected(self, id_, ex=True):
        '''
        Returns true if given record is a injected record

        Args:
            id\\_ (``int``)
                id handle of record

        Returns:
            (``bool``) whether record is injected record
        '''
        return self.get_bool(
            lambda res: self.raw_api.IsInjected(id_, res),
            ex=ex)

    def is_override(self, id_, ex=True):
        '''
        Returns true if given record is a override record

        Args:
            id\\_ (``int``)
                id handle of record

        Returns:
            (``bool``) whether record is override record
        '''
        return self.get_bool(
            lambda res: self.raw_api.IsOverride(id_, res),
            ex=ex)

    def is_winning_override(self, id_, ex=True):
        '''
        Returns true if given record is a winning override record

        Args:
            id\\_ (``int``)
                id handle of record

        Returns:
            (``bool``) whether record is winning override record
        '''
        return self.get_bool(
            lambda res: self.raw_api.IsWinningOverride(id_, res),
            ex=ex)

    def get_record_def(self, sig, ex=True):
        '''
        TODO: figure out what this does
        '''
        return self.get_handle(
            lambda res: self.raw_api.GetRecordDef(sig, res),
            error_msg=f'Failed to get record def for {sig}',
            ex=ex)

    def get_nodes(self, id_, ex=True):
        '''
        Returns a handle pointing to a node tree for ``id_``. The handle
        returned by this function must be freed with ``xelib.release_nodes``.
        NOTE: this can be slow for very large records like ``NAVI``

        Args:
            id\\_ (``int``)
                id handle of record to get node tree for

        Returns:
            (``int``) id handle to node tree
        '''
        return self.get_handle(
            lambda res: self.raw_api.GetNodes(id_, res),
            error_msg=f'Failed to get nodes for {self.element_context(id_)}',
            ex=ex)

    def get_conflict_data(self, nodes, handle, as_string=False, ex=False):
        '''
        Returns conflict for a given element.

        Args:
            nodes (``int``)
                id handle of node tree returned by ``get_nodes`` when called
                on ``handle``
            handle (``int``)
                id handle of element to operate on
            as_string (``bool``)
                if set to true, results will be returned as strings instead
                of enum values

        Returns:
            (``pyxedit.xelib.ConflictAll, pyxedit.xelib.ConflictThis`` or
            ``str, str``) conflict information for element
        '''
        conflict_all, conflict_this = self.get_two_bytes(
            lambda res1, res2:
                self.raw_api.GetConflictData(nodes, handle, res1, res2),
            error_msg=f'GetConflictData failed on {nodes}, {handle}',
            ex=ex)

        conflict_all = ConflictAll(conflict_all or 0)
        conflict_this = ConflictThis(conflict_this or 0)

        if as_string:
            return conflict_all.name, conflict_this.name
        else:
            return conflict_all, conflict_this

    def get_record_conflict_data(self, element, ex=False):
        '''
        TODO: figure out what this does
        '''
        return self.get_conflict_data(0, element, ex=ex)

    def get_node_elements(self, nodes, element, ex=True):
        '''
        Returns handles for the element children of ``element``.

        Args:
            nodes (``int``)
                id handle of node tree returned by ``get_nodes`` when called
                on ``handle``
            handle (``int``)
                id handle of element to get child elements for

        Returns:
            (``List[Optional[int]]``) A list of handles for child elements
            under the given element, including ``None`` placeholders for
            unassigned elements.
        '''
        return self.get_array(
            lambda len_: self.raw_api.GetNodeElements(nodes, element, len_),
            error_msg=f'GetNodeElements failed on {self.element_context(nodes)}, '
                      f'{self.element_context(element)}',
            ex=ex)

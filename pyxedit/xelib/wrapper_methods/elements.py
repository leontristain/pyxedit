from enum import Enum, unique

from pyxedit.xelib.wrapper_methods.base import WrapperMethodsBase


@unique
class ElementTypes(Enum):
    '''
    A list of element types supported by ``XEditLib.dll``.

    .. list-table::
        :widths: 20 80
        :header-rows: 0
        :align: left

        * - ``ElementTypes.File``
          - A file record (i.e. root of a plugin)
        * - ``ElementTypes.MainRecord``
          - A main record
        * - ``ElementTypes.GroupRecord``
          - A group record
        * - ``ElementTypes.SubRecord``
          - A typical subrecord
        * - ``ElementTypes.SubRecordStruct``
          - A subrecord in struct format
        * - ``ElementTypes.SubRecordArray``
          - A subrecord in array format
        * - ``ElementTypes.SubRecordUnion``
          -
        * - ``ElementTypes.Array``
          - An array
        * - ``ElementTypes.Struct``
          - A struct
        * - ``ElementTypes.Flags``
          - A set of flags
        * - ``ElementTypes.StringListTerminator``
          -
        * - ``ElementTypes.Union``
          -
        * - ``ElementTypes.StructChapter``
          -
    '''
    File = 0
    MainRecord = 1
    GroupRecord = 2
    SubRecord = 3
    SubRecordStruct = 4
    SubRecordArray = 5
    SubRecordUnion = 6
    Array = 7
    Struct = 8
    Value = 9
    Flag = 10
    StringListTerminator = 11
    Union = 12
    StructChapter = 13


@unique
class DefTypes(Enum):
    '''
    A list of def types supported by ``XEditLib.dll``.

    .. list-table::
        :widths: 20 80
        :header-rows: 0
        :align: left

        * - ``DefTypes.Record``
          -
        * - ``DefTypes.SubRecord``
          -
        * - ``DefTypes.SubRecordArray``
          -
        * - ``DefTypes.SubRecordStruct``
          -
        * - ``DefTypes.SubRecordUnion``
          -
        * - ``DefTypes.String``
          -
        * - ``DefTypes.LString``
          -
        * - ``DefTypes.LenString``
          -
        * - ``DefTypes.ByteArray``
          -
        * - ``DefTypes.Integer``
          -
        * - ``DefTypes.IntegerFormater``
          -
        * - ``DefTypes.IntegerFormaterUnion``
          -
        * - ``DefTypes.Flag``
          -
        * - ``DefTypes.Float``
          -
        * - ``DefTypes.Array``
          -
        * - ``DefTypes.Struct``
          -
        * - ``DefTypes.Union``
          -
        * - ``DefTypes.Empty``
          -
        * - ``DefTypes.StructChapter``
          -
    '''
    Record = 0
    SubRecord = 1
    SubRecordArray = 2
    SubRecordStruct = 3
    SubRecordUnion = 4
    String = 5
    LString = 6
    LenString = 7
    ByteArray = 8
    Integer = 9
    IntegerFormater = 10
    IntegerFormaterUnion = 11
    Flag = 12
    Float = 13
    Array = 14
    Struct = 15
    Union = 16
    Empty = 17
    StructChapter = 18


@unique
class SmashTypes(Enum):
    '''
    A list of smash types supported by ``XEditLib.dll``.

    .. list-table::
        :widths: 20 80
        :header-rows: 0
        :align: left

        * - ``DefTypes.Unknown``
          -
        * - ``DefTypes.Record``
          -
        * - ``DefTypes.String``
          -
        * - ``DefTypes.Integer``
          -
        * - ``DefTypes.Flag``
          -
        * - ``DefTypes.Float``
          -
        * - ``DefTypes.UnsortedArray``
          -
        * - ``DefTypes.UnsortedStructArray``
          -
        * - ``DefTypes.SortedArray``
          -
        * - ``DefTypes.SortedStructArray``
          -
        * - ``DefTypes.ByteArray``
          -
        * - ``DefTypes.Union``
          -
    '''
    Unknown = 0
    Record = 1
    String = 2
    Integer = 3
    Flag = 4
    Float = 5
    Struct = 6
    UnsortedArray = 7
    UnsortedStructArray = 8
    SortedArray = 9
    SortedStructArray = 10
    ByteArray = 11
    Union = 12


@unique
class ValueTypes(Enum):
    '''
    A list of value types supported by ``XEditLib.dll``.

    .. list-table::
        :widths: 20 80
        :header-rows: 0
        :align: left

        * - ``DefTypes.Unknown``
          -
        * - ``DefTypes.Bytes``
          -
        * - ``DefTypes.Number``
          -
        * - ``DefTypes.String``
          -
        * - ``DefTypes.Text``
          -
        * - ``DefTypes.Reference``
          -
        * - ``DefTypes.Flags``
          -
        * - ``DefTypes.Enum``
          -
        * - ``DefTypes.Color``
          -
        * - ``DefTypes.Array``
          -
        * - ``DefTypes.Struct``
          -
    '''
    Unknown = 0
    Bytes = 1
    Number = 2
    String = 3
    Text = 4
    Reference = 5
    Flags = 6
    Enum = 7
    Color = 8
    Array = 9
    Struct = 10


class ElementsMethods(WrapperMethodsBase):
    ElementTypes = ElementTypes
    DefTypes = DefTypes
    SmashTypes = SmashTypes
    ValueTypes = ValueTypes

    def has_element(self, id_, path='', ex=True):
        '''
        Checks if an element exists at the given ``path`` from the ``id_`` of
        some starting element.

        Args:
            id\\_ (``int``):
                the id of the starting element; keep in mind that the root
                element has an id of `0`
            path (``str``):
                the subpath relative to the root element to check for the
                existence of an element at

        Returns:
            (``bool``) whether an element exists at the subpath
        '''
        return self.get_bool(
            lambda res: self.raw_api.HasElement(id_, path, res),
            error_msg=f'Failed to check if element exists at '
                      f'{self.element_context(id_, path)}',
            ex=ex)

    def get_element(self, id_, path='', ex=False):
        '''
        Resolves the element at ``path`` from the ``id_`` of some starting
        element, and returns a handle to it.

        Args:
            id\\_ (``int``):
                the id of the starting element; keep in mind that the root
                element has an id of `0`
            path (``str``):
                the subpath relative to the root element to get an element at

        Returns:
            (``int``) a handle to the element; `0` if element is not found there
        '''
        return self.get_handle(
            lambda res: self.raw_api.GetElement(id_, path, res),
            error_msg=f'Failed to get element at '
                      f'{self.element_context(id_, path)}',
            ex=ex)

    def add_element(self, id_, path='', ex=True):
        '''
        Traverses ``path`` from some starting element of handle ``id_``,
        creating any elements that are not found. Returns a handle to the
        element at the end of the path.

        Args:
            id\\_ (``int``):
                the id of the starting element; keep in mind that the root
                element has an id of `0`
            path (``str``):
                the subpath relative to the root element to create elements
                up to

        Returns:
            (``int``) handle to the created element at the end of the path
        '''
        return self.get_handle(
            lambda res: self.raw_api.AddElement(id_, path, res),
            error_msg=f'Failed to create new element at '
                      f'{self.element_context(id_, path)}',
            ex=ex)

    def add_element_value(self, id_, path, value, ex=True):
        '''
        Traverses ``path`` from some starting element of handle ``id_``,
        creating any elements that are not found. Sets the value of the element
        at the end of the path to ``value``, and returns a handle to it.

        Args:
            id\\_ (``int``):
                the id of the starting element; keep in mind that the root
                element has an id of `0`
            path (``str``):
                the subpath relative to the root element to create elements
                up to
            value (``str``):
                set the value of the end element to this

        Returns:
            (``int``) handle to the created element at the end of the path
        '''
        return self.get_handle(
            lambda res: self.raw_api.AddElementValue(id_, path, value, res),
            error_msg=f'Failed to create new element at '
                      f'{self.element_context(id_, path)}, with value: {value}',
            ex=ex)

    def remove_element(self, id_, path='', ex=True):
        '''
        Removes the element at ``path`` (from some starting element of handle
        ``id_``) if it exists.

        Args:
            id\\_ (``int``):
                the id of the starting element; keep in mind that the root
                element has an id of `0`
            path (``str``):
                the subpath relative to the root element to remove an element
                at; if empty, this should resolve to the starting element itself
        '''
        return self.verify_execution(
            self.raw_api.RemoveElement(id_, path),
            error_msg=f'Failed to remove element at '
                      f'{self.element_context(id_, path)}',
            ex=ex)

    def remove_element_or_parent(self, id_, ex=True):
        '''
        Removes the element of a handle ``id_``. If the element cannot be
        removed, it gets its parent container and attempts to remove it.
        This repeats until the container can be removed, or the code reaches
        a main record.

        Args:
            id\\_ (``int``):
                the id of the element to try to remove, together with any
                parent containers if necessary
        '''
        return self.verify_execution(
            self.raw_api.RemoveElementOrParent(id_),
            error_msg=f'Failed to remove element '
                      f'{self.element_context(id_)}',
            ex=ex)

    def set_element(self, id1, id2, ex=True):
        '''
        Assigns ``id2`` to ``id1``. This is equivalent to drag and drop.

        TODO: Figure out what xelib meant by "drag and drop" and rewrite
        this help text.

        Args:
            id1 (``int``):
                An id to assign ``id2`` to.
            id2 (``int``)
                The id to assign to ``id1``.
        '''
        return self.verify_execution(
            self.raw_api.SetElement(id1, id2),
            error_msg=f'Failed to set element at '
                      f'{self.element_context(id2)} to '
                      f'{self.element_context(id1)}',
            ex=ex)

    def get_elements(self, id_=0, path='', sort=False, filter=False, sparse=False, ex=True):
        '''
        Returns an array of handles for all the elements found in the container
        at ``path``

        Args:
            id\\_ (``int``):
                The id of the element to try to find elements from
            path (``str``)
                The path from the ``id_`` to find elements at
            sort (``bool``)
                TODO: figure out what this does
            filter (``bool``)
                TODO: figure out what this does
            sparse (``bool``)
                TODO: figure out what this does

        Returns:
            (``List[int]``) a list of ids representing elements found
        '''
        return self.get_array(
            lambda len_:
                self.raw_api.GetElements(id_, path, sort, filter, sparse, len_),
            error_msg=f'Failed to get child elements at '
                      f'{self.element_context(id_, path)}',
            ex=ex)

    def get_def_names(self, id_, ex=True):
        '''
        Returns an array of the names of all elements that can exist at ``path``

        Args:
            id\\_ (``int``)
                The id of the element to generate a list of def names for

        Returns:
            (``List[str]``) A list of string names, with values like
            ``'OBND - Object Bounds'``
        '''
        return self.get_string_array(
            lambda len_: self.raw_api.GetDefNames(id_, len_),
            error_msg=f'Failed to get def names for '
                      f'{self.element_context(id_)}',
            ex=ex)

    def get_add_list(self, id_, ex=True):
        '''
        Returns an array of the signatures that can be added to ``id_``

        Args:
            id\\_ (``int``)
                The id of the element to generate a list of addable signatures
                for

        Returns:
            (``List[str]``) A list of string names, with values like
            ``'AACT - Action'``, representing a list of addable signatures for
            the element.
        '''
        return self.get_string_array(
            lambda len_: self.raw_api.GetAddList(id_, len_),
            error_msg=f'Failed to get add list for {self.element_context(id_)}',
            ex=ex)

    def get_links_to(self, id_, path='', ex=False):
        '''
        Returns the record referenced by the element at ``path``. Note that this
        returns the master of the record, _not_ the winning override.

        Args:
            id\\_ (``int``)
                The id of the element to look for reference target from
            path (``str``)
                The subpath from the element where the reference is at

        Returns:
            (``int``) id of target record of the reference
        '''
        return self.get_handle(
            lambda res: self.raw_api.GetLinksTo(id_, path, res),
            error_msg=f'Failed to get reference at '
                      f'{self.element_context(id_, path)}',
            ex=ex)

    def set_links_to(self, id_, id2, path='', ex=True):
        '''
        Sets the record referenced by the element at ``path`` to ``id2``

        Args:
            id\\_ (``int``)
                The id of the element to start from
            id2 (``int``)
                The id of the reference target to set to
            path (``str``)
                The subpath from the element where the reference is at, this
                reference will be set to the target pointed by ``id2``
        '''
        return self.verify_execution(
            self.raw_api.SetLinksTo(id_, path, id2),
            error_msg=f'Failed to set reference at '
                      f'{self.element_context(id_, path)}',
            ex=ex)

    def get_container(self, id_, ex=False):
        '''
        Returns a handle to the container of ``id``

        Args:
            id\\_ (``int``)
                The id of the element to get container for
        '''
        return self.get_handle(
            lambda res: self.raw_api.GetContainer(id_, res),
            error_msg=f'Failed to get container for '
                      f'{self.element_context(id_)}',
            ex=ex)

    def get_element_file(self, id_, ex=True):
        '''
        Returns a handle to the file (i.e. plugin) ``id`` belongs to

        Args:
            id\\_ (``int``)
                The id of the element to get the file/plugin for

        Returns:
            (``int``) Handle id pointing to the file/plugin of the element
        '''
        return self.get_handle(
            lambda res: self.raw_api.GetElementFile(id_, res),
            error_msg=f'Failed to get element file for '
                      f'{self.element_context(id_)}',
            ex=ex)

    def get_element_group(self, id_, ex=True):
        '''
        Returns a handle to the group the element belongs to

        Args:
            id\\_ (``int``)
                The id of the element to get group for

        Returns:
            (``int``) (I'm guessing, haven't confirmed) Handle id pointing to
            the group record this element is a part of
        '''
        return self.get_handle(
            lambda res: self.raw_api.GetElementGroup(id_, res),
            error_msg=f'Failed to get element group for: '
                      f'{self.element_context(id_)}',
            ex=ex)

    def get_element_record(self, id_, ex=True):
        '''
        Returns a handle to the record the element belongs to

        Args:
            id\\_ (``int``)
                The id of the element to get record for

        Returns:
            (``int``) (I'm guessing, haven't confirmed) Handle id pointing to
            the record this element is part of
        '''
        return self.get_handle(
            lambda res: self.raw_api.GetElementRecord(id_, res),
            error_msg=f'Failed to get element record for: '
                      f'{self.element_context(id_)}',
            ex=ex)

    def element_count(self, id_, ex=True):
        '''
        Returns the number of element children ``id_`` has

        Args:
            id\\_ (``int``)
                Counts children under this element

        Returns:
            (``int``) number of child elements
        '''
        return self.get_integer(
            lambda res: self.raw_api.ElementCount(id_, res),
            error_msg=f'Failed to get element count for '
                      f'{self.element_context(id_)}',
            ex=ex)

    def element_equals(self, id_, id2, ex=True):
        '''
        Returns true if ``id_`` and ``id2`` refer to the same element

        Args:
            id\\_ (``int``)
                element to check if equal to ``id2``
            id2 (``int``)
                element to check if equal to ``id_``

        Returns:
            (``bool``) whether two handles point to the same element
        '''
        return self.get_bool(
            lambda res: self.raw_api.ElementEquals(id_, id2, res),
            error_msg=f'Failed to check element equality for '
                      f'{self.element_context(id_)} and '
                      f'{self.element_context(id2)}',
            ex=ex)

    def element_matches(self, id_, path, value, ex=True):
        '''
        Returns true if the value at ``path`` matches ``value``. When the
        element at ``path`` contains a reference, ``value`` can be a FormID,
        Editor ID, or FULL Name. FULL Names passed to this function must be
        surrounded by double quotes.

        Args:
            id\\_ (``int``)
                element to start from
            path (``str``)
                path from the starting element leading to element to act on
            value (``Any``)
                the value to check against, can be various types depending
                on the element being checked

        Returns:
            (``bool``) whether the element value matches given value
        '''
        return self.get_bool(
            lambda res: self.raw_api.ElementMatches(id_, path, value, res),
            error_msg=f'Failed to check element matches for '
                      f'{self.element_context(id_, path)},{value}',
            ex=ex)

    def has_array_item(self, id_, path, subpath, value, ex=True):
        '''
        Returns true if the array at ``path`` contains an item which matches
        ``value`` at ``subpath``

        Args:
            id\\_ (``int``)
                element to start from
            path (``str``)
                path from the starting element leading to the array to act on
            subpath (``str``)
                subpath under an array item to check for a value match
            value (``Any``)
                the value to check against

        Returns:
            (``bool``) whether an array item at the subpath with the given value
            exists
        '''
        return self.get_bool(
            lambda res:
                self.raw_api.HasArrayItem(id_, path, subpath, value, res),
            error_msg=f'Failed to check if array has item for '
                      f'{self.array_item_context(id_, path, subpath, value)}',
            ex=ex)

    def get_array_item(self, id_, path, subpath, value, ex=True):
        '''
        Returns the first item in the array at ``path`` which matches ``value``
        at ``subpath``.

        Args:
            id\\_ (``int``)
                element to start from
            path (``str``)
                path from the starting element leading to the array element
                to act on
            subpath (``str``)
                subpath under an array item to check for a value match for
            value (``Any``)
                the value to find array item with

        Returns:
            (``int``) handle to array item found with subpath, value matching
            what is given
        '''
        return self.get_handle(
            lambda res:
                self.raw_api.GetArrayItem(id_, path, subpath, value, res),
            error_msg=f'Failed to get array item for '
                      f'{self.array_item_context(id_, path, subpath, value)}',
            ex=ex)

    def add_array_item(self, id_, path, subpath, value, ex=True):
        '''
        Adds an item to the array at ``path`` and sets ``value`` at ``subpath``.
        Returns a handle to the added array item.

        Args:
            id\\_ (``int``)
                element to start from
            path (``str``)
                path from the starting element leading to the array element
                to act on
            subpath (``str``)
                the added array item will have the given value at this subpath
                under the item
            value (``Any``)
                the added array item will have this value at the given subpath

        Returns:
            (``int``) handle to the added array item
        '''
        return self.get_handle(
            lambda res:
                self.raw_api.AddArrayItem(id_, path, subpath, value, res),
            error_msg=f'Failed to add array item to '
                      f'{self.array_item_context(id_, path, subpath, value)}',
            ex=ex)

    def remove_array_item(self, id_, path, subpath, value, ex=True):
        '''
        Removes the first item in the array at ``path`` which matches ``value``
        at ``subpath``.

        Args:
            id\\_ (``int``)
                element to start from
            path (``str``)
                path from the starting element leading to the array element
                to act on
            subpath (``str``)
                look for an element with this subpath with the given value to
                remove
            value (``any``)
                look for an element with the given subpath with this value to
                remove
        '''
        return self.verify_execution(
            self.raw_api.RemoveArrayItem(id_, path, subpath, value),
            error_msg=f'Failed to remove array item '
                      f'{self.array_item_context(id_, path, subpath, value)}',
            ex=ex)

    def move_array_item(self, id_, index, ex=True):
        '''
        Moves the array item ``id_`` to position ``index``

        Args:
            id\\_ (``int``)
                an array item element to act on
            index (``int``)
                move the given array item to this index
        '''
        return self.verify_execution(
            self.raw_api.MoveArrayItem(id_, index),
            error_msg=f'Failed to move array item {self.element_context(id_)} '
                      f'to {index}',
            ex=ex)

    def copy_element(self, id_, id2, as_new=False, ex=True):
        '''
        Copies element ``id_`` into ``id2``. Records are copied as overrides if
        ``asNew`` is False. Returns a handle to the copied element.

        Args:
            id\\_ (``int``)
                copy from this element
            id2 (``int``)
                copy into this element
            as_new (``bool``)
                whether to copy as a new record instead of copy as override

        Returns:
            (``int``) handle to the copied element
        '''
        return self.get_handle(
            lambda res: self.raw_api.CopyElement(id_, id2, as_new, res),
            error_msg=f'Failed to copy element {self.element_context(id_)} to '
                      f'{id2}',
            ex=ex)

    def find_next_element(self, id_, search, by_path, by_value, ex=True):
        '''
        TODO: figure out what this does
        '''
        return self.get_handle(
            lambda res: self.raw_api.FindNextElement(id_,
                                                     search,
                                                     by_path,
                                                     by_value,
                                                     res),
            error_msg=f'Failed to find next element from {id_} via '
                      f'search={search}, by_path={by_path}, '
                      f'by_value={by_value}',
            ex=ex)

    def find_previous_element(self, id_, search, by_path, by_value, ex=True):
        '''
        TODO: figure out what this does
        '''
        return self.get_handle(
            lambda res: self.raw_api.FindPreviousElement(id_,
                                                         search,
                                                         by_path,
                                                         by_value,
                                                         res),
            error_msg=f'Failed to find previous element from {id_} via '
                      f'search={search}, by_path={by_path}, '
                      f'by_value={by_value}',
            ex=ex)

    def get_signature_allowed(self, id_, signature, ex=True):
        '''
        Returns true if ``id_`` is allowed to reference ``signature``

        Args:
            id\\_ (``int``)
                id of an element, expected to be a reference element
            signature (``str``)
                a string signature like ``'ARMO'`` or ``'KYWD'`` to check for

        Returns:
            (``bool``) whether the signature is a legal reference to set for
            the element
        '''
        return self.get_bool(
            lambda res: self.raw_api.GetSignatureAllowed(id_, signature, res),
            error_msg=f'Failed to check if signature {signature} is allowed on '
                      f'{self.element_context(id_)}',
            ex=ex)

    def get_allowed_signatures(self, id_, ex=True):
        '''
        Returns an array of all signatures ``id_`` is allowed to reference.

        Args:
            id\\_ (``int``)
                id of an element, expected to be a reference element

        Returns:
            (``List(str)``) a list of signatures (e.g. ``['KYWD', 'NULL']``)
            that the element is allowed to reference
        '''
        return self.get_string_array(
            lambda len_: self.raw_api.GetAllowedSignatures(id_, len_),
            error_msg=f'Failed to get allowed signatures for '
                      f'{self.element_context(id_)}',
            ex=ex)

    def get_is_modified(self, id_, ex=True):
        '''
        Returns true if ``id_`` has been modified during the current session.

        Args:
            id\\_ (``int``)
                id of an element to check whether modified

        Returns:
            (``bool``) whether element has been modified in current session
        '''
        return self.get_bool(
            lambda res: self.raw_api.GetIsModified(id_, res),
            error_msg=f'Failed to get is modified for '
                      f'{self.element_context(id_)}',
            ex=ex)

    def get_is_editable(self, id_, ex=True):
        '''
        Returns true if ``id_`` can be edited.

        Args:
            id\\_ (``int``)
                id of an element to check whether is editable

        Returns:
            (``bool``) whether element is editable
        '''
        return self.get_bool(
            lambda res: self.raw_api.GetIsEditable(id_, res),
            error_msg=f'Failed to get is editable for '
                      f'{self.element_context(id_)}',
            ex=ex)

    def set_is_editable(self, id_, bool_, ex=True):
        '''
        TODO: figure out what this does
        '''
        return self.verify_execution(
            self.raw_api.SetIsEditable(id_, bool_),
            error_msg=f'Failed to set is editable for '
                      f'{self.element_context(id_)}',
            ex=ex)

    def get_is_removable(self, id_, ex=True):
        '''
        Returns true if ``id_`` can be removed.

        Args:
            id\\_ (``int``)
                id of an element to check whether is removable

        Returns:
            (``bool``) whether element is removable
        '''
        return self.get_bool(
            lambda res: self.raw_api.GetIsRemoveable(id_, res),
            error_msg=f'Failed to get is removable for '
                      f'{self.element_context(id_)}',
            ex=ex)

    def get_can_add(self, id_, ex=True):
        '''
        Returns true if elements can be added to element at ``id_``

        Args:
            id\\_ (``int``)
                id of an element to check whether elements can be added to it

        Returns:
            (``bool``) whether elements can be added to this element
        '''
        return self.get_bool(
            lambda res: self.raw_api.GetCanAdd(id_, res),
            error_msg=f'Failed to get can add for '
                      f'{self.element_context(id_)}',
            ex=ex)

    def element_type(self, id_, ex=True):
        '''
        Returns the element type of ``id_``

        Args:
            id\\_ (``int``)
                id of element in question

        Returns:
            (``pyxedit.Xelib.ElementTypes``) element type enum value
        '''
        result = self.get_byte(
            lambda res: self.raw_api.ElementType(id_, res),
            error_msg=f'Failed to get element type for '
                      f'{self.element_context(id_)}',
            ex=ex)
        return result if result is None else ElementTypes(result)

    def def_type(self, id_, ex=True):
        '''
        Returns the def type of ``id_``

        Args:
            id\\_ (``int``)
                id of element in question

        Returns:
            (``pyxedit.Xelib.DefTypes``) def type enum value
        '''
        result = self.get_byte(
            lambda res: self.raw_api.DefType(id_, res),
            error_msg=f'Failed to get def type for '
                      f'{self.element_context(id_)}',
            ex=ex)
        return result if result is None else DefTypes(result)

    def smash_type(self, id_, ex=True):
        '''
        Returns the smash type of ``id_``

        Args:
            id\\_ (``int``)
                id of element in question

        Returns:
            (``pyxedit.Xelib.SmashTypes``) smash type enum value
        '''
        result = self.get_byte(
            lambda res: self.raw_api.SmashType(id_, res),
            error_msg=f'Failed to get smash type for '
                      f'{self.element_context(id_)}',
            ex=ex)
        return result if result is None else SmashTypes(result)

    def value_type(self, id_, ex=True):
        '''
        Returns the value type of ``id_``

        Args:
            id\\_ (``int``)
                id of element in question

        Returns:
            (``pyxedit.Xelib.ValueTypes``) value type enum value
        '''
        result = self.get_byte(
            lambda res: self.raw_api.ValueType(id_, res),
            error_msg=f'Failed to get value type for '
                      f'{self.element_context(id_)}',
            ex=ex)
        return result if result is None else ValueTypes(result)

    def is_sorted(self, id_, ex=True):
        '''
        Returns true if ``id_`` is a sorted array

        Args:
            id\\_ (``int``)
                id of element in question

        Returns:
            (``bool``) whether element is sorted array
        '''
        return self.get_bool(
            lambda res: self.raw_api.IsSorted(id_, res),
            error_msg=f'Failed to get is sorted for '
                      f'{self.element_context(id_)}',
            ex=ex)

    def is_fixed(self, id_, ex=True):
        '''
        TODO: figure out what this does
        '''
        return self.get_bool(
            lambda res: self.raw_api.IsFixed(id_, res),
            error_msg=f'Failed to get is fixed for '
                      f'{self.element_context(id_)}',
            ex=ex)

    def is_flags(self, id_, ex=True):
        '''
        Returns true if ``id_`` contains flags

        Args:
            id\\_ (``int``)
                id of element in question

        Returns:
            (``bool``) whether element contains flags
        '''
        return self.value_type(id_, ex=ex) == ValueTypes.Flags

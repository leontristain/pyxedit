from enum import Enum, unique

from pyxedit.xelib.wrapper_methods.base import WrapperMethodsBase


@unique
class ElementTypes(Enum):
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
        return self.get_bool(
            lambda res: self.raw_api.HasElement(id_, path, res),
            error_msg=f'Failed to check if element exists at '
                      f'{self.element_context(id_, path)}',
            ex=ex)

    def get_element(self, id_, path='', ex=False):
        return self.get_handle(
            lambda res: self.raw_api.GetElement(id_, path, res),
            error_msg=f'Failed to get element at '
                      f'{self.element_context(id_, path)}',
            ex=ex)

    def add_element(self, id_, path='', ex=True):
        return self.get_handle(
            lambda res: self.raw_api.AddElement(id_, path, res),
            error_msg=f'Failed to create new element at '
                      f'{self.element_context(id_, path)}',
            ex=ex)

    def add_element_value(self, id_, path, value, ex=True):
        return self.get_handle(
            lambda res: self.raw_api.AddElementValue(id_, path, value, res),
            error_msg=f'Failed to create new element at '
                      f'{self.element_context(id_, path)}, with value: {value}',
            ex=ex)

    def remove_element(self, id_, path='', ex=True):
        return self.verify_execution(
            self.raw_api.RemoveElement(id_, path),
            error_msg=f'Failed to remove element at '
                      f'{self.element_context(id_, path)}',
            ex=ex)

    def remove_element_or_parent(self, id_, ex=True):
        return self.verify_execution(
            self.raw_api.RemoveElementOrParent(id_),
            error_msg=f'Failed to remove element '
                      f'{self.element_context(id_)}',
            ex=ex)

    def set_element(self, id1, id2, ex=True):
        return self.verify_execution(
            self.raw_api.SetElement(id1, id2),
            error_msg=f'Failed to set element at '
                      f'{self.element_context(id2)} to '
                      f'{self.element_context(id1)}',
            ex=ex)

    def get_elements(self, id_=0, path='', sort=False, filter=False, sparse=False, ex=True):
        return self.get_array(
            lambda len_:
                self.raw_api.GetElements(id_, path, sort, filter, sparse, len_),
            error_msg=f'Failed to get child elements at '
                      f'{self.element_context(id_, path)}',
            ex=ex)

    def get_def_names(self, id_, ex=True):
        return self.get_string_array(
            lambda len_: self.raw_api.GetDefNames(id_, len_),
            error_msg=f'Failed to get def names for '
                      f'{self.element_context(id_)}',
            ex=ex)

    def get_add_list(self, id_, ex=True):
        return self.get_string_array(
            lambda len_: self.raw_api.GetAddList(id_, len_),
            error_msg=f'Failed to get add list for {self.element_context(id_)}',
            ex=ex)

    def get_links_to(self, id_, path='', ex=False):
        return self.get_handle(
            lambda res: self.raw_api.GetLinksTo(id_, path, res),
            error_msg=f'Failed to get reference at '
                      f'{self.element_context(id_, path)}',
            ex=ex)

    def set_links_to(self, id_, id2, path='', ex=True):
        return self.verify_execution(
            self.raw_api.SetLinksTo(id_, path, id2),
            error_msg=f'Failed to set reference at '
                      f'{self.element_context(id_, path)}',
            ex=ex)

    def get_container(self, id_, ex=False):
        return self.get_handle(
            lambda res: self.raw_api.GetContainer(id_, res),
            error_msg=f'Failed to get container for '
                      f'{self.element_context(id_)}',
            ex=ex)

    def get_element_file(self, id_, ex=True):
        return self.get_handle(
            lambda res: self.raw_api.GetElementFile(id_, res),
            error_msg=f'Failed to get element file for '
                      f'{self.element_context(id_)}',
            ex=ex)

    def get_element_group(self, id_, ex=True):
        return self.get_handle(
            lambda res: self.raw_api.GetElementGroup(id_, res),
            error_msg=f'Failed to get element group for: '
                      f'{self.element_context(id_)}',
            ex=ex)

    def get_element_record(self, id_, ex=True):
        return self.get_handle(
            lambda res: self.raw_api.GetElementRecord(id_, res),
            error_msg=f'Failed to get element record for: '
                      f'{self.element_context(id_)}',
            ex=ex)

    def element_count(self, id_, ex=True):
        return self.get_integer(
            lambda res: self.raw_api.ElementCount(id_, res),
            error_msg=f'Failed to get element count for '
                      f'{self.element_context(id_)}',
            ex=ex)

    def element_equals(self, id_, id2, ex=True):
        return self.get_bool(
            lambda res: self.raw_api.ElementEquals(id_, id2, res),
            error_msg=f'Failed to check element equality for '
                      f'{self.element_context(id_)} and '
                      f'{self.element_context(id2)}',
            ex=ex)

    def element_matches(self, id_, path, value, ex=True):
        return self.get_bool(
            lambda res: self.raw_api.ElementMatches(id_, path, value, res),
            error_msg=f'Failed to check element matches for '
                      f'{self.element_context(id_, path)},{value}',
            ex=ex)

    def has_array_item(self, id_, path, subpath, value, ex=True):
        return self.get_bool(
            lambda res:
                self.raw_api.HasArrayItem(id_, path, subpath, value, res),
            error_msg=f'Failed to check if array has item for '
                      f'{self.array_item_context(id_, path, subpath, value)}',
            ex=ex)

    def get_array_item(self, id_, path, subpath, value, ex=True):
        return self.get_handle(
            lambda res:
                self.raw_api.GetArrayItem(id_, path, subpath, value, res),
            error_msg=f'Failed to get array item for '
                      f'{self.array_item_context(id_, path, subpath, value)}',
            ex=ex)

    def add_array_item(self, id_, path, subpath, value, ex=True):
        return self.get_handle(
            lambda res:
                self.raw_api.AddArrayItem(id_, path, subpath, value, res),
            error_msg=f'Failed to add array item to '
                      f'{self.array_item_context(id_, path, subpath, value)}',
            ex=ex)

    def remove_array_item(self, id_, path, subpath, value, ex=True):
        return self.verify_execution(
            self.raw_api.RemoveArrayItem(id_, path, subpath, value),
            error_msg=f'Failed to remove array item '
                      f'{self.array_item_context(id_, path, subpath, value)}',
            ex=ex)

    def move_array_item(self, id_, index, ex=True):
        return self.verify_execution(
            self.raw_api.MoveArrayItem(id_, index),
            error_msg=f'Failed to move array item {self.element_context(id_)} '
                      f'to {index}',
            ex=ex)

    def copy_element(self, id_, id2, as_new=False, ex=True):
        return self.get_handle(
            lambda res: self.raw_api.CopyElement(id_, id2, as_new, res),
            error_msg=f'Failed to copy element {self.element_context(id_)} to '
                      f'{id2}',
            ex=ex)

    def find_next_element(self, id_, search, by_path, by_value, ex=True):
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
        return self.get_bool(
            lambda res: self.raw_api.GetSignatureAllowed(id_, signature, res),
            error_msg=f'Failed to check if signature {signature} is allowed on '
                      f'{self.element_context(id_)}',
            ex=ex)

    def get_allowed_signatures(self, id_, ex=True):
        return self.get_string_array(
            lambda len_: self.raw_api.GetAllowedSignatures(id_, len_),
            error_msg=f'Failed to get allowed signatures for '
                      f'{self.element_context(id_)}',
            ex=ex)

    def get_is_modified(self, id_, ex=True):
        return self.get_bool(
            lambda res: self.raw_api.GetIsModified(id_, res),
            error_msg=f'Failed to get is modified for '
                      f'{self.element_context(id_)}',
            ex=ex)

    def get_is_editable(self, id_, ex=True):
        return self.get_bool(
            lambda res: self.raw_api.GetIsEditable(id_, res),
            error_msg=f'Failed to get is editable for '
                      f'{self.element_context(id_)}',
            ex=ex)

    def set_is_editable(self, id_, bool_, ex=True):
        return self.verify_execution(
            self.raw_api.SetIsEditable(id_, bool_),
            error_msg=f'Failed to set is editable for '
                      f'{self.element_context(id_)}',
            ex=ex)

    def get_is_removable(self, id_, ex=True):
        return self.get_bool(
            lambda res: self.raw_api.GetIsRemoveable(id_, res),
            error_msg=f'Failed to get is removable for '
                      f'{self.element_context(id_)}',
            ex=ex)

    def get_can_add(self, id_, ex=True):
        return self.get_bool(
            lambda res: self.raw_api.GetCanAdd(id_, res),
            error_msg=f'Failed to get can add for '
                      f'{self.element_context(id_)}',
            ex=ex)

    def element_type(self, id_, ex=True):
        result = self.get_byte(
            lambda res: self.raw_api.ElementType(id_, res),
            error_msg=f'Failed to get element type for '
                      f'{self.element_context(id_)}',
            ex=ex)
        return result if result is None else ElementTypes(result)

    def def_type(self, id_, ex=True):
        result = self.get_byte(
            lambda res: self.raw_api.DefType(id_, res),
            error_msg=f'Failed to get def type for '
                      f'{self.element_context(id_)}',
            ex=ex)
        return result if result is None else DefTypes(result)

    def smash_type(self, id_, ex=True):
        result = self.get_byte(
            lambda res: self.raw_api.SmashType(id_, res),
            error_msg=f'Failed to get smash type for '
                      f'{self.element_context(id_)}',
            ex=ex)
        return result if result is None else SmashTypes(result)

    def value_type(self, id_, ex=True):
        result = self.get_byte(
            lambda res: self.raw_api.ValueType(id_, res),
            error_msg=f'Failed to get value type for '
                      f'{self.element_context(id_)}',
            ex=ex)
        return result if result is None else ValueTypes(result)

    def is_sorted(self, id_, ex=True):
        return self.get_bool(
            lambda res: self.raw_api.IsSorted(id_, res),
            error_msg=f'Failed to get is sorted for '
                      f'{self.element_context(id_)}',
            ex=ex)

    def is_fixed(self, id_, ex=True):
        return self.get_bool(
            lambda res: self.raw_api.IsFixed(id_, res),
            error_msg=f'Failed to get is fixed for '
                      f'{self.element_context(id_)}',
            ex=ex)

    def is_flags(self, id_, ex=True):
        return self.value_type(id_, ex=ex) == ValueTypes.Flags

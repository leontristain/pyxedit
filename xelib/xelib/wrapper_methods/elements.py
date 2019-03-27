from enum import Enum, unique

from xelib.xelib.wrapper_methods.base import WrapperMethodsBase


@unique
class ElementTypes(Enum):
    etFile = 0
    etMainRecord = 1
    etGroupRecord = 2
    etSubRecord = 3
    etSubRecordStruct = 4
    etSubRecordArray = 5
    etSubRecordUnion = 6
    etArray = 7
    etStruct = 8
    etValue = 9
    etFlag = 10
    etStringListTerminator = 11
    etUnion = 12
    etStructChapter = 13


@unique
class DefTypes(Enum):
    dtRecord = 0
    dtSubRecord = 1
    dtSubRecordArray = 2
    dtSubRecordStruct = 3
    dtSubRecordUnion = 4
    dtString = 5
    dtLString = 6
    dtLenString = 7
    dtByteArray = 8
    dtInteger = 9
    dtIntegerFormater = 10
    dtIntegerFormaterUnion = 11
    dtFlag = 12
    dtFloat = 13
    dtArray = 14
    dtStruct = 15
    dtUnion = 16
    dtEmpty = 17
    dtStructChapter = 18


@unique
class SmashTypes(Enum):
    stUnknown = 0
    stRecord = 1
    stString = 2
    stInteger = 3
    stFlag = 4
    stFloat = 5
    stStruct = 6
    stUnsortedArray = 7
    stUnsortedStructArray = 8
    stSortedArray = 9
    stSortedStructArray = 10
    stByteArray = 11
    stUnion = 12


@unique
class ValueTypes(Enum):
    vtUnknown = 0
    vtBytes = 1
    vtNumber = 2
    vtString = 3
    vtText = 4
    vtReference = 5
    vtFlags = 6
    vtEnum = 7
    vtColor = 8
    vtArray = 9
    vtStruct = 10


class ElementsMethods(WrapperMethodsBase):
    ElementTypes = ElementTypes
    DefTypes = DefTypes
    SmashTypes = SmashTypes
    ValueTypes = ValueTypes

    def has_element(self, id_, path=''):
        return self.get_bool(
            lambda res: self.raw_api.HasElement(id_, path, res),
            error_msg=f'Failed to check if element exists at '
                      f'{self.element_context(id_, path)}')

    def get_element(self, id_, path='', ex=False):
        return self.get_handle(
            lambda res: self.raw_api.GetElement(id_, path, res),
            error_msg=f'Failed to get element at '
                      f'{self.element_context(id_, path)}',
            ex=ex)

    def add_element(self, id_, path=''):
        return self.get_handle(
            lambda res: self.raw_api.AddElement(id_, path, res),
            error_msg=f'Failed to create new element at '
                      f'{self.element_context(id_, path)}')

    def add_element_value(self, id_, path, value):
        return self.get_handle(
            lambda res: self.raw_api.AddElementValue(id_, path, value, res),
            error_msg=f'Failed to create new element at '
                      f'{self.element_context(id_, path)}, with value: {value}')

    def remove_element(self, id_, path='', ex=True):
        return self.verify_execution(
            self.raw_api.RemoveElement(id_, path),
            error_msg=f'Failed to remove element at '
                      f'{self.element_context(id_, path)}',
            ex=ex)

    def remove_element_or_parent(self, id_):
        return self.verify_execution(
            self.raw_api.RemoveElementOrParent(id_),
            error_msg=f'Failed to remove element '
                      f'{self.element_context(id_)}')

    def set_element(self, id1, id2):
        return self.verify_execution(
            self.raw_api.SetElement(id1, id2),
            error_msg=f'Failed to set element at '
                      f'{self.element_context(id2)} to '
                      f'{self.element_context(id1)}')

    def get_elements(self, id_=0, path='', sort=False, filter=False, ex=True):
        return self.get_array(
            lambda len_:
                self.raw_api.GetElements(id_, path, sort, filter, len_),
            error_msg=f'Failed to get child elements at '
                      f'{self.element_context(id_, path)}',
            ex=ex)

    def get_def_names(self, id_):
        return self.get_string_array(
            lambda len_: self.raw_api.GetDefNames(id_, len_),
            error_msg=f'Failed to get def names for '
                      f'{self.element_context(id_)}')

    def get_add_list(self, id_):
        return self.get_string_array(
            lambda len_: self.raw_api.GetAddList(id_, len_),
            error_msg=f'Failed to get add list for {self.element_context(id_)}')

    def get_links_to(self, id_, path='', ex=False):
        return self.get_handle(
            lambda res: self.raw_api.GetLinksTo(id_, path, res),
            error_msg=f'Failed to get reference at '
                      f'{self.element_context(id_, path)}',
            ex=ex)

    def set_links_to(self, id_, id2, path=''):
        return self.verify_execution(
            self.raw_api.SetLinksTo(id_, path, id2),
            error_msg=f'Failed to set reference at '
                      f'{self.element_context(id_, path)}')

    def get_container(self, id_, ex=False):
        return self.get_handle(
            lambda res: self.raw_api.GetContainer(id_, res),
            error_msg=f'Failed to get container for '
                      f'{self.element_context(id_)}',
            ex=ex)

    def get_element_file(self, id_):
        return self.get_handle(
            lambda res: self.raw_api.GetElementFile(id_, res),
            error_msg=f'Failed to get element file for '
                      f'{self.element_context(id_)}')

    def get_element_group(self, id_):
        return self.get_handle(
            lambda res: self.raw_api.GetElementGroup(id_, res),
            error_msg=f'Failed to get element group for: '
                      f'{self.element_context(id_)}')

    def get_element_record(self, id_):
        return self.get_handle(
            lambda res: self.raw_api.GetElementRecord(id_, res),
            error_msg=f'Failed to get element record for: '
                      f'{self.element_context(id_)}')

    def element_count(self, id_, ex=True):
        return self.get_integer(
            lambda res: self.raw_api.ElementCount(id_, res),
            error_msg=f'Failed to get element count for '
                      f'{self.element_context(id_)}',
            ex=ex)

    def element_equals(self, id_, id2):
        return self.get_bool(
            lambda res: self.raw_api.ElementEquals(id_, id2, res),
            error_msg=f'Failed to check element equality for '
                      f'{self.element_context(id_)} and '
                      f'{self.element_context(id2)}')

    def element_matches(self, id_, path, value):
        return self.get_bool(
            lambda res: self.raw_api.ElementMatches(id_, path, value, res),
            error_msg=f'Failed to check element matches for '
                      f'{self.element_context(id_, path)},{value}')

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

    def copy_element(self, id_, id2, as_new=False):
        return self.get_handle(
            lambda res: self.raw_api.CopyElement(id_, id2, as_new, res),
            error_msg=f'Failed to copy element {self.element_context(id_)} to '
                      f'{id2}')

    def find_next_element(self, id_, search, by_path, by_value):
        return self.get_handle(
            lambda res: self.raw_api.FindNextElement(id_,
                                                     search,
                                                     by_path,
                                                     by_value,
                                                     res),
            error_msg=f'Failed to find next element from {id_} via '
                      f'search={search}, by_path={by_path}, '
                      f'by_value={by_value}')

    def find_previous_element(self, id_, search, by_path, by_value):
        return self.get_handle(
            lambda res: self.raw_api.FindPreviousElement(id_,
                                                         search,
                                                         by_path,
                                                         by_value,
                                                         res),
            error_msg=f'Failed to find previous element from {id_} via '
                      f'search={search}, by_path={by_path}, '
                      f'by_value={by_value}')

    def get_signature_allowed(self, id_, signature):
        return self.get_bool(
            lambda res: self.raw_api.GetSignatureAllowed(id_, signature, res),
            error_msg=f'Failed to check if signature {signature} is allowed on '
                      f'{self.element_context(id_)}')

    def get_allowed_signatures(self, id_):
        return self.get_string_array(
            lambda len_: self.raw_api.GetAllowedSignatures(id_, len_),
            error_msg=f'Failed to get allowed signatures for '
                      f'{self.element_context(id_)}')

    def get_is_modified(self, id_):
        return self.get_bool(
            lambda res: self.raw_api.GetIsModified(id_, res),
            error_msg=f'Failed to get is modified for '
                      f'{self.element_context(id_)}')

    def get_is_editable(self, id_):
        return self.get_bool(
            lambda res: self.raw_api.GetIsEditable(id_, res),
            error_msg=f'Failed to get is editable for '
                      f'{self.element_context(id_)}')

    def set_is_editable(self, id_, bool_):
        return self.verify_execution(
            self.raw_api.SetIsEditable(id_, bool_),
            error_msg=f'Failed to set is editable for '
                      f'{self.element_context(id_)}')

    def get_is_removable(self, id_):
        return self.get_bool(
            lambda res: self.raw_api.GetIsRemoveable(id_, res),
            error_msg=f'Failed to get is removable for '
                      f'{self.element_context(id_)}')

    def get_can_add(self, id_):
        return self.get_bool(
            lambda res: self.raw_api.GetCanAdd(id_, res),
            error_msg=f'Failed to get can add for '
                      f'{self.element_context(id_)}')

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

    def is_sorted(self, id_):
        return self.get_bool(
            lambda res: self.raw_api.IsSorted(id_, res),
            error_msg=f'Failed to get is sorted for '
                      f'{self.element_context(id_)}')

    def is_fixed(self, id_):
        return self.get_bool(
            lambda res: self.raw_api.IsFixed(id_, res),
            error_msg=f'Failed to get is fixed for '
                      f'{self.element_context(id_)}')

    def is_flags(self, id_):
        return self.value_type(id_) == ValueTypes.vtFlags

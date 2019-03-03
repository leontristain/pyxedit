from xelib.lib import raw_api
from xelib.helpers import get_handle, validate, get_integer, get_string
from xelib.elements import (element_context,
                            get_element,
                            get_uint_value,
                            set_uint_value,
                            name,
                            get_value,
                            set_value,
                            has_element,
                            add_element,
                            get_flag,
                            set_flag)


# ================
# file value methods
# ================


def get_next_object_id(id_):
    return get_uint_value(id_, 'File Header\\HEDR\\Next Object ID')


def set_next_object_id(id_, next_object_id):
    set_uint_value(id_, 'File Header\\HEDR\\Next Object ID', next_object_id)


def get_file_name(id_):
    return name(id_)


def get_file_author(id_):
    return get_value(id_, 'File Header\\CNAM')


def set_file_author(id_, author):
    return set_value(id_, 'File Header\\CNAM', author)


def get_file_description(id_):
    return get_value(id_, 'File Header\\SNAM')


def set_file_description(id_, description):
    if not has_element(id_, 'File Header\\SNAM'):
        add_element(id_, 'File Header\\SNAM')
    set_value(id_, 'File Header\\SNAM', description)


def get_is_esm(id_):
    return get_flag(id_, 'File Header\\Record Header\\Record Flags', 'ESM')


def set_is_esm(id_, state):
    return set_flag(id_,
                    'File Header\\Record Header\\Record Flags',
                    'ESM',
                    state)


# ================
# file handling methods
# ================


def add_file(file_name):
    return get_handle(lambda res: raw_api.AddFile(file_name, res),
                      error_msg=f'Failed to add new file {file_name}')


def file_by_index(index):
    return get_handle(lambda res: raw_api.FileByIndex(index, res))


def file_by_load_order(load_order):
    return get_handle(lambda res: raw_api.FileByLoadOrder(load_order, res))


def file_by_name(file_name):
    return get_handle(lambda res: raw_api.FileByName(file_name, res))


def file_by_author(author):
    return get_handle(lambda res: raw_api.FileByAuthor(author, res))


def nuke_file(id_):
    validate(raw_api.NukeFile(id_), f'Failed to nuke file: {id_}')


def rename_file(id_, new_file_name):
    validate(raw_api.RenameFile(id_, new_file_name),
             f'Failed to rename file {element_context(id_)} to {new_file_name}')


def save_file(id_, file_path):
    validate(raw_api.SaveFile(id_, file_path),
             f'Failed to save file {element_context(id_)}')


def get_record_count(id_):
    return get_integer(
        lambda res: raw_api.GetRecordCount(id_, res),
        error_msg=f'Failed to get record count for {element_context(id_)}')


def get_override_record_count(id_):
    return get_integer(
        lambda res: raw_api.GetOverrideRecordCount(id_, res),
        error_msg=f'Failed to get override record count for '
                  f'{element_context(id_)}')


def md5_hash(id_):
    return get_string(
        lambda len_: raw_api.MD5Hash(id_, len_),
        error_msg=f'Failed to get MD5 Hash for {element_context(id_)}')


def crc_hash(id_):
    return get_string(
        lambda len_: raw_api.CRCHash(id_, len_),
        error_msg=f'Failed to get CRC Hash for {element_context(id_)}')


def get_file_load_order(id_):
    return get_integer(
        lambda res: raw_api.GetFileLoadOrder(id_, res),
        error_msg=f'Failed to load order for ${element_context(id_)}')


def get_file_header(id_):
    return get_element(id_, 'File Header')


def sort_editor_ids(id_, sig):
    validate(raw_api.SortEditorIDs(id_, sig),
             f'Failed to sort {sig} EditorIDs for: {element_context(id_)}')


def sort_names(id_, sig):
    validate(raw_api.SortNames(id_, sig),
             f'Failed to sort {sig} Names for {element_context(id_)}')


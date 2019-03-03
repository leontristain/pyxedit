from xelib.elements import (get_uint_value,
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
    raise NotImplementedError


def file_by_index(index):
    raise NotImplementedError


def file_by_load_order(load_order):
    raise NotImplementedError


def file_by_name(file_name):
    raise NotImplementedError


def file_by_author(file_name):
    raise NotImplementedError


def nuke_file(id_):
    raise NotImplementedError


def rename_file(id_, new_file_name):
    raise NotImplementedError


def save_file(id_, file_path):
    raise NotImplementedError


def get_record_count(id_):
    raise NotImplementedError


def get_override_record_count(id_):
    raise NotImplementedError


def md5_hash(id_):
    raise NotImplementedError


def get_file_load_order(id_):
    raise NotImplementedError


def get_file_header(id_):
    raise NotImplementedError


def sort_editor_ids(id_, sig):
    raise NotImplementedError


def sort_names(id_, sig):
    raise NotImplementedError


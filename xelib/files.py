
# ================
# file value methods
# ================


def get_next_object_id(id_):
    raise NotImplementedError


def set_next_object_id(id_, next_object_id):
    raise NotImplementedError


def get_file_name(id_):
    raise NotImplementedError


def get_file_author(id_):
    raise NotImplementedError


def set_file_author(id_, author):
    raise NotImplementedError


def get_file_description(id_):
    raise NotImplementedError


def set_file_description(id_, description):
    raise NotImplementedError


def get_is_esm(id_):
    raise NotImplementedError


def set_is_esm(id_):
    raise NotImplementedError


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


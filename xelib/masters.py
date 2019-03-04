from xelib.lib import raw_api
from xelib.helpers import validate, get_array, get_string_array
from xelib.elements import element_context, name, get_loaded_file_names


def clean_masters(id_):
    validate(raw_api.CleanMasters(id_),
             f'Failed to clean masters in: {element_context(id_)}')


def sort_masters(id_):
    validate(raw_api.SortMasters(id_),
             f'Failed to sort masters in: {element_context(id_)}')


def add_master(id_, file_name):
    validate(raw_api.AddMaster(id_, file_name),
             f'Failed to add master {file_name} to file: '
             f'{element_context(id_)}')


def add_required_masters(id_, id2, as_new=False):
    validate(raw_api.AddRequiredMasters(id_, id2, as_new),
             f'Failed to add required masters for {element_context(id_)} to '
             f'file: {element_context(id2)}')


def get_masters(id_):
    return get_array(
        lambda len_: raw_api.GetMasters(id_, len_),
        error_msg=f'Failed to get masters for {element_context(id_)}')


def get_required_by(id_):
    return get_array(
        lambda len_: raw_api.GetRequiredBy(id_, len_),
        error_msg=f'Failed to get required by for {element_context(id_)}')


def get_master_names(id_):
    return get_string_array(
        lambda len_: raw_api.GetMasterNames(id, len_),
        error_msg=f'Failed to get master names for {element_context(id_)}')


def add_all_masters(id_):
    file_name = name(id_)
    for loaded_file_name in get_loaded_file_names():
        if loaded_file_name.endswith('.Hardcoded.dat'):
            continue
        if loaded_file_name == file_name:
            break
        add_master(id_, loaded_file_name)


def get_available_masters(id_):
    file_name = name(id_)
    current_masters = get_master_names(id_)

    available_masters = []
    for loaded_file_name in get_loaded_file_names():
        if loaded_file_name == file_name:
            break
        if loaded_file_name not in current_masters:
            available_masters.append(loaded_file_name)

    return available_masters

from xelib.lib import raw_api
from xelib.helpers import verify_execution
from xelib.elements import name


def filter_record(id_):
    verify_execution(
        raw_api.FilterRecord(id_),
        error_msg=f'Failed to filter record {name(id_)}')


def reset_filter():
    verify_execution(
        raw_api.ResetFilter(),
        error_msg=f'Failed to reset filter')

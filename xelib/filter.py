from xelib.lib import raw_api
from xelib.helpers import validate
from xelib.elements import name


def filter_record(id_):
    validate(raw_api.FilterRecord(id_), f'Failed to filter record {name(id_)}')


def reset_filter():
    validate(raw_api.ResetFilter(), f'Failed to reset filter')

import json

from xelib.lib import raw_api
from xelib.helpers import validate, get_string
from xelib.elements import element_context


def check_for_errors(id_):
    validate(raw_api.CheckForErrors(id_),
             f'Failed to check {element_context(id_)} for errors')


def get_error_thread_done():
    return raw_api.GetErrorThreadDone()


def get_errors():
    return json.loads(get_string(lambda len_: raw_api.GetErrors(len_),
                                 error_msg=f'Failed to get errors'))['errors']


def remove_identical_records(id_, remove_itms=True, remove_itpos=True):
    validate(raw_api.RemoveIdenticalRecords(id_, remove_itms, remove_itpos),
             f'Failed to remove identical errors from {element_context(id_)}')

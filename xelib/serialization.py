import json

from xelib.lib import raw_api
from xelib.helpers import get_string, verify_execution
from xelib.elements import element_context


def element_to_json(id_):
    return get_string(
        lambda len_: raw_api.ElementToJson(id_, len_),
        error_msg=f'Failed to serialize element to JSON: '
                  f'{element_context(id_)}')


def element_to_dict(id_):
    return json.loads(element_to_json(id_))


def element_from_json(id_, path, json):
    verify_execution(
        raw_api.ElementFromJson(id_, path, json),
        error_msg=f'Failed to deserialize element from JSON: '
                  f'{element_context(id_, path)}')


def element_from_dict(id_, path, dict_):
    element_from_json(id_, path, json.dumps(dict_))

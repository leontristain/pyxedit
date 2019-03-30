import json

from xedit.xelib.wrapper_methods.base import WrapperMethodsBase


class SerializationMethods(WrapperMethodsBase):
    def element_to_json(self, id_):
        return self.get_string(
            lambda len_: self.raw_api.ElementToJson(id_, len_),
            error_msg=f'Failed to serialize element to JSON: '
                      f'{self.element_context(id_)}')

    def element_to_dict(self, id_):
        return json.loads(self.element_to_json(id_))

    def element_from_json(self, id_, path, json):
        return self.verify_execution(
            self.raw_api.ElementFromJson(id_, path, json),
            error_msg=f'Failed to deserialize element from JSON: '
                      f'{self.element_context(id_, path)}')

    def element_from_dict(self, id_, path, dict_):
        return self.element_from_json(id_, path, json.dumps(dict_))

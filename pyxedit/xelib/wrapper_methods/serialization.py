import json

from pyxedit.xelib.wrapper_methods.base import WrapperMethodsBase


class SerializationMethods(WrapperMethodsBase):
    def element_to_json(self, id_, ex=True):
        '''
        Serializes an element to JSON

        Args:
            id\\_ (``int``)
                id handle of element to serialize

        Returns:
            (``str``) serialized json
        '''
        return self.get_string(
            lambda len_: self.raw_api.ElementToJson(id_, len_),
            error_msg=f'Failed to serialize element to JSON: '
                      f'{self.element_context(id_)}',
            ex=ex)

    def element_to_dict(self, id_, ex=True):
        '''
        Convert the element data to a dictionary representation

        Args:
            id\\_ (``int``)
                id handle of element to convert to dict
        Returns:
            (``str``) dictionary representation of element data
        '''
        return json.loads(self.element_to_json(id_, ex=ex))

    def element_from_json(self, id_, path, json, ex=True):
        '''
        Creates elements by deserializing JSON in the context of the given
        element at the given subpath.

        Args:
            id\\_ (``int``)
                id handle of element to start from
            path (``str``)
                subpath from the starting element to the element to
                create from JSON
            json (``str``)
                json string containing data of element to add
        '''
        return self.verify_execution(
            self.raw_api.ElementFromJson(id_, path, json),
            error_msg=f'Failed to deserialize element from JSON: '
                      f'{self.element_context(id_, path)}',
            ex=ex)

    def element_from_dict(self, id_, path, dict_, ex=True):
        '''
        Creates elements by loading a dictionary representation in the context
        of the given element at the given subpath.

        Args:
            id\\_ (``int``)
                id handle of element to start from
            path (``str``)
                subpath from the starting element to the element to
                create from dictionary representation
            dict\\_ (``str``)
                dictionary representation containing data of element to add
        '''
        return self.element_from_json(id_, path, json.dumps(dict_), ex=ex)

    def def_to_json(self, id_, ex=True):
        '''
        TODO: figure out what this does
        '''
        return self.get_string(
            lambda len_: self.raw_api.DefToJson(id_, len_),
            error_msg=f'Failed to serialize def to JSON: '
                      f'{self.element_context(id_)}',
            ex=ex)

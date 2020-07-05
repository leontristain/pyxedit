from pyxedit.xelib.wrapper_methods.base import WrapperMethodsBase


class RecordValuesMethods(WrapperMethodsBase):
    def editor_id(self, id_, ex=True):
        '''
        Returns the EditorID of the given record.

        Args:
            id\\_ (``int``)
                id handle of record

        Returns:
            (``str``) EditorID of record
        '''
        return self.get_value(id_, 'EDID', ex=ex)

    def full_name(self, id_, ex=True):
        '''
        Returns the full name of the given record.

        Args:
            id\\_ (``int``)
                id handle of record

        Returns:
            (``str``) Full name of record
        '''
        return self.get_value(id_, 'FULL', ex=ex)

    def get_ref_editor_id(self, id_, path, ex=True):
        '''
        Returns the EditorID of the link target of a reference.

        Args:
            id\\_ (``int``)
                id handle of element to start from
            path (``str``)
                path from the starting element where reference element
                is located at

        Returns:
            (``str``) EditorID of record being referenced by the reference
            element
        '''
        with self.get_links_to(id_, path, ex=ex) as linked:
            return self.editor_id(linked, ex=ex) if linked else ''

    def translate(self, id_, vector, ex=True):
        '''
        Translates the position of a record.

        Args:
            id\\_ (``int``)
                id handle of record to translate
            vector (``Dict[str, float]``)
                a vector in the form of a dictionary containing keys
                ``'X'``, ``'Y'``, ``'Z'`` mapping to float values,
                representing the new position to translate to.
        '''
        position = self.get_element(id_, 'DATA\\Position', ex=ex)
        for coord in ('X', 'Y', 'Z'):
            translate_value = vector.get(coord)
            if translate_value:
                new_value = (self.get_float_value(position, coord, ex=ex) +
                             translate_value)
                self.set_float_value(position, 'X', new_value, ex=ex)

    def rotate(self, id_, vector, ex=True):
        '''
        Rotates the orientation of a record.

        Args:
            id\\_ (``int``)
                id handle of record to rotate
            vector (``Dict[str, float]``)
                a vector in the form of a dictionary containing keys
                ``'X'``, ``'Y'``, ``'Z'`` mapping to float values,
                representing the new direction to rotate to.
        '''
        rotation = self.get_element(id_, 'DATA\\Rotation', ex=ex)
        for coord in ('X', 'Y', 'Z'):
            rotation_value = vector.get(coord)
            if rotation_value:
                new_value = (self.get_float_value(rotation, coord, ex=ex) +
                             rotation_value)
                self.set_float_value(rotation, coord, new_value, ex=ex)

    def get_record_flag(self, id_, name, ex=True):
        '''
        Returns the flag state of a given flag on a record.

        Args:
            id\\_ (``int``)
                id handle of record
            name (``str``)
                name of flag

        Returns:
            (``bool``) the state of given flag on given record
        '''
        return self.get_flag(id_, 'Record Header\\Record Flags', name, ex=ex)

    def set_record_flag(self, id_, name, state, ex=True):
        '''
        Sets the flag state of a given flag on a record.

        Args:
            id\\_ (``int``)
                id handle of record
            name (``str``)
                name of flag
            state (``bool``)
                state of flag to set to
        '''
        self.set_flag(id_, 'Record Header\\Record Flags', name, state, ex=ex)

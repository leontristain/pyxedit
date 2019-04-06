from pyxedit.xelib.wrapper_methods.base import WrapperMethodsBase


class RecordValuesMethods(WrapperMethodsBase):
    def editor_id(self, id_, ex=True):
        return self.get_value(id_, 'EDID', ex=ex)

    def full_name(self, id_, ex=True):
        return self.get_value(id_, 'FULL', ex=ex)

    def get_ref_editor_id(self, id_, path, ex=True):
        with self.get_links_to(id_, path, ex=ex) as linked:
            return self.editor_id(linked, ex=ex) if linked else ''

    def translate(self, id_, vector, ex=True):
        position = self.get_element(id_, 'DATA\\Position', ex=ex)
        for coord in ('X', 'Y', 'Z'):
            translate_value = vector.get(coord)
            if translate_value:
                new_value = (self.get_float_value(position, coord, ex=ex) +
                             translate_value)
                self.set_float_value(position, 'X', new_value, ex=ex)

    def rotate(self, id_, vector, ex=True):
        rotation = self.get_element(id_, 'DATA\\Rotation', ex=ex)
        for coord in ('X', 'Y', 'Z'):
            rotation_value = vector.get(coord)
            if rotation_value:
                new_value = (self.get_float_value(rotation, coord, ex=ex) +
                             rotation_value)
                self.set_float_value(rotation, coord, new_value, ex=ex)

    def get_record_flag(self, id_, name, ex=True):
        return self.get_flag(id_, 'Record Header\\Record Flags', name, ex=ex)

    def set_record_flag(self, id_, name, state, ex=True):
        self.set_flag(id_, 'Record Header\\Record Flags', name, state, ex=ex)

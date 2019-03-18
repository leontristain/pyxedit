from xelib.xelib.wrapper_methods.base import WrapperMethodsBase


class RecordValuesMethods(WrapperMethodsBase):
    def editor_id(self, id_):
        return self.get_value(id_, 'EDID')

    def full_name(self, id_):
        return self.get_value(id_, 'FULL')

    def get_ref_editor_id(self, id_, path):
        with self.get_links_to(id_, path) as linked:
            return self.editor_id(linked) if linked else ''

    def translate(self, id_, vector):
        position = self.get_element(id_, 'DATA\\Position')
        for coord in ('X', 'Y', 'Z'):
            translate_value = vector.get(coord)
            if translate_value:
                new_value = (
                    self.get_float_value(position, coord) + translate_value)
                self.set_float_value(position, 'X', new_value)

    def rotate(self, id_, vector):
        rotation = self.get_element(id_, 'DATA\\Rotation')
        for coord in ('X', 'Y', 'Z'):
            rotation_value = vector.get(coord)
            if rotation_value:
                new_value = (
                    self.get_float_value(rotation, coord) + rotation_value)
                self.set_float_value(rotation, coord, new_value)

    def get_record_flag(self, id_, name):
        return self.get_flag(id_, 'Record Header\\Record Flags', name)

    def set_record_flag(self, id_, name, state):
        self.set_flag(id_, 'Record Header\\Record Flags', name, state)

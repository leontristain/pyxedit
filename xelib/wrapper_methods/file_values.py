from xelib.wrapper_methods.base import WrapperMethodsBase


class FileValuesMethods(WrapperMethodsBase):
    def get_next_object_id(self, id_):
        return self.get_uint_value(id_, 'File Header\\HEDR\\Next Object ID')

    def set_next_object_id(self, id_, next_object_id):
        self.set_uint_value(id_,
                            'File Header\\HEDR\\Next Object ID',
                            next_object_id)

    def get_file_name(self, id_):
        return self.name(id_)

    def get_file_author(self, id_):
        return self.get_value(id_, 'File Header\\CNAM')

    def set_file_author(self, id_, author):
        return self.set_value(id_, 'File Header\\CNAM', author)

    def get_file_description(self, id_):
        return self.get_value(id_, 'File Header\\SNAM')

    def set_file_description(self, id_, description):
        if not self.has_element(id_, 'File Header\\SNAM'):
            self.add_element(id_, 'File Header\\SNAM')
        self.set_value(id_, 'File Header\\SNAM', description)

    def get_is_esm(self, id_):
        return self.get_flag(id_,
                             'File Header\\Record Header\\Record Flags',
                             'ESM')

    def set_is_esm(self, id_, state):
        return self.set_flag(id_,
                             'File Header\\Record Header\\Record Flags',
                             'ESM',
                             state)

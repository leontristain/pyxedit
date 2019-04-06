from pyxedit.xelib.wrapper_methods.base import WrapperMethodsBase


class FileValuesMethods(WrapperMethodsBase):
    def get_next_object_id(self, id_, ex=True):
        return self.get_uint_value(id_,
                                   'File Header\\HEDR\\Next Object ID',
                                   ex=ex)

    def set_next_object_id(self, id_, next_object_id, ex=True):
        self.set_uint_value(id_,
                            'File Header\\HEDR\\Next Object ID',
                            next_object_id,
                            ex=ex)

    def get_file_name(self, id_, ex=True):
        return self.name(id_, ex=ex)

    def get_file_author(self, id_, ex=True):
        return self.get_value(id_, 'File Header\\CNAM', ex=ex)

    def set_file_author(self, id_, author, ex=True):
        return self.set_value(id_, 'File Header\\CNAM', author, ex=ex)

    def get_file_description(self, id_, ex=True):
        return self.get_value(id_, 'File Header\\SNAM', ex=ex)

    def set_file_description(self, id_, description, ex=True):
        if not self.has_element(id_, 'File Header\\SNAM', ex=ex):
            self.add_element(id_, 'File Header\\SNAM', ex=ex)
        self.set_value(id_, 'File Header\\SNAM', description, ex=ex)

    def get_is_esm(self, id_, ex=True):
        return self.get_flag(id_,
                             'File Header\\Record Header\\Record Flags',
                             'ESM',
                             ex=ex)

    def set_is_esm(self, id_, state, ex=True):
        return self.set_flag(id_,
                             'File Header\\Record Header\\Record Flags',
                             'ESM',
                             state,
                             ex=ex)

from pyxedit.xelib.wrapper_methods.base import WrapperMethodsBase


class FileValuesMethods(WrapperMethodsBase):
    def get_next_object_id(self, id_, ex=True):
        '''
        Returns the next object id of file

        Args:
            id\\_ (``int``)
                id handle of file

        Returns:
            (``int``) next object id under ``File Header\\HEDR\\Next Object ID``
            from the file record
        '''
        return self.get_uint_value(id_,
                                   'File Header\\HEDR\\Next Object ID',
                                   ex=ex)

    def set_next_object_id(self, id_, next_object_id, ex=True):
        '''
        Sets the next object id of file

        Args:
            id\\_ (``int``)
                id handle of file
            next_object_id (``int``)
                next object id to set under ``File Header\\HEDR\\Next Object ID``
        '''
        self.set_uint_value(id_,
                            'File Header\\HEDR\\Next Object ID',
                            next_object_id,
                            ex=ex)

    def get_file_name(self, id_, ex=True):
        '''
        Returns the file name of file

        Args:
            id\\_ (``int``)
                id handle of file

        Returns:
            (``str``) name of file
        '''
        return self.name(id_, ex=ex)

    def get_file_author(self, id_, ex=True):
        '''
        Returns the author of file

        Args:
            id\\_ (``int``)
                id handle of file

        Returns:
            (``str``) author of file
        '''
        return self.get_value(id_, 'File Header\\CNAM', ex=ex)

    def set_file_author(self, id_, author, ex=True):
        '''
        Sets the author of file

        Args:
            id\\_ (``int``)
                id handle of file
            author (``str``)
                author to set to
        '''
        return self.set_value(id_, 'File Header\\CNAM', author, ex=ex)

    def get_file_description(self, id_, ex=True):
        '''
        Returns the description of file

        Args:
            id\\_ (``int``)
                id handle of file

        Returns:
            (``str``) description string of file
        '''
        return self.get_value(id_, 'File Header\\SNAM', ex=ex)

    def set_file_description(self, id_, description, ex=True):
        '''
        Sets the description of file

        Args:
            id\\_ (``int``)
                id handle of file
            description (``str``)
                description string to set to
        '''
        if not self.has_element(id_, 'File Header\\SNAM', ex=ex):
            self.add_element(id_, 'File Header\\SNAM', ex=ex)
        self.set_value(id_, 'File Header\\SNAM', description, ex=ex)

    def get_is_esm(self, id_, ex=True):
        '''
        Returns whether the file is flagged as an ESM

        Args:
            id\\_ (``int``)
                id handle of file

        Returns:
            (``bool``) whether file is esm
        '''
        return self.get_flag(id_,
                             'File Header\\Record Header\\Record Flags',
                             'ESM',
                             ex=ex)

    def set_is_esm(self, id_, state, ex=True):
        '''
        Set the ESM flag state for a file

        Args:
            id\\_ (``int``)
                id handle of file
            state (``bool``)
                whether to enable or disable the esm flag for the file
        '''
        return self.set_flag(id_,
                             'File Header\\Record Header\\Record Flags',
                             'ESM',
                             state,
                             ex=ex)

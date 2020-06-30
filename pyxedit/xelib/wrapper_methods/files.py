from pyxedit.xelib.wrapper_methods.base import WrapperMethodsBase


class FilesMethods(WrapperMethodsBase):
    def add_file(self, file_name, ignore_exists=False, ex=True):
        '''
        Creates a new plugin file with the given file name.

        Args:
            file_name (``str``)
                name of plugin file

        Returns:
            (``int``) id handle to newly added file
        '''
        return self.get_handle(
            lambda res: self.raw_api.AddFile(file_name, ignore_exists, res),
            error_msg=f'Failed to add new file {file_name}',
            ex=ex)

    def file_by_index(self, index, ex=True):
        '''
        Returns the plugin file located at the given index

        Args:
            index (``int``)
                index of file to retrieve

        Returns:
            (``int``) id handle of file
        '''
        return self.get_handle(
            lambda res: self.raw_api.FileByIndex(index, res),
            ex=ex)

    def file_by_load_order(self, load_order, ex=True):
        '''
        Returns the plugin file located at the given load order position

        Args:
            load_order (``int``)
                load order position of file to retrieve

        Returns:
            (``int``) id handle of file
        '''
        return self.get_handle(
            lambda res: self.raw_api.FileByLoadOrder(load_order, res),
            ex=ex)

    def file_by_name(self, file_name, ex=True):
        '''
        Returns the plugin file with the given file name

        Args:
            file_name (``str``)
                name of plugin file to retrieve

        Returns:
            (``int``) id handle of file
        '''
        return self.get_handle(
            lambda res: self.raw_api.FileByName(file_name, res),
            ex=ex)

    def file_by_author(self, author, ex=True):
        '''
        Returns the plugin file with the given author

        TODO: what happens if there are multiple such files?

        Args:
            author (``str``)
                author of file to retrieve

        Returns:
            (``int``) id handle of file
        '''
        return self.get_handle(
            lambda res: self.raw_api.FileByAuthor(author, res),
            ex=ex)

    def nuke_file(self, id_, ex=True):
        '''
        Removes all records and groups in the file

        Args:
            id\\_ (``int``)
                id handle of file
        '''
        return self.verify_execution(
            self.raw_api.NukeFile(id_),
            error_msg=f'Failed to nuke file: {id_}',
            ex=ex)

    def rename_file(self, id_, new_file_name, ex=True):
        '''
        Renames file to a new file name

        Args:
            id\\_ (``int``)
                id handle of file
            new_file_name (``str``)
                new name to rename to
        '''
        return self.verify_execution(
            self.raw_api.RenameFile(id_, new_file_name),
            error_msg=f'Failed to rename file {self.element_context(id_)} to '
                      f'{new_file_name}',
            ex=ex)

    def save_file(self, id_, file_path='', ex=True):
        '''
        Save the file at the given filesystem location

        Args:
            id\\_ (``int``)
                id handle of file
            file_path (``str``)
                full filesystem path (including file name) to save to;
                if not provided (or empty string provided), will save the
                file under the game data folder using the file record's file
                name
        '''
        return self.verify_execution(
            self.raw_api.SaveFile(id_, file_path),
            error_msg=f'Failed to save file {self.element_context(id_)}',
            ex=ex)

    def get_record_count(self, id_, ex=True):
        '''
        Returns the number of records in the file

        Args:
            id\\_ (``int``)
                id handle of file

        Returns:
            (``int``) number of records in the file
        '''
        return self.get_integer(
            lambda res: self.raw_api.GetRecordCount(id_, res),
            error_msg=f'Failed to get record count for '
                      f'{self.element_context(id_)}',
            ex=ex)

    def get_override_record_count(self, id_, ex=True):
        '''
        Returns the number of override records in the file

        Args:
            id\\_ (``int``)
                id handle of file

        Returns:
            (``int``) number of override records in the file
        '''
        return self.get_integer(
            lambda res: self.raw_api.GetOverrideRecordCount(id_, res),
            error_msg=f'Failed to get override record count for '
                      f'{self.element_context(id_)}',
            ex=ex)

    def md5_hash(self, id_, ex=True):
        '''
        Returns the md5 hash of the file

        Args:
            id\\_ (``int``)
                id handle of file

        Returns:
            (``str``) md5 hash of file
        '''
        return self.get_string(
            lambda len_: self.raw_api.MD5Hash(id_, len_),
            error_msg=f'Failed to get MD5 Hash for {self.element_context(id_)}',
            ex=ex)

    def crc_hash(self, id_, ex=True):
        '''
        Returns the crc hash of the file

        Args:
            id\\_ (``int``)
                id handle of file

        Returns:
            (``str``) crc hash of file
        '''
        return self.get_string(
            lambda len_: self.raw_api.CRCHash(id_, len_),
            error_msg=f'Failed to get CRC Hash for {self.element_context(id_)}',
            ex=ex)

    def get_file_load_order(self, id_, ex=True):
        '''
        Returns the load order of the file

        Args:
            id\\_ (``int``)
                id handle of file

        Returns:
            (``int``) load order position of file
        '''
        return self.get_integer(
            lambda res: self.raw_api.GetFileLoadOrder(id_, res),
            error_msg=f'Failed to load order for ${self.element_context(id_)}',
            ex=ex)

    def get_file_header(self, id_, ex=True):
        '''
        Returns a handle to the file's file header

        Args:
            id\\_ (``int``)
                id handle of file

        Returns:
            (``int``) id handle to the file's header
        '''
        return self.get_element(id_, 'File Header', ex=ex)

    def sort_editor_ids(self, id_, sig, ex=True):
        '''
        TODO: figure out what this does
        '''
        return self.verify_execution(
            self.raw_api.SortEditorIDs(id_, sig),
            error_msg=f'Failed to sort {sig} EditorIDs for: '
                      f'{self.element_context(id_)}',
            ex=ex)

    def sort_names(self, id_, sig, ex=True):
        '''
        TODO: figure out what this does
        '''
        return self.verify_execution(
            self.raw_api.SortNames(id_, sig),
            error_msg=f'Failed to sort {sig} Names for '
                      f'{self.element_context(id_)}',
            ex=ex)

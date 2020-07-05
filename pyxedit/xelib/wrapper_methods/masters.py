from pyxedit.xelib.wrapper_methods.base import WrapperMethodsBase


class MastersMethods(WrapperMethodsBase):
    def clean_masters(self, id_, ex=True):
        '''
        Remove unnecessary masters from a file

        Args:
            id\\_ (``int``)
                id handle of file
        '''
        return self.verify_execution(
            self.raw_api.CleanMasters(id_),
            error_msg=f'Failed to clean masters in: '
                      f'{self.element_context(id_)}',
            ex=ex)

    def sort_masters(self, id_, ex=True):
        '''
        Orders the masters in given file based on the order in which they are
        loaded

        Args:
            id\\_ (``int``)
                id handle of file
        '''
        return self.verify_execution(
            self.raw_api.SortMasters(id_),
            error_msg=f'Failed to sort masters in: '
                      f'{self.element_context(id_)}',
            ex=ex)

    def add_master(self, id_, file_name, ex=True):
        '''
        Add a master to a file

        Args:
            id\\_ (``int``)
                id handle of file
            file_name (``str``)
                name of master to add
        '''
        return self.verify_execution(
            self.raw_api.AddMaster(id_, file_name),
            error_msg=f'Failed to add master {file_name} to file: '
                      f'{self.element_context(id_)}',
            ex=ex)

    def add_required_masters(self, id_, id2, as_new=False, ex=True):
        '''
        Adds required masters in order to allow for a record copy operation.

        Args:
            id\\_ (``int``)
                id handle of the record to allow copy for
            id2 (``int``)
                id handle of the file serving as copy destination, it is on this
                file that required masters are added
            as_new (``bool``)
                whether the copy is intended to be copied as new record instead
                of copied as override
        '''
        return self.verify_execution(
            self.raw_api.AddRequiredMasters(id_, id2, as_new),
            error_msg=f'Failed to add required masters for '
                      f'{self.element_context(id_)} to file: '
                      f'{self.element_context(id2)}',
            ex=ex)

    def get_masters(self, id_, ex=True):
        '''
        Returns the masters of a given file

        Args:
            id\\_ (``int``)
                id handle of file

        Returns:
            (``List[int]``) a list of id handles of master files
        '''
        return self.get_array(
            lambda len_: self.raw_api.GetMasters(id_, len_),
            error_msg=f'Failed to get masters for {self.element_context(id_)}',
            ex=ex)

    def get_required_by(self, id_, ex=True):
        '''
        Returns all dependents of a given file (files that this file is a
        master of)

        Args:
            id\\_ (``int``)
                id handle of file

        Returns:
            (``List[int]``) a list of id handles of dependents that require it
        '''
        return self.get_array(
            lambda len_: self.raw_api.GetRequiredBy(id_, len_),
            error_msg=f'Failed to get required by for '
                      f'{self.element_context(id_)}',
            ex=ex)

    def get_master_names(self, id_, ex=True):
        '''
        Returns the master names of a given file

        Args:
            id\\_ (``int``)
                id handle of file

        Returns:
            (``List[str]``) a list of master file names
        '''
        return self.get_string_array(
            lambda len_: self.raw_api.GetMasterNames(id_, len_),
            error_msg=f'Failed to get master names for '
                      f'{self.element_context(id_)}',
            ex=ex)

    def add_all_masters(self, id_, ex=True):
        '''
        Adds all files loaded before the given file as its master

        Args:
            id\\_ (``int``)
                id handle of file
        '''
        file_name = self.name(id_, ex=ex)
        for loaded_file_name in self.get_loaded_file_names(ex=ex):
            if loaded_file_name.endswith('.Hardcoded.dat'):
                continue
            if loaded_file_name == file_name:
                break
            self.add_master(id_, loaded_file_name, ex=ex)

    def get_available_masters(self, id_, ex=True):
        '''
        Returns a list of master names that could be masters of a given file
        (i.e. loaded before it), but are not already masters of it.

        Args:
            id\\_ (``int``)
                id handle of file
        '''
        file_name = self.name(id_, ex=ex)
        current_masters = self.get_master_names(id_, ex=ex)

        available_masters = []
        for loaded_file_name in self.get_loaded_file_names(ex=ex):
            if loaded_file_name == file_name:
                break
            if loaded_file_name not in current_masters:
                available_masters.append(loaded_file_name)

        return available_masters

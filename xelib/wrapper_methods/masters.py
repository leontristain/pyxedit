from xelib.wrapper_methods.base import WrapperMethodsBase


class MastersMethods(WrapperMethodsBase):
    def clean_masters(self, id_):
        return self.verify_execution(
            self.raw_api.CleanMasters(id_),
            error_msg=f'Failed to clean masters in: '
                      f'{self.element_context(id_)}')

    def sort_masters(self, id_):
        return self.verify_execution(
            self.raw_api.SortMasters(id_),
            error_msg=f'Failed to sort masters in: '
                      f'{self.element_context(id_)}')

    def add_master(self, id_, file_name):
        return self.verify_execution(
            self.raw_api.AddMaster(id_, file_name),
            error_msg=f'Failed to add master {file_name} to file: '
                      f'{self.element_context(id_)}')

    def add_required_masters(self, id_, id2, as_new=False):
        return self.verify_execution(
            self.raw_api.AddRequiredMasters(id_, id2, as_new),
            error_msg=f'Failed to add required masters for '
                      f'{self.element_context(id_)} to file: '
                      f'{self.element_context(id2)}')

    def get_masters(self, id_):
        return self.get_array(
            lambda len_: self.raw_api.GetMasters(id_, len_),
            error_msg=f'Failed to get masters for {self.element_context(id_)}')

    def get_required_by(self, id_):
        return self.get_array(
            lambda len_: self.raw_api.GetRequiredBy(id_, len_),
            error_msg=f'Failed to get required by for '
                      f'{self.element_context(id_)}')

    def get_master_names(self, id_):
        return self.get_string_array(
            lambda len_: self.raw_api.GetMasterNames(id, len_),
            error_msg=f'Failed to get master names for '
                      f'{self.element_context(id_)}')

    def add_all_masters(self, id_):
        file_name = self.name(id_)
        for loaded_file_name in self.get_loaded_file_names():
            if loaded_file_name.endswith('.Hardcoded.dat'):
                continue
            if loaded_file_name == file_name:
                break
            self.add_master(id_, loaded_file_name)

    def get_available_masters(self, id_):
        file_name = self.name(id_)
        current_masters = self.get_master_names(id_)

        available_masters = []
        for loaded_file_name in self.get_loaded_file_names():
            if loaded_file_name == file_name:
                break
            if loaded_file_name not in current_masters:
                available_masters.append(loaded_file_name)

        return available_masters

from xelib.wrapper_methods.base import WrapperMethodsBase


class FilterMethods(WrapperMethodsBase):
    def filter_record(self, id_):
        self.verify_execution(
            self.raw_api.FilterRecord(id_),
            error_msg=f'Failed to filter record {self.name(id_)}')

    def reset_filter(self):
        self.verify_execution(
            self.raw_api.ResetFilter(),
            error_msg=f'Failed to reset filter')

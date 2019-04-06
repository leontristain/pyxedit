import json

from pyxedit.xelib.wrapper_methods.base import WrapperMethodsBase


class ErrorsMethods(WrapperMethodsBase):
    def check_for_errors(self, id_, ex=True):
        self.verify_execution(
            self.raw_api.CheckForErrors(id_),
            error_msg=f'Failed to check {self.element_context(id_)} for errors',
            ex=ex)

    def get_error_thread_done(self):
        return self.raw_api.GetErrorThreadDone()

    def get_errors(self, ex=True):
        return json.loads(
            self.get_string(
                lambda len_: self.raw_api.GetErrors(len_),
                error_msg=f'Failed to get errors',
                ex=ex))['errors']

    def remove_identical_records(self,
                                 id_,
                                 remove_itms=True,
                                 remove_itpos=True,
                                 ex=True):
        self.verify_execution(
            self.raw_api.RemoveIdenticalRecords(id_, remove_itms, remove_itpos),
            error_msg=f'Failed to remove identical errors from '
                      f'{self.element_context(id_)}',
            ex=ex)

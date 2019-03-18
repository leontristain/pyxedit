from xelib.xelib.wrapper_methods.base import WrapperMethodsBase


class MessagesMethods(WrapperMethodsBase):
    def get_messages(self):
        return self.get_string(
            lambda len_: self.raw_api.GetMessagesLength(len_),
            method=self.raw_api.GetMessages,
            ex=False)

    def clear_messages(self):
        self.raw_api.ClearMessages()

    def get_exception_message(self):
        return self.get_string(
            lambda len_: self.raw_api.GetExceptionMessageLength(len_),
            method=self.raw_api.GetExceptionMessage,
            ex=False)

    def get_exception_stack(self):
        return self.get_string(
            lambda len_: self.raw_api.GetExceptionStackLength(len_),
            method=self.raw_api.GetExceptionStack,
            ex=False)

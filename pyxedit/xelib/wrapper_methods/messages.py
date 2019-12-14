from pyxedit.xelib.wrapper_methods.base import WrapperMethodsBase


class MessagesMethods(WrapperMethodsBase):
    def get_messages(self, ex=False):
        '''
        Gets any messages that have been added to ``XEditLib.dll``'s internal
        log since the last time this method was called.

        Returns:
            ``(str)`` New ``XEditLib.dll`` log messages since the last call
            of this method
        '''
        return self.get_string(
            lambda len_: self.raw_api.GetMessagesLength(len_),
            method=self.raw_api.GetMessages,
            ex=ex)

    def clear_messages(self):
        '''
        Clears all messages from ``XEditLib.dll``'s internal log.
        '''
        self.raw_api.ClearMessages()

    def get_exception_message(self, ex=False):
        '''
        Returns the error message of the last ``XEditLib.dll`` exception that
        occurred. If no exception has occurred since the last time this method
        was invoked, an empty string will be returned.

        .. warning::
            Users of this ``Xelib`` API should never need to call this method,
            since in cases where ``ex=True`` is used in a method call, any
            resulting exceptions in python should automatically contain this
            error message.

        Returns:
            ``(str)`` Error message of the last ``XEditLib.dll`` exception
            since the last call of this method.
        '''
        return self.get_string(
            lambda len_: self.raw_api.GetExceptionMessageLength(len_),
            method=self.raw_api.GetExceptionMessage,
            ex=ex)

    def get_exception_stack(self, ex=False):
        '''
        Returns the exception stacktrace of the last ``XEditLib.dll`` exception
        that occurred.

        .. warning::
            Users of this ``Xelib`` API should never need to call this method,
            since in cases where ``ex=True`` is used in a method call, any
            resulting exceptions in python should automatically contain this
            stack trace.

        Returns:
            ``(str)`` Stack trace of the last ``XEditLib.dll`` exception
            since the last call of this method.
        '''
        return self.get_string(
            lambda len_: self.raw_api.GetExceptionStackLength(len_),
            method=self.raw_api.GetExceptionStack,
            ex=ex)

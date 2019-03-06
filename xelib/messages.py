from xelib.lib import raw_api
from xelib.helpers import get_string


def get_messages():
    return get_string(
        lambda len_: raw_api.GetMessagesLength(len_),
        method=raw_api.GetMessages)


def clear_messages():
    raw_api.ClearMessages()


def get_exception_message():
    return get_string(
        lambda len_: raw_api.GetExceptionMessageLength(len_),
        method=raw_api.GetExceptionMessage)


def get_exception_stack():
    return get_string(
        lambda len_: raw_api.GetExceptionStackLength(len_),
        method=raw_api.GetExceptionStack)

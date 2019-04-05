from enum import Enum


class XEditTypes(Enum):
    Ref = 1
    Value = 2
    Container = 3


class XEditError(Exception):
    '''
    Exception class to raise for xedit-related errors
    '''
    pass

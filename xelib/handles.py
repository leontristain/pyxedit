from collections.abc import Iterable
from contextlib import contextmanager

from xelib.meta import release
from xelib.helpers import XelibError


def release_handles(handles):
    if isinstance(handles, int):
        release(handles)
    elif isinstance(handles, Iterable):
        for handle in handles:
            if isinstance(handle, int):
                release(handle)
            else:
                raise XelibError(f'tried to release handle {handle}; this '
                                 f'is not a valid handle id since it is '
                                 f'not an integer')
    else:
        raise XelibError(f'tried to release item {handle}; this is neither '
                         f'a single handle (should be an int) nor a list '
                         f'of handles (should be a list of int); thus this '
                         f'is not valid input')


@contextmanager
def manage(handles):
    '''
    Generic handle manager. Handles may be passed into the context, where
    handles will be freed on context exit.

    @param handles: handles, can be a single handle or a list of handles
    '''
    try:
        yield handles
    finally:
        release_handles(handles)


def handle_managed(callback):
    '''
    A decorator that can be slapped onto functions that returns a handle or
    list of handles, that turns the function into a context manager that yields
    those handles, that will release the handles after the context.
    '''
    @contextmanager
    def context_manager(*args, **kwargs):
        handles = callback(*args, **kwargs)
        try:
            yield handles
        finally:
            release_handles(handles)
    return context_manager

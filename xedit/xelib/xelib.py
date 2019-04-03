import ctypes
from contextlib import contextmanager
from ctypes import wintypes
from itertools import tee
from pathlib import Path

from xedit.xelib.definitions import DelphiTypes, XEditLibSignatures
from xedit.xelib.wrapper_methods.element_values import ElementValuesMethods
from xedit.xelib.wrapper_methods.elements import ElementsMethods
from xedit.xelib.wrapper_methods.errors import ErrorsMethods
from xedit.xelib.wrapper_methods.file_values import FileValuesMethods
from xedit.xelib.wrapper_methods.files import FilesMethods
from xedit.xelib.wrapper_methods.filter import FilterMethods
from xedit.xelib.wrapper_methods.groups import GroupsMethods
from xedit.xelib.wrapper_methods.helpers import HelpersMethods, XelibError
from xedit.xelib.wrapper_methods.masters import MastersMethods
from xedit.xelib.wrapper_methods.messages import MessagesMethods
from xedit.xelib.wrapper_methods.meta import MetaMethods
from xedit.xelib.wrapper_methods.record_values import RecordValuesMethods
from xedit.xelib.wrapper_methods.records import RecordsMethods
from xedit.xelib.wrapper_methods.resources import ResourcesMethods
from xedit.xelib.wrapper_methods.serialization import SerializationMethods
from xedit.xelib.wrapper_methods.setup import SetupMethods

__all__ = ['DLL_PATH', 'Xelib', 'XelibError']

DLL_PATH = Path(__file__).parent / '../../XEditLib/XEditLib.dll'


def pairwise(iterable):
    '''
    A pairwise iterator, copied from:
        https://docs.python.org/3/library/itertools.html
    '''
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


class Xelib(ElementValuesMethods,
            ElementsMethods,
            ErrorsMethods,
            FileValuesMethods,
            FilesMethods,
            FilterMethods,
            GroupsMethods,
            HelpersMethods,
            MastersMethods,
            MessagesMethods,
            MetaMethods,
            RecordValuesMethods,
            RecordsMethods,
            ResourcesMethods,
            SerializationMethods,
            SetupMethods):
    '''
    Xelib class
    '''
    def __init__(self):
        self.dll_path = DLL_PATH
        self._raw_api = None
        self._handles_stack = []
        self._current_handles = set()

    def __enter__(self):
        if not self._raw_api:
            self._raw_api = self.load_lib(self.dll_path)
            self.initialize()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self._raw_api:
            self.release_handles()
            self.finalize()
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel32.FreeLibrary.argtypes = [wintypes.HMODULE]
            kernel32.FreeLibrary(self._raw_api._handle)
            self._raw_api = None

    @property
    def loaded(self):
        return bool(self._raw_api)

    @property
    def opened_handles(self):
        opened_handles = set()
        for handles in self._handles_stack:
            opened_handles.update(handles)
        opened_handles.update(self._current_handles)
        return opened_handles

    def track_handle(self, handle):
        self._current_handles.add(handle)

    def release_handle(self, handle):
        found_layers = [
            layer for layer in self._handles_stack + [self._current_handles]
            if handle in layer]
        if found_layers:
            for layer in found_layers:
                layer.remove(handle)
            try:
                self.release(handle)
            except XelibError:
                pass

    def release_handles(self):
        while self._current_handles:
            try:
                self.release(self._current_handles.pop())
            except XelibError:
                pass

    @contextmanager
    def manage_handles(self):
        try:
            self._handles_stack.append(self._current_handles)
            self._current_handles = set()
            yield
        finally:
            self.release_handles()
            self._current_handles = self._handles_stack.pop()

    def print_handle_management_stack(self):
        for i, handles in enumerate(self._handles_stack):
            print(f'{i}: {handles}')
        print(f'{len(self._handles_stack)}: {self._current_handles}')

    def promote_handle(self, handle):
        full_stack = self._handles_stack + [self._current_handles]
        for (current_handles,
             parent_scope_handles) in pairwise(reversed(full_stack)):
            if handle in current_handles:
                current_handles.remove(handle)
                parent_scope_handles.add(handle)
                return parent_scope_handles

        print(f'failed to promote handle {handle}')

    @property
    def raw_api(self):
        if not self._raw_api:
            raise XelibError(f'Must use Xelib within its own context; the '
                             f'code should look something like: `with xelib '
                             f'as xelib: xelib.do_something`')
        return self._raw_api

    @staticmethod
    def load_lib(dll_path):
        lib = ctypes.CDLL(str(dll_path))
        types_mapping = {mapping.name: mapping.value for mapping in DelphiTypes}
        for signature in XEditLibSignatures:
            method_name = signature.name
            params, return_type = signature.value
            try:
                method = getattr(lib, method_name)
                method.argtypes = [types_mapping[delphi_type]
                                   for _, delphi_type in params.items()]
                if return_type:
                    method.restype = types_mapping[return_type]
            except AttributeError:
                print(f'WARNING: missing function {method_name}')
        return lib

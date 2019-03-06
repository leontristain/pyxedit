import ctypes
from ctypes import wintypes
from pathlib import Path

from xelib.definitions import DelphiTypes, XEditLibSignatures
from xelib.wrapper_methods.element_values import ElementValuesMethods
from xelib.wrapper_methods.elements import ElementsMethods
from xelib.wrapper_methods.errors import ErrorsMethods
from xelib.wrapper_methods.file_values import FileValuesMethods
from xelib.wrapper_methods.files import FilesMethods
from xelib.wrapper_methods.filter import FilterMethods
from xelib.wrapper_methods.groups import GroupsMethods
from xelib.wrapper_methods.helpers import HelpersMethods, XelibError
from xelib.wrapper_methods.masters import MastersMethods
from xelib.wrapper_methods.messages import MessagesMethods
from xelib.wrapper_methods.meta import MetaMethods
from xelib.wrapper_methods.record_values import RecordValuesMethods
from xelib.wrapper_methods.records import RecordsMethods
from xelib.wrapper_methods.resources import ResourcesMethods
from xelib.wrapper_methods.serialization import SerializationMethods
from xelib.wrapper_methods.setup import SetupMethods

__all__ = ['DLL_PATH', 'Xelib', 'XelibError']

DLL_PATH = Path(__file__).parent / '../XEditLib/XEditLib.dll'


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

    def __init__(self):
        self.dll_path = DLL_PATH
        self._raw_api = None

    def __enter__(self):
        if not self._raw_api:
            self._raw_api = self.load_lib(self.dll_path)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self._raw_api:
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel32.FreeLibrary.argtypes = [wintypes.HMODULE]
            kernel32.FreeLibrary(self._raw_api._handle)
            self._raw_api = None

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

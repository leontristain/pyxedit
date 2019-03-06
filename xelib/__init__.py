import ctypes
from ctypes import wintypes
from pathlib import Path

from xelib.definitions import DelphiTypes, XEditLibSignatures
from xelib.setup import get_game_path, set_game_path, set_game_mode


DLL_PATH = Path(__file__).parent / '../XEditLib/XEditLib.dll'


class Xelib:
    def __init__(self):
        self.dll_path = DLL_PATH
        self.raw_api = None

    def __enter__(self):
        self.raw_api = self.load_lib()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.raw_api:
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel32.FreeLibrary.argtypes = [wintypes.HMODULE]
            kernel32.FreeLibrary(self.raw_api._handle)
            self.raw_api

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


def test():
    set_game_mode()
    set_game_path('D:\\SteamLibrary\\steamapps\\common\\Skyrim Special Edition\\')
    print(get_game_path())

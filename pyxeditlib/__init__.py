from pathlib import Path
import ctypes

from . import loader

DLL_PATH = Path(__file__).parent / '../XEditLib/XEditLib.dll'
lib = loader.load_lib(DLL_PATH)

def get_string(callback, method=lib.GetResultString):
    len_ = ctypes.c_long(0)
    callback(ctypes.byref(len_))
    if len_.value < 1:
        return ''
    buffer = ctypes.create_unicode_buffer(len_.value)
    result = method(buffer, len_)
    print(result)
    if result:
        return buffer.value

def set_game_path(game_path):
    return lib.SetGamePath(game_path)

def get_game_path(game_mode=4):
    def callback(len):
        lib.GetGamePath(game_mode, len)
    return get_string(callback)

def set_game_mode(game_mode=4):
    return lib.SetGameMode(game_mode)

def test():
    set_game_mode()
    set_game_path('D:\\SteamLibrary\\steamapps\\common\\Skyrim Special Edition\\')
    print(get_game_path())

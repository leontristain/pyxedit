from xelib.lib import raw_api
from xelib.helpers import get_string
from xelib.setup import get_game_path, set_game_path, set_game_mode


def test():
    set_game_mode()
    set_game_path('D:\\SteamLibrary\\steamapps\\common\\Skyrim Special Edition\\')
    print(get_game_path())

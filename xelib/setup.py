from collections import namedtuple
from enum import Enum, unique

from xelib.lib import raw_api
from xelib.helpers import (element_context,
                           get_byte,
                           get_handle,
                           get_string,
                           validate)

GameInfo = namedtuple('GameInfo', 'name short_name mode exe_name')


@unique
class Games(Enum):
    FalloutNV = GameInfo('Fallout NV', 'FalloutNV', 0, 'FalloutNV.exe')
    Fallout3 = GameInfo('Fallout 3', 'Fallout3', 1, 'Fallout3.exe')
    Oblivion = GameInfo('Oblivion', 'Oblivion', 2, 'Oblivion.exe')
    Skyrim = GameInfo('Skyrim', 'Skyrim', 3, 'TESV.exe')
    SkyrimSE = GameInfo('Skyrim SE', 'Skyrim', 4, 'SkyrimSE.exe')
    Fallout4 = GameInfo('Fallout 4', 'Fallout4', 5, 'Fallout4.exe')


def get_game_path(game=Games.SkyrimSE):
    return get_string(
        lambda len_: raw_api.GetGamePath(game.value.mode, len_),
        error_msg=f'GetGamePath failed for game {game}; mode {game.value.mode}')


def set_game_path(path):
    validate(raw_api.SetGamePath(path), f'Failed to SetGamePath to {path}')


def get_game_language(game=Games.SkyrimSE):
    return get_string(
        lambda len_: raw_api.GetGameLanguage(game.value.mode, len_),
        error_msg=f'GetGameLanguage failed for game {game}; mode '
                  f'{game.value.mode}') or 'English'


def set_language(language):
    validate(raw_api.SetLanguage(language),
             f'Failed to SetLanguage to {language}')


def set_game_mode(game=Games.SkyrimSE):
    validate(raw_api.SetGameMode(game.value.mode),
             f'Failed to SetGameMode to game {game}; mode {game.value.mode}')


def get_load_order():
    return get_string(lambda len_: raw_api.GetLoadOrder(len_),
                      error_msg=f'GetLoadOrder failed')


def get_active_plugins():
    return get_string(lambda len_: raw_api.GetActivePlugins(len_),
                      error_msg=f'GetActivePlugins failed')


def load_plugins(load_order, smart_load=True):
    validate(raw_api.Load_plugins(load_order, smart_load),
             f'Failed to LoadPlugins given load_order {repr(load_order)} and '
             f'smart_load={smart_load}')


def load_plugin(file_name):
    validate(raw_api.LoadPlugin(file_name), f'Failed to load {file_name}')


def load_plugin_header(file_name):
    return get_handle(
        lambda res: raw_api.LoadPluginHeader(file_name, res),
        error_msg=f'Failed to load plugin header for {file_name}')


def build_references(id_, sync=True):
    validate(raw_api.BuildReferences(id_, sync),
             f'Failed to build references for {element_context(id_)}')


def unload_plugin(id_):
    validate(raw_api.UnloadPlugin(id_),
             f'Failed to unload plugin {element_context(id_)}')


def get_loader_status():
    return get_byte(
        lambda res: raw_api.GetLoaderStatus(res),
        error_msg=f'Failed to get loader status')


def get_loaded_file_names(exclude_hardcoded=True):
    pass

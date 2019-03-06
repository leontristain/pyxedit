from collections import namedtuple
from enum import Enum, unique

from xelib.wrapper_methods.base import WrapperMethodsBase


GameInfo = namedtuple('GameInfo', 'name short_name mode exe_name')


@unique
class Games(Enum):
    FalloutNV = GameInfo('Fallout NV', 'FalloutNV', 0, 'FalloutNV.exe')
    Fallout3 = GameInfo('Fallout 3', 'Fallout3', 1, 'Fallout3.exe')
    Oblivion = GameInfo('Oblivion', 'Oblivion', 2, 'Oblivion.exe')
    Skyrim = GameInfo('Skyrim', 'Skyrim', 3, 'TESV.exe')
    SkyrimSE = GameInfo('Skyrim SE', 'Skyrim', 4, 'SkyrimSE.exe')
    Fallout4 = GameInfo('Fallout 4', 'Fallout4', 5, 'Fallout4.exe')


class SetupMethods(WrapperMethodsBase):
    GameInfo = GameInfo
    Games = Games

    def get_game_path(self, game=None):
        game = game or self.Games.SkyrimSE
        return self.get_string(
            lambda len_: self.raw_api.GetGamePath(game.value.mode, len_),
            error_msg=f'GetGamePath failed for game {game}; mode '
                      f'{game.value.mode}')

    def set_game_path(self, path):
        self.verify_execution(
            self.raw_api.SetGamePath(path),
            error_msg=f'Failed to SetGamePath to {path}')

    def get_game_language(self, game=None):
        game = game or self.Games.SkyrimSE
        return self.get_string(
            lambda len_: self.raw_api.GetGameLanguage(game.value.mode, len_),
            error_msg=f'GetGameLanguage failed for game {game}; mode '
                      f'{game.value.mode}') or 'English'

    def set_language(self, language):
        self.verify_execution(
            self.raw_api.SetLanguage(language),
            error_msg=f'Failed to SetLanguage to {language}')

    def set_game_mode(self, game=None):
        game = game or self.Games.SkyrimSE
        self.verify_execution(
            self.raw_api.SetGameMode(game.value.mode),
            error_msg=f'Failed to SetGameMode to game {game}; mode '
                      f'{game.value.mode}')

    def get_load_order(self):
        return self.get_string(
            lambda len_: self.raw_api.GetLoadOrder(len_),
            error_msg=f'GetLoadOrder failed')

    def get_active_plugins(self):
        return self.get_string(
            lambda len_: self.raw_api.GetActivePlugins(len_),
            error_msg=f'GetActivePlugins failed')

    def load_plugins(self, load_order, smart_load=True):
        self.verify_execution(
            self.raw_api.Load_plugins(load_order, smart_load),
            error_msg=f'Failed to LoadPlugins given load_order '
                      f'{repr(load_order)} and smart_load={smart_load}')

    def load_plugin(self, file_name):
        self.verify_execution(
            self.raw_api.LoadPlugin(file_name),
            error_msg=f'Failed to load {file_name}')

    def load_plugin_header(self, file_name):
        return self.get_handle(
            lambda res: self.raw_api.LoadPluginHeader(file_name, res),
            error_msg=f'Failed to load plugin header for {file_name}')

    def build_references(self, id_, sync=True):
        self.verify_execution(
            self.raw_api.BuildReferences(id_, sync),
            error_msg=f'Failed to build references for '
                      f'{self.element_context(id_)}')

    def unload_plugin(self, id_):
        self.verify_execution(
            self.raw_api.UnloadPlugin(id_),
            error_msg=f'Failed to unload plugin {self.element_context(id_)}')

    def get_loader_status(self):
        return self.get_byte(
            lambda res: self.raw_api.GetLoaderStatus(res),
            error_msg=f'Failed to get loader status')

    def get_loaded_file_names(self, exclude_hardcoded=True):
        with self.get_elements() as elements:
            file_names = []
            for file_ in elements:
                file_name = self.name(file_)
                if exclude_hardcoded and file_name.endswith('.Hardcoded.dat'):
                    continue
                file_names.append(file_name)
            return file_names

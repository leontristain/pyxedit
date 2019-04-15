from enum import Enum, unique

from pyxedit.xelib.wrapper_methods.base import WrapperMethodsBase


@unique
class LoaderStates(Enum):
    lsInactive = 0
    lsActive = 1
    lsDone = 2
    lsError = 3


@unique
class GameModes(Enum):
    gmFNV = 0
    gmFO3 = 1
    gmTES4 = 2
    gmTES5 = 3
    gmSSE = 4
    gmFO4 = 5


class SetupMethods(WrapperMethodsBase):
    LoaderStates = LoaderStates
    GameModes = GameModes

    def get_game_path(self, game=None, ex=True):
        game = game or self.GameModes.gmSSE
        return self.get_string(
            lambda len_: self.raw_api.GetGamePath(game.value, len_),
            error_msg=f'GetGamePath failed for game {game}; mode '
                      f'{game.value}',
            ex=ex)

    def set_game_path(self, path, ex=True):
        return self.verify_execution(
            self.raw_api.SetGamePath(path),
            error_msg=f'Failed to SetGamePath to {path}',
            ex=ex)

    def get_game_language(self, game=None, ex=True):
        game = game or self.GameModes.gmSSE
        return self.get_string(
            lambda len_: self.raw_api.GetGameLanguage(game.value, len_),
            error_msg=f'GetGameLanguage failed for game {game}; mode '
                      f'{game.value}',
            ex=ex) or 'English'

    def set_language(self, language, ex=True):
        return self.verify_execution(
            self.raw_api.SetLanguage(language),
            error_msg=f'Failed to SetLanguage to {language}',
            ex=ex)

    def set_game_mode(self, game=None, ex=True):
        game = game or self.GameModes.gmSSE
        return self.verify_execution(
            self.raw_api.SetGameMode(game.value),
            error_msg=f'Failed to SetGameMode to game {game}; mode '
                      f'{game.value}',
            ex=ex)

    def get_load_order(self, ex=True):
        return self.get_string(
            lambda len_: self.raw_api.GetLoadOrder(len_),
            error_msg=f'GetLoadOrder failed',
            ex=ex)

    def get_active_plugins(self, ex=True):
        return self.get_string(
            lambda len_: self.raw_api.GetActivePlugins(len_),
            error_msg=f'GetActivePlugins failed',
            ex=ex)

    def load_plugins(self, load_order, smart_load=True, ex=True):
        return self.verify_execution(
            self.raw_api.LoadPlugins(load_order, smart_load),
            error_msg=f'Failed to LoadPlugins given load_order '
                      f'{repr(load_order)} and smart_load={smart_load}',
            ex=ex)

    def load_plugin(self, file_name, ex=True):
        return self.verify_execution(
            self.raw_api.LoadPlugin(file_name),
            error_msg=f'Failed to load {file_name}',
            ex=ex)

    def load_plugin_header(self, file_name, ex=True):
        return self.get_handle(
            lambda res: self.raw_api.LoadPluginHeader(file_name, res),
            error_msg=f'Failed to load plugin header for {file_name}',
            ex=ex)

    def build_references(self, id_, sync=True, ex=True):
        return self.verify_execution(
            self.raw_api.BuildReferences(id_, sync),
            error_msg=f'Failed to build references for '
                      f'{self.element_context(id_)}',
            ex=ex)

    def unload_plugin(self, id_, ex=True):
        return self.verify_execution(
            self.raw_api.UnloadPlugin(id_),
            error_msg=f'Failed to unload plugin {self.element_context(id_)}',
            ex=ex)

    def get_loader_status(self, ex=True):
        return LoaderStates(self.get_byte(
            lambda res: self.raw_api.GetLoaderStatus(res),
            error_msg=f'Failed to get loader status',
            ex=ex))

    def get_loaded_file_names(self, exclude_hardcoded=True, ex=True):
        file_names = []
        for file_ in self.get_elements(ex=ex):
            file_name = self.name(file_, ex=ex)
            if exclude_hardcoded and file_name.endswith('.Hardcoded.dat'):
                continue
            file_names.append(file_name)
        return file_names

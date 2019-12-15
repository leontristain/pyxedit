from enum import Enum, unique

from pyxedit.xelib.wrapper_methods.base import WrapperMethodsBase


@unique
class LoaderStates(Enum):
    Inactive = 0
    Active = 1
    Done = 2
    Error = 3


@unique
class GameModes(Enum):
    FNV = 0
    FO3 = 1
    TES4 = 2
    TES5 = 3
    SSE = 4
    FO4 = 5


class SetupMethods(WrapperMethodsBase):
    LoaderStates = LoaderStates
    GameModes = GameModes

    def get_game_path(self, game=None, ex=True):
        '''
        Retrieves the path to the given game, as discovered or understood by
        ``XEditLib.dll``. The path is the top-level directory of the installed
        game (e.g. ``D:\\SteamLibrary\\steamapps\\common\\Skyrim Special Edition\\``).
        ``XEditLib.dll`` will look at the registry to discover the path to the
        specified game if needed.

        Args:
            game (``Xelib.GameModes``):
                The game to retrieve the game path for.

        Returns:
            (``str``) the path to the game
        '''
        game = game or self.GameModes.SSE
        return self.get_string(
            lambda len_: self.raw_api.GetGamePath(game.value, len_),
            error_msg=f'GetGamePath failed for game {game}; mode '
                      f'{game.value}',
            ex=ex)

    def set_game_path(self, path, ex=True):
        '''
        Configures ``XEditLib.dll`` to use the given value as the game path.
        The provided path should be the top-level directory of the installed
        game (e.g.
        ``D:\\SteamLibrary\\steamapps\\common\\Skyrim Special Edition\\``).

        This path will be used when loading plugins and resource files.

        Args:
            path (``str``): the path to the game
        '''
        return self.verify_execution(
            self.raw_api.SetGamePath(path),
            error_msg=f'Failed to SetGamePath to {path}',
            ex=ex)

    def get_game_language(self, game=None, ex=True):
        '''
        Retrieves the language used for a given game, as understood by
        ``XEditLib.dll``

        Args:
            game (``Xelib.GameModes``):
                The game to retrieve the language for.

        Returns:
            (``str``) the language used for the game
        '''
        game = game or self.GameModes.SSE
        return self.get_string(
            lambda len_: self.raw_api.GetGameLanguage(game.value, len_),
            error_msg=f'GetGameLanguage failed for game {game}; mode '
                      f'{game.value}',
            ex=ex) or 'English'

    def set_language(self, language, ex=True):
        '''
        Configures the language to be used by ``XEditLib.dll`` when loading
        string files.

        Args:
            language (``str``):
                the language to use
        '''
        return self.verify_execution(
            self.raw_api.SetLanguage(language),
            error_msg=f'Failed to SetLanguage to {language}',
            ex=ex)

    def set_game_mode(self, game=None, ex=True):
        '''
        Configures the game mode for ``XEditLib.dll``.

        Args:
            game (``Xelib.GameModes``):
                The game to retrieve the language for.
        '''
        game = game or self.GameModes.SSE
        return self.verify_execution(
            self.raw_api.SetGameMode(game.value),
            error_msg=f'Failed to SetGameMode to game {game}; mode '
                      f'{game.value}',
            ex=ex)

    def get_load_order(self, ex=True):
        '''
        Returns the user's load order as determined by ``XEditLib.dll`` from
        ``loadorder.txt``, ``plugins.txt``, or plugin dates, depending on
        game and available files. The load order is returned as a list of
        filenames separated by ``\\r\\n``.

        Returns:
            (``str``) the load order in a string form
        '''
        return self.get_string(
            lambda len_: self.raw_api.GetLoadOrder(len_),
            error_msg=f'GetLoadOrder failed',
            ex=ex)

    def get_active_plugins(self, ex=True):
        '''
        Returns the user's active plugins as determined from ``plugins.txt``.
        Active plugins are returned as a list of filenames separated by
        ``\\r\\n``.

        Returns:
            (``str``) the active plugins list in a string form
        '''
        return self.get_string(
            lambda len_: self.raw_api.GetActivePlugins(len_),
            error_msg=f'GetActivePlugins failed',
            ex=ex)

    def load_plugins(self, load_order, smart_load=True, use_dummies=False, ex=True):
        '''
        Loads the given ``load_order`` of plugin files. If ``smart_load`` is
        set to ``True``, master files required by files in ``load_order`` will
        be automatically loaded as necessary. Plugin loading is performed in a
        background thread. Use ``xelib.get_loader_status`` to track the loader
        and determine when it is done.

        Args:
            load_order (``str``):
                the load order of plugins to load; should be given in string
                form as a ``\\r\\n``-separated list of plugin names.
            smart_load (``bool``):
                whether to automatically load masters as well
            use_dummies (``bool``):
                TODO: to be written
        '''
        return self.verify_execution(
            self.raw_api.LoadPlugins(load_order, smart_load, use_dummies),
            error_msg=f'Failed to LoadPlugins given load_order '
                      f'{repr(load_order)}; smart_load={smart_load}; '
                      f'use_dummies={use_dummies}',
            ex=ex)

    def load_plugin(self, file_name, ex=True):
        '''
        Loads the plugin file ``file_name`` at the next available load order
        position after the currently loaded plugin files. Plugin loading is
        performed in a background thread, use ``xelib.get_loader_status`` to
        track the loader and determine when it is done.

        Args:
            file_name (``str``):
                the name of the plugin to further load into the current session
        '''
        return self.verify_execution(
            self.raw_api.LoadPlugin(file_name),
            error_msg=f'Failed to load {file_name}',
            ex=ex)

    def load_plugin_header(self, file_name, ex=True):
        '''
        Loads the header of plugin file ``file_name`` and returns a handle to
        it. This plugin should be unloaded with ``xelib.unload_plugin`` when
        you're done with it.

        Note: Unlike ``xelib.load_plugin`` above, this function does not use
        a background thread.

        Args:
            file_name (``str``):
                the name of the plugin to load header for
        Returns:
            (``int``) a handle to the loaded plugin header
        '''
        return self.get_handle(
            lambda res: self.raw_api.LoadPluginHeader(file_name, res),
            error_msg=f'Failed to load plugin header for {file_name}',
            ex=ex)

    def build_references(self, id_, sync=True, ex=True):
        '''
        Builds the "reference by" information for the given ``id_`` plugin file
        handle. If `id_` is ``0``, reference information will be built for all
        loaded plugins.

        Args:
            id_ (``int``):
                the handle to the plugin file to build references for; 0 means
                all plugins
            sync (``bool``):
                TODO: to be written
        '''
        return self.verify_execution(
            self.raw_api.BuildReferences(id_, sync),
            error_msg=f'Failed to build references for '
                      f'{self.element_context(id_)}',
            ex=ex)

    def unload_plugin(self, id_, ex=True):
        '''
        Unloads the plugin file `id_`. Only plugins at the end of the active
        load order which have not have references built can be unloaded. Plugin
        headers loaded with ``xelib.load_plugin_header`` can also be unloaded.

        Args:
            id_ (``int``):
                the handle to the plugin file to unload
        '''
        return self.verify_execution(
            self.raw_api.UnloadPlugin(id_),
            error_msg=f'Failed to unload plugin {self.element_context(id_)}',
            ex=ex)

    def get_loader_status(self, ex=True):
        '''
        Returns the status of the loader. This method is used to check the
        progress and completion of asynchronous load methods like
        ``xelib.load_plugins`` and ``xelib.load_plugin``.

        Returns:
            (``Xelib.LoaderStates``) the enum value representing the current
            loader status
        '''
        return LoaderStates(self.get_byte(
            lambda res: self.raw_api.GetLoaderStatus(res),
            error_msg=f'Failed to get loader status',
            ex=ex))

    def get_loaded_file_names(self, exclude_hardcoded=True, ex=True):
        '''
        Returns an array of all loaded file names. If ``exclude_hardcoded`` is
        set to ``True``, hardcoded files will be ignored.

        Args:
            exclude_hardcoded (``bool``):
                if set to ``True``, hardcoded files like ``TESV.exe`` (usually
                there is at least one at the very base) in the plugins list will
                be ignored.

        Returns:
            (``List[str]``) a list of plugin file names that are loaded
        '''
        file_names = []
        for file_ in self.get_elements(ex=ex):
            file_name = self.name(file_, ex=ex)
            if exclude_hardcoded and file_name.endswith('.exe'):
                continue
            file_names.append(file_name)
        return file_names

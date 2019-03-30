import os
import time

from xedit.xedit.base import XEditBase
from xedit.xelib import Xelib


class XEdit(XEditBase):
    def __init__(self,
                 game_mode=Xelib.GameModes.gmSSE,
                 game_path=None,
                 plugins=None):
        self.import_all_object_classes()

        self._game_mode = game_mode
        self._game_path = game_path
        self._plugins = plugins or []
        self._xelib = Xelib()

        self.handle = 0
        self.auto_release = False

    @property
    def game_path(self):
        if self._xelib.loaded:
            return self.xelib.get_game_path()
        else:
            return self._game_path

    @property
    def plugin_count(self):
        return int(self.xelib.get_global('FileCount'))

    @property
    def plugin_names(self):
        return self.xelib.get_loaded_file_names()

    def session(self, load_plugins=True):
        class XeditSession:
            def __init__(self, xedit, load_plugins):
                self.xedit = xedit
                self.load_plugins = load_plugins

            def __enter__(self):
                self.xedit.xelib.__enter__()
                self.xedit.xelib.set_game_mode(self.xedit._game_mode)
                if self.xedit._game_path:
                    self.xedit.xelib.set_game_path(self.xedit._game_path)
                if self.load_plugins:
                    self.xedit.xelib.load_plugins(
                        os.linesep.join(self.xedit._plugins))
                    while (self.xedit.xelib.get_loader_status() ==
                                                Xelib.LoaderStates.lsActive):
                        time.sleep(0.1)
                return self.xedit

            def __exit__(self, exc_type, exc_value, traceback):
                self.xedit.xelib.__exit__(exc_type, exc_value, traceback)

        return XeditSession(self, load_plugins)

    @classmethod
    def quickstart(cls, game=XEditBase.Games.SkyrimSE, plugins=None):
        '''
        For when you want to play around with an xedit session in the
        interpreter quickly
        '''
        plugins = plugins or ['Skyrim.esm', 'Update.esm', 'Dawnguard.esm']
        xedit = cls(game_mode=game, plugins=plugins)
        return xedit.session().__enter__()

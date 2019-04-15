from contextlib import contextmanager
import os
import time

from pyxedit.xedit.base import XEditBase
from pyxedit.xelib import Xelib


class XEdit(XEditBase):
    def __init__(self,
                 game_mode=XEditBase.Games.SkyrimSE,
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

    @contextmanager
    def session(self, load_plugins=True):
        with self.xelib.session():
            self.xelib.set_game_mode(self._game_mode)
            if self._game_path:
                self.xelib.set_game_path(self._game_path)
            if load_plugins:
                self.xelib.load_plugins(os.linesep.join(self._plugins))
                while (self.xelib.get_loader_status() ==
                           Xelib.LoaderStates.lsActive):
                    time.sleep(0.1)
            yield self

    @classmethod
    def quickstart(cls, game=XEditBase.Games.SkyrimSE, plugins=None):
        '''
        For when you want to play around with an xedit session in the
        interpreter quickly
        '''
        plugins = plugins or ['Skyrim.esm', 'Update.esm', 'Dawnguard.esm']
        xedit = cls(game_mode=game, plugins=plugins)
        return xedit.session().__enter__()

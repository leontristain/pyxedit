from contextlib import contextmanager

from pyxedit.xedit.base import XEditBase
from pyxedit.xelib import Xelib


class XEdit(XEditBase):
    def __init__(self,
                 game_mode=XEditBase.GameModes.SSE,
                 game_path=None,
                 plugins=None,
                 xeditlib_path=None):
        self.import_all_object_classes()
        self._xelib = Xelib(game_mode=game_mode,
                            game_path=game_path,
                            plugins=plugins,
                            xeditlib_path=xeditlib_path)
        self.handle = 0
        self.auto_release = False

    @property
    def game_mode(self):
        return self._xelib.game_mode

    @game_mode.setter
    def game_mode(self, value):
        self._xelib.game_mode = value

    @property
    def game_path(self):
        return self._xelib.game_path

    @game_path.setter
    def game_path(self, value):
        self._xelib.game_path = value

    @property
    def plugins(self):
        return self._xelib.plugins

    @plugins.setter
    def plugins(self, value):
        self._xelib.plugins = value

    @property
    def plugin_count(self):
        return int(self.xelib.get_global('FileCount'))

    @property
    def plugin_names(self):
        return self.xelib.get_loaded_file_names()

    @contextmanager
    def session(self, load_plugins=True):
        with self.xelib.session():
            yield self

    def add_file(self, file_name):
        return self.objectify(self.xelib.add_file(file_name))

    @classmethod
    def quickstart(cls, game=XEditBase.GameModes.SSE, plugins=None):
        '''
        For when you want to play around with an xedit session in the
        interpreter quickly
        '''
        plugins = plugins or ['Skyrim.esm', 'Update.esm', 'Dawnguard.esm']
        xedit = cls(game_mode=game, plugins=plugins)
        xedit.xelib.start_session()
        return xedit

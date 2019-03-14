import os
import time

from xelib.xedit.base import XEditBase
from xelib.xedit.plugin import XEditPlugin
from xelib.xelib import Xelib


class XEdit(XEditBase):
    def __init__(self,
                 game_mode=Xelib.GameModes.gmSSE,
                 game_path=None,
                 plugins=None):
        self.game_mode = game_mode
        self.game_path = game_path
        self.plugins = plugins or []
        self._xelib = Xelib()

    def plugin(self, plugin_name):
        h = self.xelib.file_by_name(plugin_name)
        return XEditPlugin.from_xedit_obj(h, self)

    def session(self):
        class XeditSession:
            def __init__(xedit):
                self.xedit = xedit

            def __enter__(self):
                self.xedit.xelib.__enter__()
                self.xedit.xelib.set_game_mode(self.game_mode)
                if self.game_path:
                    self.xedit.xelib.set_game_path(self.game_path)
                self.xedit.xelib.load_plugins(os.linesep.join(self.plugins))
                while (self.xedit.xelib.get_loader_status() ==
                                            Xelib.LoaderStates.lsActive):
                    time.sleep(0.1)
                return self.xedit

            def __exit__(self, exc_type, exc_value, traceback):
                self.xedit.xelib.__exit__(exc_type, exc_value, traceback)

        return XeditSession(self)

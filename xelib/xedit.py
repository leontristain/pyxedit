import os
import time

from xelib.xelib import Xelib


class XEditError(Exception):
    pass


class XEditBase:
    def __init__(self, xelib):
        self.handle = None
        self._handle_group = None
        self._xelib = xelib

    @property
    def xelib(self):
        if self.handle and self.handle not in self._handle_group:
            raise XEditError(f'Accessing XEdit object of handle {self.handle} '
                             f'which has already been released from the '
                             f'xelib session')
        return self._xelib


class XEditPlugin(XEditBase):
    def __init__(self, xelib, handle):
        self.xelib = xelib
        self.handle = handle

    @property
    def name(self):
        return self.xelib.name(self.handle)

    @property
    def author(self):
        return self.xelib.get_file_author(self.handle)

    @author.setter
    def author(self, value):
        self.xelib.set_file_author(self.handle, value)

    @property
    def description(self):
        return self.xelib.get_description(self.handle)

    @description.setter
    def description(self, value):
        self.xelib.set_description(self.handle, value)

    @property
    def is_esm(self):
        return self.xelib.get_is_esm(self.handle)

    @is_esm.setter
    def is_esm(self, value):
        self.xelib.set_is_esm(self.handle, value)

    @property
    def next_object_id(self):
        return self.xelib.get_next_object_id(self.handle)

    @next_object_id.setter
    def next_object_id(self, value):
        self.xelib.set_next_object_id(self.handle, value)

    def save(self):
        return self.xelib.save_file(self.handle)

    def save_as(self, file_path):
        return self.xelib.save_file(self.handle, file_path=file_path)


class XEdit(XEditBase):
    def __init__(self, game_mode, game_path, plugins):
        self.game_mode = game_mode
        self.data_path = game_path
        self.plugins = plugins
        self.xelib = Xelib()

    def session(self):
        class XeditSession:
            def __init__(xedit):
                self.xedit = xedit

            def __enter__(self):
                self.xedit.xelib.__enter__()
                self.xedit.xelib.set_game_mode(self.game_mode)
                self.xedit.xelib.set_game_path(self.game_path)
                self.xedit.xelib.load_plugins(os.linesep.join(self.plugins))
                while (self.xedit.xelib.get_loader_status() ==
                           Xelib.LoaderStates.lsActive):
                    time.sleep(0.1)
                return self.xedit

            def __exit__(self, exc_type, exc_value, traceback):
                self.xedit.xelib.__exit__(exc_type, exc_value, traceback)

        return XeditSession(self)

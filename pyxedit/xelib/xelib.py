import ctypes
from contextlib import contextmanager
from ctypes import wintypes
from itertools import tee
from pathlib import Path
import os
import time

from pyxedit.xelib.definitions import DelphiTypes, XEditLibSignatures
from pyxedit.xelib.wrapper_methods.element_values import ElementValuesMethods
from pyxedit.xelib.wrapper_methods.elements import ElementsMethods
from pyxedit.xelib.wrapper_methods.errors import ErrorsMethods
from pyxedit.xelib.wrapper_methods.file_values import FileValuesMethods
from pyxedit.xelib.wrapper_methods.files import FilesMethods
from pyxedit.xelib.wrapper_methods.filter import FilterMethods
from pyxedit.xelib.wrapper_methods.groups import GroupsMethods
from pyxedit.xelib.wrapper_methods.helpers import HelpersMethods, XelibError
from pyxedit.xelib.wrapper_methods.masters import MastersMethods
from pyxedit.xelib.wrapper_methods.messages import MessagesMethods
from pyxedit.xelib.wrapper_methods.meta import MetaMethods
from pyxedit.xelib.wrapper_methods.record_values import RecordValuesMethods
from pyxedit.xelib.wrapper_methods.records import RecordsMethods
from pyxedit.xelib.wrapper_methods.resources import ResourcesMethods
from pyxedit.xelib.wrapper_methods.serialization import SerializationMethods
from pyxedit.xelib.wrapper_methods.setup import SetupMethods

__all__ = ['DLL_PATH', 'Xelib', 'XelibError']

DLL_PATH = Path(__file__).parent / '../../XEditLib/XEditLib.dll'


def pairwise(iterable):
    '''
    A pairwise iterator, copied from:
        https://docs.python.org/3/library/itertools.html
    '''
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


class Xelib(ElementValuesMethods,
            ElementsMethods,
            ErrorsMethods,
            FileValuesMethods,
            FilesMethods,
            FilterMethods,
            GroupsMethods,
            HelpersMethods,
            MastersMethods,
            MessagesMethods,
            MetaMethods,
            RecordValuesMethods,
            RecordsMethods,
            ResourcesMethods,
            SerializationMethods,
            SetupMethods):
    '''
    Xelib class
    '''
    def __init__(self,
                 game_mode=SetupMethods.GameModes.SSE,
                 game_path=None,
                 plugins=None):
        '''
        Initializer
        '''
        # Initialization attributes
        self._game_mode = game_mode
        self._game_path = game_path
        self._plugins = plugins or []

        # XEditLib.dll entry points
        self.dll_path = DLL_PATH
        self._raw_api = None

        # Attribute for handle management
        self._handles_stack = []
        self._current_handles = set()

    @property
    def game_path(self):
        return self.get_game_path() if self.loaded else self._game_path

    @game_path.setter
    def game_path(self, value):
        self._game_path = value
        if self.loaded:
            return self.set_game_path(value)

    @contextmanager
    def session(self, load_plugins=True):
        try:
            # sanity check that API has not yet been loaded
            if self.loaded:
                raise XelibError('Api already loaded')

            # load XEditLib.dll
            self._raw_api = self.load_lib(self.dll_path)

            # initialize the xEdit context
            self.initialize()

            # set the game mode if given
            if self._game_mode:
                self.set_game_mode(self._game_mode)

            # set the game path explicitly if given
            if self._game_path:
                self.set_game_path(self._game_path)

            # load plugins if specified
            if load_plugins:
                self.load_plugins(os.linesep.join(self._plugins))
                while (self.get_loader_status() ==
                            SetupMethods.LoaderStates.Active):
                    time.sleep(0.1)

            # loading is done, given handle to user
            yield self

        finally:
            # sanity check that API is loaded
            if not self.loaded:
                raise XelibError('Api is not loaded; something is wrong')

            # unload the API
            self.release_all_handles()
            self.finalize()
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel32.FreeLibrary.argtypes = [wintypes.HMODULE]
            kernel32.FreeLibrary(self._raw_api._handle)
            self._raw_api = None

    @property
    def loaded(self):
        return bool(self._raw_api)

    @property
    def full_handles_stack(self):
        return self._handles_stack + [self._current_handles]

    @property
    def all_opened_handles(self):
        opened_handles = set()
        for handles in self.full_handles_stack:
            opened_handles.update(handles)
        return opened_handles

    def track_handle(self, handle):
        self._current_handles.add(handle)

    def release_handle(self, handle):
        try:
            self.release(handle)
        except XelibError:
            pass
        finally:
            for layer in self.full_handles_stack:
                if handle in layer:
                    layer.remove(handle)

    def release_handles(self, handles):
        for handle in handles:
            self.release_handle(handle)

    def release_current_handles(self):
        self.release_handles(list(self._current_handles))

    def release_all_handles(self):
        self.release_handles(list(self.all_opened_handles))

    @contextmanager
    def manage_handles(self):
        try:
            self._handles_stack.append(self._current_handles)
            self._current_handles = set()
            yield
        finally:
            self.release_current_handles()
            self._current_handles = self._handles_stack.pop()

    def print_handle_management_stack(self):
        for i, handles in enumerate(self._handles_stack):
            print(f'{i}: {handles}')
        print(f'{len(self._handles_stack)}: {self._current_handles}')

    def promote_handle(self, handle):
        for (current_layer,
             parent_layer) in pairwise(reversed(self.full_handles_stack)):
            if handle in current_layer:
                current_layer.remove(handle)
                parent_layer.add(handle)
                return parent_layer
        print(f'failed to promote handle {handle}')

    @property
    def raw_api(self):
        if not self._raw_api:
            raise XelibError(f'Must use Xelib within its own context; the '
                             f'code should look something like: `with xelib '
                             f'as xelib: xelib.do_something`')
        return self._raw_api

    @staticmethod
    def load_lib(dll_path):
        # load XEditLib.dll
        lib = ctypes.CDLL(str(dll_path))

        # define type signatures for XEditLib.dll methods
        for signature in XEditLibSignatures:
            method_name = signature.name
            params, return_type = signature.value
            try:
                method = getattr(lib, method_name)
                method.argtypes = [DelphiTypes[type_].value
                                   for _, type_ in params.items()]
                if return_type:
                    method.restype = DelphiTypes[return_type].value
            except AttributeError:
                print(f'WARNING: missing function {method_name}')

        # return a handle to the loaded library
        return lib

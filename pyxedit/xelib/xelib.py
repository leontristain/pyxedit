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

DLL_PATH = Path(__file__).parent / '../xedit-lib/XEditLib.dll'


def pairwise(iterable):
    '''
    A pairwise iterator, copied from:
        https://docs.python.org/3/library/itertools.html
    '''
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def with_debug_log(method=False):
    '''
    A decorator for debugging purposes. It can be used to wrap around a
    function or a method, such that whenever the method is called, the wrapper
    will log the call signature and the return value to a `log.txt` file in
    your current working directory.

    @param method:
        if True, the first argument to the call (which in an object method
        will typically be `self`) will be ommitted from the call signature.
    '''
    def _with_debug_log(callable):
        def wrapper(*args, **kwargs):
            # determine what args to display based on whether method=True
            displayed_args = args[1:] if method else args

            # collect the parameters and format the values into a call signature
            # string
            params = []
            if displayed_args:
                params.append(', '.join([f'{repr(a)}' for a in displayed_args]))
            if kwargs:
                params.append(', '.join([f'{k}={repr(v)}' for k, v in kwargs.items()]))
            params_text = ', '.join(params)

            # we will write/append to this file
            with open('log.txt', 'a') as f:
                # write the call signature
                f.write(f'{callable.__name__}({params_text})\n')

                # execute the wrapped function
                return_value = callable(*args, **kwargs)

                if return_value is not None:
                    # format the returned value; if it is a multi-line string,
                    # only display the first line
                    displayed_return_value = return_value
                    if (isinstance(displayed_return_value, str) and
                            '\n' in displayed_return_value):
                        displayed_return_value = (
                            displayed_return_value.split('\n')[0] + ' ...')

                    # write the return value
                    f.write(f'    --> {displayed_return_value}\n')
            return return_value
        return wrapper
    return _with_debug_log


class XelibWrapperAPI:
    '''
    A class that wraps around the CDLL object for XEditLib.dll. Each call to
    something on the CDLL object will be interjected and given a `with_log_debug`
    wrapper around that same call. This way, all calls to XEditLib.dll can have
    its calling signature and return values logged for inspection.
    '''
    def __init__(self, raw_api):
        # keeps a reference to CDLL object
        self.raw_api = raw_api

    def __getattr__(self, attr):
        try:
            # make sure methods on XelibWrapperAPI itself is not affected
            return super(XelibWrapperAPI, self).__getattr__(attr)
        except AttributeError:
            # otherwise, run __get_method to generate a wrapped callable
            # around the requested raw_api call
            return self.__get_method(attr)

    def __get_method(self, name):
        # return a `with_debug_log` wrapped callable around the raw_api call
        return with_debug_log()(getattr(self.raw_api, name))


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
    def __init__(self,
                 game_mode=SetupMethods.GameModes.SSE,
                 game_path=None,
                 plugins=None,
                 xeditlib_path=None):
        '''
        ``Xelib`` class initializer.

        Args:
            game_mode (``Xelib.GameModes``):
                This is where you tell Xelib which game you want it to work
                with. Accepts anything in the ``Xelib.GameModes`` enum.
                For Skyrim, use ``Xelib.GameModes.TES5``. For Skyrim Special
                Edition, use ``Xelib.GameModes.SSE``.

            game_path (``str``):
                The path to the game folder. If not given, the library will
                attempt to automatically find the game's install path using
                known registry values.

            plugins (``List[str]``):
                The list of plugins to load. Any required masters will be
                automatically included as well.

            xeditlib_path (``str``):
                If you want to point ``Xelib`` to use your own copy of
                ``XEditLib.dll``, you may provide the file path here. Otherwise,
                the library will use its own copy of ``XEditLib.dll``. Note that
                ``pyxedit.Xelib`` makes very tight assumptions about what
                functions exist in ``XEditLib.dll`` and what their signatures
                are. If your provided ``XEditLib.dll`` does not have a perfectly
                matching API, there will likely be all kinds of errors.
        '''
        # Initialization attributes
        self._game_mode = game_mode
        self._game_path = game_path
        self._plugins = plugins or []

        # XEditLib.dll entry points
        self.dll_path = xeditlib_path or DLL_PATH
        self._raw_api = None
        self._wrapper_api = None  # point `raw_api` to this to log debug calls

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

    def start_session(self, load_plugins=True):
        # sanity check that API has not yet been loaded
        if self.loaded:
            raise XelibError('Api already loaded')

        # load XEditLib.dll
        self._raw_api = self.load_lib(self.dll_path)
        self._wrapper_api = XelibWrapperAPI(self._raw_api)

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

    def end_session(self):
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
        self._wrapper_api = None

    @contextmanager
    def session(self, load_plugins=True):
        '''
        Creates a context manager for your ``Xelib`` session. This is the
        primary way in which you are expected to use the ``Xelib`` API.
        See example:

        .. highlight:: python
        .. code-block:: python

            with Xelib(plugins=['GOT.esp']).session() as xelib:
                # do stuff with xelib handle
                print(xelib.get_element('GOT.esp\\\\NPC_\\\\JonSnow'))

        Upon entering the session context, ``Xelib`` will load ``XEditLib.dll``,
        and call its ``InitXEdit`` function. Then, if ``load_plugin`` is set
        to ``True``, ``Xelib`` will attempt to load its list of plugins.

        Upon exiting the session context, ``Xelib`` will release all opened
        handles, then call the ``CloseXEdit`` function, and finally frees the
        ``XEditLib.dll`` shared library from memory.

        Args:
            load_plugins (``bool``):
                Whether to load ``Xelib``'s list of plugins after initializing
                ``XEditLib.dll``
        '''
        try:
            self.start_session()
            yield self
        finally:
            self.end_session()

    @property
    def loaded(self):
        '''
        (``bool``) A property that tells you whether ``XEditLib.dll`` is loaded.
        (i.e. whether you are within a session)
        '''
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
        '''
        Add the given handle to the current handle management stack layer
        for tracking purposes.

        Args:
            handle (``int``)
                The handle to track
        '''
        self._current_handles.add(handle)

    def release_handle(self, handle):
        '''
        Releases a handle, and remove it from the handle management stack.

        Args:
            handle (``int``)
                The handle to release
        '''
        try:
            self.release(handle)
        except XelibError:
            pass
        finally:
            for layer in self.full_handles_stack:
                if handle in layer:
                    layer.remove(handle)

    def release_handles(self, handles):
        '''
        Releases the given list of handles.

        Args:
            handles (``List[int]``)
                The list of handles to release
        '''
        for handle in handles:
            self.release_handle(handle)

    def release_current_handles(self):
        self.release_handles(list(self._current_handles))

    def release_all_handles(self):
        self.release_handles(list(self.all_opened_handles))

    @contextmanager
    def manage_handles(self):
        '''
        A context manager that helps you manage sets of handles. Any new handles
        returned by a ``Xelib`` API method within such a context will be
        automatically released on context exit. These handle management contexts
        can be nested. See below example:

        .. highlight:: python
        .. code-block:: python

            with Xelib(plugins=['GOT.esp', 'LOTR.esp']).session() as xelib:
                # handle 1 gets created
                h1 = xelib.get_element('GOT.esp\\\\NPC_\\\\JonSnow')

                with xelib.manage_handles():
                    # handle 2 gets created
                    h2 = xelib.get_element('GOT.esp\\\\NPC_\\\\Brienne')

                    with xelib.manage_handles():
                        # handle 3 gets created
                        h3 = xelib.get_element('LOTR.esp\\\\NPC_\\\\Imrahil')

                    # on context exit, handle 3 gets released
                # on context exit, handle 2 gets released
            # at the end of session, handle 1 gets released
        '''
        try:
            self._handles_stack.append(self._current_handles)
            self._current_handles = set()
            yield
        finally:
            self.release_current_handles()
            self._current_handles = self._handles_stack.pop()

    def print_handle_management_stack(self):
        '''
        Prints the entire handle management stack to stdout. Useful for
        debugging.
        '''
        for i, handles in enumerate(self._handles_stack):
            print(f'{i}: {handles}')
        print(f'{len(self._handles_stack)}: {self._current_handles}')

    def promote_handle(self, handle):
        '''
        Promotes the given handle from its current handle management context
        to its parent handle management context. This is useful for preserving
        handles you're interested in.

        Args:
            handle (``int``)
                The handle to promote to parent handle management context
        '''
        for (current_layer,
             parent_layer) in pairwise(reversed(self.full_handles_stack)):
            if handle in current_layer:
                current_layer.remove(handle)
                parent_layer.add(handle)
                return parent_layer
        print(f'failed to promote handle {handle}')

    @property
    def raw_api(self):
        '''
        (``ctypes.CDLL``) A property that gives you the handle to the
        ``ctypes.CDLL`` raw API object. Calling functions from this object
        will call functions on ``XEditLib.dll`` directly. If you want the
        lowest access to ``XEditLib.dll``, this provides it.

        This property cannot be accessed when ``XEditLib.dll`` has not been
        loaded (i.e. not in a session), in which case, a ``XelibError`` will
        be raised.

        Most users should probably not call the DLL functions directly, since
        the call patterns are a bit counterintuitive to users of higher-level
        programming languages. For example, most string getter functions on
        ``XEditLib.dll`` will return not the result string itself, but a
        `success` value of `True` or `False`, where the caller is expected to
        then call a ``GetResultString`` function to retrieve the value from some
        centralized result location.

        The ``Xelib`` API methods are essentially near 1-to-1 mappings of
        the ``XEditLib.dll`` functions, except with the tedious patterns of
        "checking for success and then call a value-getter function"
        automatically handled, such that the function call would return the
        actual value itself, or raise Exceptions, like what you'd expect from
        a higher-level programming language API. Thus, most users should use
        ``Xelib`` methods instead.
        '''
        if not self._raw_api:
            raise XelibError(f'Must use Xelib within its own context; the '
                             f'code should look something like: `with xelib '
                             f'as xelib: xelib.do_something`')

        # uncomment the `self._wrapper_api` below to log debug calls; will
        # affect performance, so only enable when necessary
        # return self._wrapper_api
        return self._raw_api

    @staticmethod
    def load_lib(dll_path):
        '''
        Loads ``XEditLib.dll`` into python and wrap it with ctypes definitions
        based on known calling signatures of the DLL functions.

        Args:
            dll_path (``str``):
                Path to the ``XEditLib.dll`` file
        Returns:
            ``ctypes.CDLL``: handle to the loaded library
        '''
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


'''
If the below switch is turned on, the associated logic will add to the `Xelib`
class `with_debug_log` wrappers for all of the Xelib API calls. This will log
all Xelib API calls to a `log.txt` file in your current working directory. It
can be immensely helpful when optimizing the high-level XEdit API's usage of
the Xelib API, but logging every call will affect performance, so this should
be only enabled when debugging.
'''
apply_log_wrappers = False
if apply_log_wrappers:
    import inspect  # NOQA
    for methods in (
            ElementValuesMethods,
            ElementsMethods,
            ErrorsMethods,
            FileValuesMethods,
            FilesMethods,
            FilterMethods,
            GroupsMethods,
            # for now, we ignore HelpersMethods stuff since they are too
            # low-leveled and tend to add a lot of noise to the log. In due time
            # we should at least support the stuff like `element_context`
            # HelpersMethods
            MastersMethods,
            MessagesMethods,
            MetaMethods,
            RecordValuesMethods,
            RecordsMethods,
            ResourcesMethods,
            SerializationMethods,
            SetupMethods):
        for name, method in inspect.getmembers(methods, inspect.isfunction):
            if not name.startswith('_'):
                setattr(Xelib, name, with_debug_log(method=True)(method))

from enum import Enum, unique

from pyxedit.xelib.wrapper_methods.base import WrapperMethodsBase


@unique
class SortBy(Enum):
    None_ = 0
    FormID = 1
    EditorID = 2
    Name = 3


class MetaMethods(WrapperMethodsBase):
    SortBy = SortBy

    def initialize(self):
        '''
        Initializes an xEdit session. Corresponds to ``InitXEdit`` from
        ``XEditLib.dll``. I'm not fully sure what this does exactly,
        but it is required for the other ``XEditLib.dll`` functions to work.
        The name ``InitXEdit`` sounds like it may be the equivalent of starting
        up xEdit.

        Without running this first, calling other ``XEditLib.dll`` functions
        will at times result in memory access violation related to null
        references.

        .. warning::
            Users should not have to run this method by hand, as it should be
            covered with ``Xelib``'s context manager functionality.
        '''
        self.raw_api.InitXEdit()

    def finalize(self):
        '''
        Closes the xEdit session. Corresponds to ``CloseXEdit`` from
        ``XEditLib.dll``.

        .. warning::
            Users should not have to run this method by hand, as it should be
            covered with ``Xelib``'s context manager functionality.
        '''
        self.raw_api.CloseXEdit()

    def get_global(self, key: str, ex: bool = True):
        '''
        Retrieves the value of an ``XEditLib.dll`` global variable. Examples of
        global variables may include ``ProgramPath``, ``Version``, and
        ``FileCount``. These values are used for some of ``XEditLib.dll``'s
        internal functionality.

        The above examples might be out of date in due time. To see what global
        variables ``XEditLib.dll`` currently contains, you can run
        :func:`~pyxedit.Xelib.get_globals`.

        :param key: name of the global variable to retrieve
        :param ex: whether failures should trigger an Exception or return a
                   falsey value
        :returns: the value of the global variable being retrieved
        '''
        return self.get_string(
            lambda len_: self.raw_api.GetGlobal(key, len_),
            error_msg=f'GetGlobal failed',
            ex=ex)

    def get_globals(self, ex: bool = True):
        '''
        Returns a list of name-value pairs for all globals. Entries are
        separated by ``\\r\\n``, and the name value pairs are separated by
        ``=``.

        :param ex: whether failures should trigger an Exception or return a
                   falsey value
        :returns: name-value pairs for all globals as described above
        '''
        return self.get_string(
            lambda len_: self.raw_api.GetGlobals(len_),
            error_msg=f'GetGlobals failed',
            ex=ex)

    def set_sort_mode(self, mode, reverse=False, ex=True):
        return self.verify_execution(
            self.raw_api.SetSortMode(mode.value, reverse),
            error_msg=f'Failed to set sort mode to {mode} '
                      f'{"ASC" if reverse else "DESC"}',
            ex=ex)

    def release(self, id_, ex=True):
        return self.verify_execution(
            self.raw_api.Release(id_),
            error_msg=f'Failed to release handle {id_}',
            ex=ex)

    def release_nodes(self, id_, ex=True):
        return self.verify_execution(
            self.raw_api.ReleaseNodes(id_),
            error_msg=f'Failed to release nodes {id_}',
            ex=ex)

    def switch(self, id_, id2, ex=True):
        return self.verify_execution(
            self.raw_api.Switch(id_, id2),
            error_msg=f'Failed to switch interface #{id_} and #{id2}',
            ex=ex)

    def get_duplicate_handles(self, id_, ex=True):
        return self.get_array(
            lambda len_: self.raw_api.GetDuplicateHandles(id_, len_),
            error_msg=f'Failed to get duplicate handles for {id_}',
            ex=ex)

    def clean_store(self, ex=True):
        return self.verify_execution(
            self.raw_api.CleanStore(),
            error_msg=f'Failed to clean interface store',
            ex=ex)

    def reset_store(self, ex=True):
        return self.verify_execution(
            self.raw_api.ResetStore(),
            error_msg=f'Failed to reset interface store',
            ex=ex)

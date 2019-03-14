class XEditError(Exception):
    pass


class XEditBase:
    def __init__(self, xelib, handle, handle_group):
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

    @classmethod
    def from_xedit_obj(cls, handle, xedit_obj):
        if not handle or handle not in xedit_obj._xelib._current_handles:
            raise XEditError(f'Attempting to create XEdit object from invalid '
                             f'handle {handle}')
        return cls(xedit_obj.xelib, handle, xedit_obj._xelib._current_handles)
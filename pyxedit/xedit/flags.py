from pyxedit.xedit.generic import XEditGenericObject


class XEditFlags(XEditGenericObject):
    '''
    Used for flag types
    '''
    # dictionary-like functionality
    def __getitem__(self, key):
        return self.get_flag(key)

    def __setitem__(self, key, value):
        return self.set_flag(key)

    def __iter__(self):
        for key in self.keys():
            yield key

    def __len__(self):
        return len(self.all_flags)

    def __repr__(self):
        return (f'<{self.__class__.__name__} '
                f'enabled: {repr(tuple(self.enabled))} '
                f'{self.handle}>')

    def keys(self):
        for flag_name in self.all_flags:
            yield flag_name

    def values(self):
        for key in self.keys():
            yield self[key]

    def items(self):
        for key in self.keys():
            yield key, self[key]

    # translating to and from a raw dictionary
    def to_dict(self):
        return {key: value for key, value in self.items()}

    def from_dict(self, dict_):
        for key, value in dict_:
            self[key] = value

    # wrappers for xelib methods
    def get_flag(self, flag_name):
        return self.xelib_run('get_flag', flag_name)

    def set_flag(self, flag_name, state):
        return self.xelib_run('set_flag', flag_name, state)

    @property
    def all_flags(self):
        return self.xelib_run('get_all_flags')

    @property
    def enabled(self):
        return self.xelib_run('get_enabled_flags')

    @enabled.setter
    def enabled(self, value):
        return self.xelib_run('set_enabled_flags', value)

    def enable(self, flag_name):
        return self.xelib_run('set_flag', flag_name, True)

    def disable(self, flag_name):
        return self.xelib_run('set_flag', flag_name, False)

from functools import partial

from xelib.xedit.base import XEditGenericObject


class XEditTextureSet(XEditGenericObject):
    SIGNATURE = 'TXST'

    def texture_slot_path(self, slot):
        return f'Textures (RGB/A)\\TX{slot:0>2}'

    def get_texture_path(self, slot=0):
        '''
        Returns the string at the texture slot path if it exists; or None if not
        '''
        with self.manage_handles():
            slot_path = self.texture_slot_path(slot)
            if self.get(slot_path):
                return self.get_value(path=slot_path)

    def set_texture_path(self, path, slot=0):
        '''
        Sets the string at the texture slot path; if None is given, the slot
        path will be deleted if it exists.
        '''
        with self.manage_handles():
            slot_path = self.texture_slot_path(slot)
            if path is None:
                if self.get(slot_path):
                    self.delete_texture_path(slot=slot)
            else:
                if not self.get(slot_path):
                    self.add(slot_path)
                self.set_value(path, path=slot_path)

    def delete_texture_path(self, slot=0):
        '''
        Delete the texture slot path
        '''
        with self.manage_handles():
            self[self.texture_slot_path(slot)].delete()

    tx00 = property(fget=partial(get_texture_path, slot=0),
                    fset=partial(set_texture_path, slot=0),
                    fdel=partial(delete_texture_path, slot=0))
    tx01 = property(fget=partial(get_texture_path, slot=1),
                    fset=partial(set_texture_path, slot=1),
                    fdel=partial(delete_texture_path, slot=1))
    tx02 = property(fget=partial(get_texture_path, slot=2),
                    fset=partial(set_texture_path, slot=2),
                    fdel=partial(delete_texture_path, slot=2))
    tx03 = property(fget=partial(get_texture_path, slot=3),
                    fset=partial(set_texture_path, slot=3),
                    fdel=partial(delete_texture_path, slot=3))
    tx04 = property(fget=partial(get_texture_path, slot=4),
                    fset=partial(set_texture_path, slot=4),
                    fdel=partial(delete_texture_path, slot=4))
    tx05 = property(fget=partial(get_texture_path, slot=5),
                    fset=partial(set_texture_path, slot=5),
                    fdel=partial(delete_texture_path, slot=5))
    tx06 = property(fget=partial(get_texture_path, slot=6),
                    fset=partial(set_texture_path, slot=6),
                    fdel=partial(delete_texture_path, slot=6))
    tx07 = property(fget=partial(get_texture_path, slot=7),
                    fset=partial(set_texture_path, slot=7),
                    fdel=partial(delete_texture_path, slot=7))

    @property
    def texture_paths(self):
        '''
        Return the list of all texture paths.
        '''
        return [self.tx00, self.tx01, self.tx02, self.tx03,
                self.tx04, self.tx05, self.tx06, self.tx07]

    @property
    def file_paths(self):
        '''
        Return a list of all file paths currently associated with this record
        '''
        return [path for path in self.texture_paths if path]

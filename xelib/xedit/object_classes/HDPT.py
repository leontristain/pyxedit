from enum import Enum

from xelib.xedit.base import XEditGenericObject


class HeadPartTypes(Enum):
    Misc = 'Misc'
    Face = 'Face'
    Eyes = 'Eyes'
    Hair = 'Hair'
    FacialHair = 'Facial Hair'
    Scar = 'Scar'
    Eyebrows = 'Eyebrows'


class XEditHeadPart(XEditGenericObject):
    SIGNATURE = 'HDPT'
    TYPES = HeadPartTypes

    def get_modl(self):
        return self.get_value(path='Model\\MODL')

    def set_modl(self, value):
        return self.set_value(value, path='Model\\MODL', create_node=True)

    def del_modl(self):
        return self.delete(path='Model\\MODL')

    modl = property(fget=get_modl, fset=set_modl, fdel=del_modl)
    model_filename = modl

    def get_pnam(self):
        return self.TYPES(self.get_value(path='PNAM'))

    def set_pnam(self, headpart_type):
        return self.set_value(
                        headpart_type.value, path='PNAM', create_node=True)

    def del_pnam(self):
        return self.delete(path='PNAM')

    pnam = property(fget=get_pnam, fset=set_pnam, fdel=del_pnam)
    headpart_type = pnam

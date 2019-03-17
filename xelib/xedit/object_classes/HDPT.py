from xelib.xedit.base import XEditGenericObject


class XEditHeadPart(XEditGenericObject):
    SIGNATURE = 'HDPT'

    def get_modl(self):
        return self.get_value(path='Model\\MODL')

    def set_modl(self, value):
        return self.set_value(value, path='Model\\MODL', create_node=True)

    def del_modl(self):
        return self.delete(path='Model\\MODL')

    modl = property(fget=get_modl, fset=set_modl, fdel=del_modl)
    model_filename = modl

    def get_pnam(self):
        return self.get_value(path='Model\\MODL')

    def set_pnam(self, value):
        return self.set_value(value, path='Model\\MODL', create_node=True)

    def del_modl(self):
        return self.delete(path='Model\\MODL')

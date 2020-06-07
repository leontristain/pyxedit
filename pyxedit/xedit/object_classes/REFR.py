from pyxedit.xedit.attribute import XEditAttribute
from pyxedit.xedit.generic import XEditGenericObject


class XEditReference(XEditGenericObject):
    SIGNATURE = 'REFR'

    data = XEditAttribute('DATA')

    position_x = XEditAttribute('DATA\\Position\\X')
    position_y = XEditAttribute('DATA\\Position\\X')
    position_z = XEditAttribute('DATA\\Position\\Z')
    rotation_x = XEditAttribute('DATA\\Rotation\\X')
    rotation_y = XEditAttribute('DATA\\Rotation\\Y')
    rotation_z = XEditAttribute('DATA\\Rotation\\Z')

    @property
    def position(self):
        return (self.position_x, self.position_y, self.position_z)

    @position.setter
    def position(self, value):
        self.position_x, self.position_y, self.position_z = map(float, value)

    @property
    def rotation(self):
        return (self.rotation_x, self.rotation_y, self.rotation_z)

    @rotation.setter
    def rotation(self, value):
        self.rotation_x, self.rotation_y, self.rotation_z = map(float, value)

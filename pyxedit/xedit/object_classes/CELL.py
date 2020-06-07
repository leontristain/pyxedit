from pyxedit.xedit.attribute import XEditAttribute
from pyxedit.xedit.generic import XEditGenericObject


class XEditCell(XEditGenericObject):
    SIGNATURE = 'CELL'

    xclw = water_height = XEditAttribute('XCLW')
    xlcn = location = XEditAttribute('XLCN')
    xcmo = music_type = XEditAttribute('XCMO')

    @property
    def persistent(self):
        return self.child_group['Persistent']

    @property
    def temporary(self):
        return self.child_group['Temporary']

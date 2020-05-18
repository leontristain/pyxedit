from pyxedit.xedit.attribute import XEditAttribute
from pyxedit.xedit.generic import XEditGenericObject


class XEditGlobalVariable(XEditGenericObject):
    SIGNATURE = 'GLOB'

    fnam = type = XEditAttribute('FNAM')
    fltv = value = XEditAttribute('FLTV')

from pyxedit.xedit.attribute import XEditAttribute
from pyxedit.xedit.generic import XEditGenericObject


class XEditFormList(XEditGenericObject):
    SIGNATURE = 'FLST'

    lnam = items = XEditAttribute('LNAM')

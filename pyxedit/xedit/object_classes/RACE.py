from pyxedit.xedit.attribute import XEditAttribute
from pyxedit.xedit.generic import XEditGenericObject


class XEditRace(XEditGenericObject):
    SIGNATURE = 'RACE'

    wnam = skin = XEditAttribute('WNAM')
    kwda = keywords = XEditAttribute('KWDA')
    # to be continued

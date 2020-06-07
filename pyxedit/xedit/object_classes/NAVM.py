from pyxedit.xedit.attribute import XEditAttribute
from pyxedit.xedit.generic import XEditGenericObject


class XEditNavMesh(XEditGenericObject):
    SIGNATURE = 'NAVM'

    nvnm = geometry = XEditAttribute('NVNM')

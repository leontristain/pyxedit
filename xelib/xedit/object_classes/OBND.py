from xelib.xedit.base import XEditAttribute, XEditGenericObject


class XEditObjectBounds(XEditGenericObject):
    SIGNATURE = 'OBND'

    x1 = XEditAttribute('X1')
    y1 = XEditAttribute('Y1')
    z1 = XEditAttribute('Z1')
    x2 = XEditAttribute('X2')
    y2 = XEditAttribute('Y2')
    z2 = XEditAttribute('Z2')


from xelib.xedit.base import XEditAttribute, XEditGenericObject


class XEditArmor(XEditGenericObject):
    SIGNATURE = 'ARMO'

    obnd = object_bounds = XEditAttribute('OBND', read_only=True)
    full = full_name = XEditAttribute('FULL')
    eitm = enchantment = object_effect = XEditAttribute('EITM')
    eamt = enchantment_amount = XEditAttribute('EAMT')

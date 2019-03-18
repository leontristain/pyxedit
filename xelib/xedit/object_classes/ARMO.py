from xelib.xedit.base import XEditAttribute, XEditGenericObject


class XEditArmor(XEditGenericObject):
    SIGNATURE = 'ARMO'

    obnd = XEditAttribute('OBND', read_only=True)
    full = XEditAttribute('FULL')
    eitm = XEditAttribute('EITM')
    eamt = XEditAttribute('EAMT')

    # aliases
    object_bounds = obnd
    full_name = full
    object_effect = eitm
    enchantment = eitm
    enchantment_amount = eamt

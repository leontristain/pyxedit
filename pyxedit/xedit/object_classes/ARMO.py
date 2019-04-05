from pyxedit.xedit.attribute import XEditAttribute
from pyxedit.xedit.generic import XEditGenericObject


class XEditArmor(XEditGenericObject):
    SIGNATURE = 'ARMO'

    vmad = script_info = XEditAttribute('VMAD')
    obnd = object_bounds = XEditAttribute('OBND')
    full = full_name = XEditAttribute('FULL')
    eitm = enchantment = object_effect = XEditAttribute('EITM')
    eamt = enchantment_amount = XEditAttribute('EAMT')

    mod2 = male_model = XEditAttribute('MOD2')
    icon = male_inventory_image = XEditAttribute('ICON')
    mico = male_message_image = XEditAttribute('MICO')
    mod4 = female_model = XEditAttribute('MOD4')
    ico2 = female_inventory_image = XEditAttribute('ICO2')
    mic2 = female_message_image = XEditAttribute('MIC2')

    bodt = body_template_12byte = XEditAttribute('BODT')
    bod2 = body_template = XEditAttribute('BOD2')
    dest = destructible = destruction_data = XEditAttribute('DEST')

    ynam = pickup_sound = XEditAttribute('YNAM')
    znam = drop_sound = XEditAttribute('ZNAM')

    bmct = ragdoll_constraint_template = XEditAttribute('BMCT')
    etyp = equipment_type = equipment_slot = XEditAttribute('ETYP')
    bids = bash_impact_data_set = XEditAttribute('BIDS')
    bamt = bash_material = alternate_block_material = XEditAttribute('BAMT')
    rnam = race = XEditAttribute('RNAM')

    ksiz = keyword_count = XEditAttribute('KSIZ')
    kwda = keywords = XEditAttribute('KWDA')

    desc = description = XEditAttribute('DESC')
    modl = armature = XEditAttribute('MODL')
    data = XEditAttribute('DATA')
    dnam = armor_rating = XEditAttribute('DNAM')
    tnam = template = template_armor = XEditAttribute('TNAM')

from xelib.xedit.base import XEditAttribute, XEditGenericObject


class XEditArmature(XEditGenericObject):
    SIGNATURE = 'ARMA'

    bodt = body_template_12byte = XEditAttribute('BODT')
    bod2 = body_template = XEditAttribute('BOD2', read_only=True)
    rnam = race = XEditAttribute('RNAM')
    dnam = data = XEditAttribute('DNAM')
    mod2 = male_model = XEditAttribute('MOD2', read_only=True)
    mod3 = male_firstperson_model = XEditAttribute('MOD3', read_only=True)
    mod4 = female_model = XEditAttribute('MOD4', read_only=True)
    mod5 = female_firstperson_model = XEditAttribute('MOD5', read_only=True)
    nam0 = base_male_texture = male_skin_texture = XEditAttribute('NAM0')
    nam1 = base_female_texture = female_skin_texture = XEditAttribute('NAM1')
    nam2 = base_male_firstperson_texture = XEditAttribute('NAM2')
    nam3 = base_female_firstperson_texture = XEditAttribute('NAM3')
    modl = additional_races = included_races = XEditAttribute(
                                                   'MODL', read_only=True)
    sndd = footstep_sound = XEditAttribute('SNDD')
    onam = art_object = XEditAttribute('ONAM')

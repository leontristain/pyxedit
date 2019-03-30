from xedit.xedit.attribute import XEditAttribute
from xedit.xedit.generic import XEditGenericObject


def create_model_class(signature):
    # signature is expected to be something like `MOD2`, get the number on it
    n = int(signature[-1])

    # create a class
    class XEditArmatureModel(XEditGenericObject):
        pass

    # set up property for `MOD[n]` on the class
    attr_model = f'mod{n}'
    model_descriptor = XEditAttribute(attr_model.upper())
    setattr(XEditArmatureModel, attr_model, model_descriptor)
    setattr(XEditArmatureModel, 'model_filename', model_descriptor)

    # set up property for `MO[n]T` on the class
    attr_model_data = f'mo{n}t'
    model_data_descriptor = XEditAttribute(attr_model_data.upper())
    setattr(XEditArmatureModel, attr_model_data, model_data_descriptor)
    setattr(XEditArmatureModel, 'model_data', model_data_descriptor)

    # set up property for `MO[n]S` on the class
    attr_alt_textures = f'mo{n}s'
    alt_textures_descriptor = XEditAttribute(attr_alt_textures.upper())
    setattr(XEditArmatureModel, attr_alt_textures, alt_textures_descriptor)
    setattr(XEditArmatureModel, 'alternate_textures', alt_textures_descriptor)

    # return the class
    return XEditArmatureModel


class XEditArmature(XEditGenericObject):
    SIGNATURE = 'ARMA'

    bodt = body_template_12byte = XEditAttribute('BODT')
    bod2 = body_template = XEditAttribute('BOD2')
    rnam = race = XEditAttribute('RNAM')
    dnam = data = XEditAttribute('DNAM')

    mod2 = male_model = XEditAttribute(
        'MOD2', object_class=create_model_class('MOD2'))

    mod3 = male_firstperson_model = XEditAttribute(
        'MOD3', object_class=create_model_class('MOD3'))

    mod4 = female_model = XEditAttribute(
        'MOD4', object_class=create_model_class('MOD4'))

    mod5 = female_firstperson_model = XEditAttribute(
        'MOD5', object_class=create_model_class('MOD5'))

    nam0 = base_male_texture = male_skin_texture = XEditAttribute('NAM0')
    nam1 = base_female_texture = female_skin_texture = XEditAttribute('NAM1')
    nam2 = base_male_firstperson_texture = XEditAttribute('NAM2')
    nam3 = base_female_firstperson_texture = XEditAttribute('NAM3')

    modl = additional_races = included_races = XEditAttribute('MODL')
    sndd = footstep_sound = XEditAttribute('SNDD')
    onam = art_object = XEditAttribute('ONAM')

    @property
    def models(self):
        for item in [self.mod2, self.mod3, self.mod4, self.mod5]:
            if item:
                yield item

    @property
    def textures(self):
        for item in [self.nam0, self.nam1, self.nam2, self.nam3]:
            if item:
                yield item

    @property
    def file_paths(self):
        return [model.model_filename for model in self.models
                if model and model.model_filename]

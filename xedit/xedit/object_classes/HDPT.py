from enum import Enum

from xedit.xedit.attribute import XEditAttribute
from xedit.xedit.generic import XEditGenericObject


class HeadPartTypes(Enum):
    Misc = 'Misc'
    Face = 'Face'
    Eyes = 'Eyes'
    Hair = 'Hair'
    FacialHair = 'Facial Hair'
    Scar = 'Scar'
    Eyebrows = 'Eyebrows'


class XEditHeadPart(XEditGenericObject):
    SIGNATURE = 'HDPT'
    HeadPartTypes = HeadPartTypes

    full = full_name = XEditAttribute('FULL')
    modl = model_filename = XEditAttribute('Model\\MODL')
    data = flags = XEditAttribute('DATA')
    pnam = headpart_type = XEditAttribute('PNAM', enum=HeadPartTypes)
    hnam = extra_parts = XEditAttribute('HNAM')
    nam0 = parts = XEditAttribute('Parts')
    tnam = texture_set = base_texture = XEditAttribute('TNAM')
    cnam = color = XEditAttribute('CNAM')
    rnam = valid_races = resource_list = XEditAttribute('RNAM')

    @property
    def file_paths(self):
        files = ([self.model_filename] +
                 [part['NAM1'].value for part in self.parts])
        return sorted(set([file_ for file_ in files if file_]))

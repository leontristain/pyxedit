from enum import Enum

from xelib.xedit.base import XEditAttribute, XEditGenericObject


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

    full = XEditAttribute('FULL')
    modl = XEditAttribute('Model\\MODL')
    data = XEditAttribute('DATA', read_only=True)
    pnam = XEditAttribute('PNAM', enum=HeadPartTypes)
    parts = XEditAttribute('Parts', read_only=True)
    tnam = XEditAttribute('TNAM', read_only=True)
    rnam = XEditAttribute('RNAM', read_only=True)

    # aliases
    full_name = full
    model_filename = modl
    flags = data
    headpart_type = pnam
    texture_set = tnam
    valid_races = rnam

    @property
    def file_paths(self):
        with self.manage_handles():
            files = [part['NAM1'].value for part in self.parts]
        return [file_ for file_ in files if file_]

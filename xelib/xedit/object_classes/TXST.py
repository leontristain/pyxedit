from xelib.xedit.attribute import XEditAttribute
from xelib.xedit.generic import XEditGenericObject


class XEditTextureSet(XEditGenericObject):
    SIGNATURE = 'TXST'

    obnd = XEditAttribute('OBND', read_only=True)
    tx00 = XEditAttribute('Textures (RGB/A)\\TX00')
    tx01 = XEditAttribute('Textures (RGB/A)\\TX01')
    tx02 = XEditAttribute('Textures (RGB/A)\\TX02')
    tx03 = XEditAttribute('Textures (RGB/A)\\TX03')
    tx04 = XEditAttribute('Textures (RGB/A)\\TX04')
    tx05 = XEditAttribute('Textures (RGB/A)\\TX05')
    tx06 = XEditAttribute('Textures (RGB/A)\\TX06')
    tx07 = XEditAttribute('Textures (RGB/A)\\TX07')

    # aliases
    object_bounds = obnd

    @property
    def texture_paths(self):
        '''
        Return the list of all texture paths.
        '''
        return [self.tx00, self.tx01, self.tx02, self.tx03,
                self.tx04, self.tx05, self.tx06, self.tx07]

    @property
    def file_paths(self):
        '''
        Return a list of all file paths currently associated with this record
        '''
        return [path for path in self.texture_paths if path]

from collections import namedtuple
import pytest

from xelib import XelibError

from . fixtures import xelib  # NOQA: for pytest


class TestElementValues:
    def get_data(self, xelib):
        test_data = namedtuple('TestData', 'xt2 file_flags armo rec element '
                                           'keyword child_group block '
                                           'sub_block persistent_group '
                                           'refr refr_flags')

        xt2 = xelib.get_element(0, path='xtest-2.esp')
        file_flags = xelib.get_element(
            xt2, 'File Header\\Record Header\\Record Flags')
        armo = xelib.get_element(xt2, path='ARMO')
        rec = xelib.get_element(armo, path='00012E46')
        element = xelib.get_element(rec, path='DNAM')
        keyword = xelib.get_element(rec, 'KWDA\\[1]')
        child_group = xelib.get_element(xt2, path='00027D1C\\Child Group')
        block = xelib.get_element(xt2, path='CELL\\[0]')
        sub_block = xelib.get_element(block, path='[0]')
        persistent_group = xelib.get_element(child_group, path='[0]')
        refr = xelib.get_element(xt2, '000170F0')
        refr_flags = xelib.get_element(refr, 'Record Header\\Record Flags')

        return test_data(xt2=xt2,
                         file_flags=file_flags,
                         armo=armo,
                         rec=rec,
                         element=element,
                         keyword=keyword,
                         child_group=child_group,
                         block=block,
                         sub_block=sub_block,
                         persistent_group=persistent_group,
                         refr=refr,
                         refr_flags=refr_flags)

    def test_group_names(self, xelib):
        data = self.get_data(xelib)

        # should resolve file names
        assert xelib.name(data.xt2) == 'xtest-2.esp'

        # should resolve top-level group names
        assert xelib.name(data.armo) == 'Armor'

        # should resolve block names
        assert xelib.name(data.block) == 'Block 0'

        # should resolve sub-block names
        assert xelib.name(data.sub_block) == 'Sub-Block 0'

        # should resolve child group names
        assert xelib.name(data.child_group) == 'Children of 00027D1C'

        # should resolve persistent/temporary group names
        assert xelib.name(data.persistent_group) == 'Persistent'

    def test_record_names(self, xelib):
        data = self.get_data(xelib)

        # should resolve FULL name, if present
        assert xelib.name(data.rec) == 'Iron Gauntlets'

        # should resolve Editor ID, if present
        assert xelib.name(data.refr) == 'ITPOTest'

        # should resolve context for cells with no EDID or FULL
        h = xelib.get_element(0, path='Update.esm\\00038381')
        assert xelib.name(h) == '"Windhelm" <32,9>'

        # should resolve context for placements with no EDID
        h = xelib.get_element(0, path='Update.esm\\0003F70F')
        assert xelib.name(h) == 'Places "Chest" in "Skyrim" <0,0>'

    def test_element_names(self, xelib):
        data = self.get_data(xelib)

        # should resolve element names
        assert xelib.name(data.element) == 'DNAM - Armor Rating'

    def test_display_name(self, xelib):
        data = self.get_data(xelib)

        # should include filename
        assert 'xtest-2.esp' in xelib.display_name(data.xt2)

        # should include load order
        assert '[06]' in xelib.display_name(data.xt2)

        # should format hardcoded dat names properly
        h = xelib.get_element(0, path='Skyrim.Hardcoded.dat', ex=True)
        assert xelib.display_name(h) == '[00] Skyrim.exe'

    def test_path(self, xelib):
        data = self.get_data(xelib)

        # should resolve file names
        assert xelib.long_path(data.xt2) == 'xtest-2.esp'

        # should resolve group signatures
        assert xelib.long_path(data.armo) == 'xtest-2.esp\\ARMO'

        # should resolve block names
        assert xelib.long_path(data.block) == 'xtest-2.esp\\CELL\\Block 0'

        # should resolve sub-block names
        assert (xelib.long_path(data.sub_block) ==
                    'xtest-2.esp\\CELL\\Block 0\\Sub-Block 0')

        # should resolve child groups
        assert (xelib.path(data.child_group) ==
                    'xtest-2.esp\\00027D1C\\Child Group')

        # should resolve temporary/persistent groups
        assert (xelib.path(data.persistent_group) ==
                    'xtest-2.esp\\00027D1C\\Child Group\\Persistent')

        # should resolve record FormIDs
        assert xelib.path(data.refr) == 'xtest-2.esp\\000170F0'

        # should resolve file headers
        assert (xelib.long_path(data.file_flags) ==
                    'xtest-2.esp\\File Header\\Record Header\\Record Flags')

        # should resolve element names
        assert (xelib.path(data.element) ==
                    'xtest-2.esp\\00012E46\\DNAM - Armor Rating')

        # should resolve array element indexes
        assert (xelib.path(data.keyword) ==
                    'xtest-2.esp\\00012E46\\KWDA - Keywords\\[1]')

    def test_signature(self, xelib):
        data = self.get_data(xelib)

        # should fail if a file is passed
        with pytest.raises(XelibError):
            xelib.signature(data.xt2)

        # should fail if an element with no signature is passed
        with pytest.raises(XelibError):
            xelib.signature(data.keyword)

        # should resolve group signatures
        assert xelib.signature(data.block) == 'GRUP'
        assert xelib.signature(data.sub_block) == 'GRUP'
        assert xelib.signature(data.child_group) == 'GRUP'
        assert xelib.signature(data.persistent_group) == 'GRUP'
        assert xelib.signature(data.armo) == 'ARMO'

        # should resolve record signatures
        assert xelib.signature(data.rec) == 'ARMO'
        assert xelib.signature(data.refr) == 'REFR'

        # should resolve element signatures
        assert xelib.signature(data.element) == 'DNAM'

    def test_get_value(self, xelib):
        data = self.get_data(xelib)

        # should resolve element values
        assert xelib.get_value(data.element) == '10.000000'
        assert xelib.get_value(data.keyword) == 'ArmorHeavy [KYWD:0006BBD2]'

        # should resolve element value at path
        assert xelib.get_value(data.rec, path='OBND\\X1') == '-11'
        assert (xelib.get_value(data.rec, path='KWDA\\[1]') ==
                    'ArmorHeavy [KYWD:0006BBD2]')
        assert (xelib.get_value(data.rec, path='Female world model\\MOD4') ==
                    'Test')

        # should fail depending on ex=True/False if path does not exist
        with pytest.raises(XelibError):
            xelib.get_value(data.rec, path='Non\\Existent\\Path', ex=True)
        assert not xelib.get_value(data.rec, path='Non\\Existent\\Path')

    def test_get_int_value(self, xelib):
        data = self.get_data(xelib)

        # should resolve element integer values
        h = xelib.get_element(data.rec, path='OBND\\Y1')
        assert xelib.get_int_value(h), -15

        # should resolve element integer values at paths
        assert xelib.get_int_value(data.rec, path='OBND\\Z1') == -1

        # should fail depending on ex=True/False if path does not exist
        with pytest.raises(XelibError):
            xelib.get_int_value(data.rec, path='Non\\Existent\\Path', ex=True)
        assert not xelib.get_int_value(data.rec, path='Non\\Existent\\Path')

    def test_get_uint_value(self, xelib):
        data = self.get_data(xelib)

        # should resolve element unsigned integer values
        assert xelib.get_uint_value(data.keyword) == 0x6bbd2

        # should resolve element unsigned integer values at paths
        assert xelib.get_uint_value(data.rec, path='KWDA\\[0]') == 0x424ef

        # should fail depending on ex=True/False if path does not exist
        with pytest.raises(XelibError):
            xelib.get_uint_value(data.rec, path='Non\\Existent\\Path', ex=True)
        assert not xelib.get_uint_value(data.rec, path='Non\\Existent\\Path')

    def test_get_float_value(self, xelib):
        data = self.get_data(xelib)

        # should resolve element float values
        assert xelib.get_float_value(data.element) == 1000.0

        # should resolve element float values at paths
        assert (xelib.get_float_value(data.rec, path='DATA\\Weight') ==
                    pytest.approx(5.0))

        # should fail depending on ex=True/False if path does not exist
        with pytest.raises(XelibError):
            xelib.get_float_value(data.rec, path='Non\\Existent\\Path', ex=True)
        assert not xelib.get_float_value(data.rec, path='Non\\Existent\\Path')

    def test_set_value(self, xelib):
        data = self.get_data(xelib)

        # should set element values
        xelib.set_value(data.element, '14.100000')
        assert xelib.get_value(data.element) == '14.100000'

        xelib.set_value(data.keyword, 'ArmorLight [KYWD:0006BBD3]')
        assert xelib.get_value(data.keyword) == 'ArmorLight [KYWD:0006BBD3]'

        # should set element value at path
        xelib.set_value(data.rec, '-8', path='OBND\\X1')
        assert xelib.get_value(data.rec, path='OBND\\X1') == '-8'

        xelib.set_value(data.rec,
                        'PerkFistsEbony [KYWD:0002C178]',
                        path='KWDA\\[0]')
        assert (xelib.get_value(data.rec, path='KWDA\\[0]') ==
                    'PerkFistsEbony [KYWD:0002C178]')

        xelib.set_value(data.rec,
                        'Armor\\Iron\\F\\GauntletsGND.nif',
                        path='Female world model\\MOD4')
        assert (xelib.get_value(data.rec, path='Female world model\\MOD4') ==
                    'Armor\\Iron\\F\\GauntletsGND.nif')

        # should fail if path does not exist
        with pytest.raises(XelibError):
            xelib.set_value(data.rec, 'Test', path='Non\\Existent\\Path')

    def test_set_int_value(self, xelib):
        data = self.get_data(xelib)

        # should set element integer values
        h = xelib.get_element(data.rec, 'OBND\\Y1')
        xelib.set_int_value(h, -13)
        assert xelib.get_int_value(h) == -13

        # should set element integer values at paths
        xelib.set_int_value(data.rec, -4, path='OBND\\Z1')
        assert xelib.get_int_value(data.rec, path='OBND\\Z1') == -4

        # should fail if path does not exist
        with pytest.raises(XelibError):
            xelib.set_int_value(data.rec, 1, path='Non\\Existent\\Path')

    def test_set_uint_value(self, xelib):
        data = self.get_data(xelib)

        # should set element unsigned integer values
        xelib.set_uint_value(data.keyword, 0x6bbe2)
        assert xelib.get_uint_value(data.keyword) == 0x6bbe2

        # should set element unsigned integer values at paths
        xelib.set_uint_value(data.rec, 0x2c177, path='KWDA\\[0]')
        assert xelib.get_uint_value(data.rec, path='KWDA\\[0]') == 0x2c177

        # should work with version control info
        # TODO: this test case is currently a xedit-lib known failure
        # xelib.set_uint_value(data.rec,
        #                      0x1234,
        #                      path='Record Header\\Version Control Info 1')
        # assert xelib.get_uint_value(
        #     data.rec, path='Record Header\\Version Control Info 1') == 0x1234

        # should fail if path does not exist
        with pytest.raises(XelibError):
            xelib.set_uint_value(data.rec, 0x10, path='Non\\Existent\\Path')

    def test_set_float_value(self, xelib):
        data = self.get_data(xelib)

        # should resolve element float values
        xelib.set_float_value(data.element, 1920.0)
        assert xelib.get_float_value(data.element) == 1920.0

        # should resolve element float at paths
        xelib.set_float_value(data.rec, 7.3, path='DATA\\Weight')
        assert (xelib.get_float_value(data.rec, path='DATA\\Weight') ==
                    pytest.approx(7.3))

        # should fail if path does not exist
        with pytest.raises(XelibError):
            xelib.set_float_value(data.rec, 1.23, path='Non\\Existent\\Path')

    def test_get_flag(self, xelib):
        data = self.get_data(xelib)

        # should return false for disabled flags
        assert xelib.get_flag(data.file_flags, '', 'ESM') is False
        assert xelib.get_flag(data.file_flags, '', 'Localized') is False
        assert xelib.get_flag(data.file_flags, '', '') is False
        assert xelib.get_flag(data.refr_flags, '', 'Deleted') is False
        assert xelib.get_flag(data.refr_flags, '', 'Ignored') is False
        assert xelib.get_flag(data.refr_flags, '', 'Unknown 0') is False

        # should return true for enabled flags
        assert xelib.get_flag(
                   0,
                   'xtest-1.esp\\File Header\\Record Header\\Record Flags',
                   'ESM') is True
        assert xelib.get_flag(
                   data.rec,
                   'BODT\\First Person Flags',
                   '33 - Hands') is True
        assert xelib.get_flag(data.refr_flags, '', 'Persistent') is True
        assert xelib.get_flag(data.refr_flags, '', 'Initially Disabled') is True

        # should fail if flag is not found
        with pytest.raises(XelibError):
            xelib.get_flag(data.refr_flags, '', 'Temporary')
        with pytest.raises(XelibError):
            xelib.get_flag(data.refr_flags, '', 'Unknown 5')

        # should fail on elements that do not have flags
        with pytest.raises(XelibError):
            xelib.get_flag(data.xt2, '', 'ESM')
        with pytest.raises(XelibError):
            xelib.get_flag(data.xt2, 'File Header', 'ESM')
        with pytest.raises(XelibError):
            xelib.get_flag(data.refr, '', 'Deleted')
        with pytest.raises(XelibError):
            xelib.get_flag(data.refr, 'Record Header', 'Deleted')

    def test_set_flag(self, xelib):
        data = self.get_data(xelib)

        # should enable disabled flags
        assert xelib.get_flag(data.file_flags, '', 'Localized') is False
        xelib.set_flag(data.file_flags, '', 'Localized', True)
        assert xelib.get_flag(data.file_flags, '', 'Localized') is True

        # TODO: This test causes issues later on for some reason (disabled
        # in xedit-lib tests)
        # assert xelib.get_flag(data.refr_flags, '', 'Deleted') is False
        # xelib.set_flag(data.refr_flags, '', 'Deleted', True)
        # assert xelib.get_flag(data.refr_flags, '', 'Deleted') is True

        assert xelib.get_flag(data.refr_flags, '', 'Ignored') is False
        xelib.set_flag(data.refr_flags, '', 'Ignored', True)
        assert xelib.get_flag(data.refr_flags, '', 'Ignored') is True

        assert xelib.get_flag(
                   data.rec, 'BODT\\First Person Flags', '32 - Body') is False
        xelib.set_flag(data.rec, 'BODT\\First Person Flags', '32 - Body', True)
        assert xelib.get_flag(
                   data.rec, 'BODT\\First Person Flags', '32 - Body') is True

        # should disable enabled flags
        assert xelib.get_flag(data.file_flags, '', 'Localized') is True
        xelib.set_flag(data.file_flags, '', 'Localized', False)
        assert xelib.get_flag(data.file_flags, '', 'Localized') is False

        # TODO: This test causes issues later on for some reason (disabled
        # in xedit-lib tests)
        # assert xelib.get_flag(data.refr_flags, '', 'Deleted') is True
        # xelib.set_flag(data.refr_flags, '', 'Deleted', False)
        # assert xelib.get_flag(data.refr_flags, '', 'Deleted') is False

        assert xelib.get_flag(data.refr_flags, '', 'Ignored') is True
        xelib.set_flag(data.refr_flags, '', 'Ignored', False)
        assert xelib.get_flag(data.refr_flags, '', 'Ignored') is False

        assert xelib.get_flag(
                   data.rec, 'BODT\\First Person Flags', '32 - Body') is True
        xelib.set_flag(data.rec, 'BODT\\First Person Flags', '32 - Body', False)
        assert xelib.get_flag(
                   data.rec, 'BODT\\First Person Flags', '32 - Body') is False

        # should fail if flag is not found
        with pytest.raises(XelibError):
            xelib.set_flag(data.refr_flags, '', 'Temporary', True)
        with pytest.raises(XelibError):
            xelib.set_flag(data.refr_flags, '', 'Unknown 5', False)

        # should fail on elements that do not have flags
        with pytest.raises(XelibError):
            xelib.set_flag(data.xt2, '', 'ESM', True)
        with pytest.raises(XelibError):
            xelib.set_flag(data.xt2, 'File Header', 'ESM', True)
        with pytest.raises(XelibError):
            xelib.set_flag(data.refr, '', 'Deleted', True)
        with pytest.raises(XelibError):
            xelib.set_flag(data.refr, 'Record Header', 'Deleted', True)

    def test_get_enabled_flags(self, xelib):
        data = self.get_data(xelib)

        # should return empty if no flags are enabled
        assert xelib.get_enabled_flags(data.file_flags) == []

        # should return enabled flag names for enabled flags
        assert (
            xelib.get_enabled_flags(
                0, 'xtest-1.esp\\File Header\\Record Header\\Record Flags') ==
            ['ESM'])
        assert (
            xelib.get_enabled_flags(data.rec, 'BODT\\First Person Flags') ==
            ['33 - Hands'])
        assert (
            xelib.get_enabled_flags(data.refr_flags, '') ==
            ['Persistent', 'Initially Disabled'])

        # should fail on elements that do not have flags
        with pytest.raises(XelibError):
            xelib.get_enabled_flags(data.xt2, '')
        with pytest.raises(XelibError):
            xelib.get_enabled_flags(data.xt2, 'File Header')
        with pytest.raises(XelibError):
            xelib.get_enabled_flags(data.refr, '')
        with pytest.raises(XelibError):
            xelib.get_enabled_flags(data.refr, 'Record Header')

    def test_set_enabled_flags(self, xelib):
        data = self.get_data(xelib)

        # should enable flags that are present
        assert xelib.get_enabled_flags(data.file_flags, '') == []
        xelib.set_enabled_flags(
                  data.file_flags, '', ['ESM', 'Localized', 'Ignored'])
        assert (xelib.get_enabled_flags(data.file_flags, '') ==
                    ['ESM', 'Localized', 'Ignored'])

        assert (xelib.get_enabled_flags(data.refr_flags, '') ==
                    ['Persistent', 'Initially Disabled'])
        xelib.set_enabled_flags(
                  data.refr_flags, '', ['Unknown 1',
                                        'Persistent',
                                        'Initially Disabled',
                                        'Ignored',
                                        'Multibound'])
        assert (xelib.get_enabled_flags(data.refr_flags, '') ==
                    ['Unknown 1',
                     'Persistent',
                     'Initially Disabled',
                     'Ignored',
                     'Multibound'])

        assert (xelib.get_enabled_flags(data.rec, 'BODT\\First Person Flags') ==
                ['33 - Hands'])
        xelib.set_enabled_flags(data.rec,
                                'BODT\\First Person Flags',
                                ['30 - Head',
                                 '33 - Hands',
                                 '40 - Tail',
                                 '52 - Unnamed',
                                 '61 - FX01'])
        assert (xelib.get_enabled_flags(data.rec, 'BODT\\First Person Flags') ==
                ['30 - Head',
                 '33 - Hands',
                 '40 - Tail',
                 '52 - Unnamed',
                 '61 - FX01'])

        # should disable flags that are not present
        assert (xelib.get_enabled_flags(data.file_flags, '') ==
                    ['ESM', 'Localized', 'Ignored'])
        xelib.set_enabled_flags(data.file_flags, '', [])
        assert xelib.get_enabled_flags(data.file_flags, '') == []

        assert (xelib.get_enabled_flags(data.refr_flags, '') ==
                    ['Unknown 1',
                     'Persistent',
                     'Initially Disabled',
                     'Ignored',
                     'Multibound'])
        xelib.set_enabled_flags(
                  data.refr_flags, '', ['Persistent', 'Initially Disabled'])
        assert (xelib.get_enabled_flags(data.refr_flags, '') ==
                    ['Persistent', 'Initially Disabled'])

        assert (xelib.get_enabled_flags(data.rec, 'BODT\\First Person Flags') ==
                ['30 - Head',
                 '33 - Hands',
                 '40 - Tail',
                 '52 - Unnamed',
                 '61 - FX01'])
        xelib.set_enabled_flags(data.rec,
                                'BODT\\First Person Flags',
                                ['33 - Hands'])
        assert (xelib.get_enabled_flags(data.rec, 'BODT\\First Person Flags') ==
                ['33 - Hands'])

        # should fail on elements that do not have flags
        with pytest.raises(XelibError):
            xelib.set_enabled_flags(data.xt2, '', [])
        with pytest.raises(XelibError):
            xelib.set_enabled_flags(data.xt2, 'File Header', [])
        with pytest.raises(XelibError):
            xelib.set_enabled_flags(data.refr, '', [])
        with pytest.raises(XelibError):
            xelib.set_enabled_flags(data.refr, 'Record Header', [])

    def test_get_all_flags(self, xelib):
        data = self.get_data(xelib)

        # should return list of flag names, empty flags included
        assert xelib.get_all_flags(data.file_flags) == [
            'ESM', '', '', '', '', '', '',
            'Localized', '', '', '', '',
            'Ignored', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
            '', '', '', '', '']

        assert xelib.get_all_flags(data.refr_flags) == [
            'Unknown 0', 'Unknown 1', 'Unknown 2', 'Unknown 3', 'Unknown 4',
            'Deleted',
            'Unknown 6', 'Unknown 7', 'Unknown 8',
            'Hidden From Local Map',
            'Persistent',
            'Initially Disabled',
            'Ignored',
            'Unknown 13', 'Unknown 14',
            'Visible when distant',
            'Is Full LOD',
            'Unknown 17', 'Unknown 18', 'Unknown 19', 'Unknown 20',
            'Unknown 21', 'Unknown 22', 'Unknown 23', 'Unknown 24',
            'Unknown 25',
            'Filter (Collision Geometry)',
            'Bounding Box (Collision Geometry)',
            'Reflected By Auto Water',
            "Don't Havok Settle",
            'No Respawn',
            'Multibound']

        assert xelib.get_all_flags(
                   data.rec, path='BODT\\First Person Flags') == [
                       '30 - Head',
                       '31 - Hair',
                       '32 - Body',
                       '33 - Hands',
                       '34 - Forearms',
                       '35 - Amulet',
                       '36 - Ring',
                       '37 - Feet',
                       '38 - Calves',
                       '39 - Shield',
                       '40 - Tail',
                       '41 - LongHair',
                       '42 - Circlet',
                       '43 - Ears',
                       '44 - Unnamed',
                       '45 - Unnamed',
                       '46 - Unnamed',
                       '47 - Unnamed',
                       '48 - Unnamed',
                       '49 - Unnamed',
                       '50 - DecapitateHead',
                       '51 - Decapitate',
                       '52 - Unnamed',
                       '53 - Unnamed',
                       '54 - Unnamed',
                       '55 - Unnamed',
                       '56 - Unnamed',
                       '57 - Unnamed',
                       '58 - Unnamed',
                       '59 - Unnamed',
                       '60 - Unnamed',
                       '61 - FX01']

        # should fail on elements that do not have flags
        with pytest.raises(XelibError):
            xelib.get_all_flags(data.xt2)
        with pytest.raises(XelibError):
            xelib.get_all_flags(data.xt2, path='File Header')
        with pytest.raises(XelibError):
            xelib.get_all_flags(data.refr)
        with pytest.raises(XelibError):
            xelib.get_all_flags(data.refr, path='Record Header')

    def test_signature_from_name(self, xelib):
        # should succeed for top-level record names
        assert xelib.signature_from_name('Armor') == 'ARMO'
        assert xelib.signature_from_name('Weapon') == 'WEAP'
        assert xelib.signature_from_name('Cell') == 'CELL'
        assert xelib.signature_from_name('Non-Player Character (Actor)') == 'NPC_'
        assert xelib.signature_from_name('Constructible Object') == 'COBJ'
        assert xelib.signature_from_name('Explosion') == 'EXPL'
        assert xelib.signature_from_name('Word of Power') == 'WOOP'

        # should succeed for other names
        assert xelib.signature_from_name('Placed Object') == 'REFR'
        assert xelib.signature_from_name('Navigation Mesh') == 'NAVM'
        assert xelib.signature_from_name('Placed NPC') == 'ACHR'
        assert xelib.signature_from_name('Placed Projectile') == 'PGRE'
        assert xelib.signature_from_name('Placed Missile') == 'PMIS'
        assert xelib.signature_from_name('Placed Arrow') == 'PARW'
        assert xelib.signature_from_name('Placed Beam') == 'PBEA'
        assert xelib.signature_from_name('Placed Flame') == 'PFLA'
        assert xelib.signature_from_name('Placed Cone/Voice') == 'PCON'
        assert xelib.signature_from_name('Placed Barrier') == 'PBAR'
        assert xelib.signature_from_name('Placed Hazard') == 'PHZD'
        assert xelib.signature_from_name('HAIR') == 'HAIR'

        # should fail if name does not correspond to a signature
        with pytest.raises(XelibError):
            xelib.signature_from_name('')
        with pytest.raises(XelibError):
            xelib.signature_from_name('This is fake')
        with pytest.raises(XelibError):
            xelib.signature_from_name('ArMoR')
        with pytest.raises(XelibError):
            xelib.signature_from_name('Constructible')
        with pytest.raises(XelibError):
            xelib.signature_from_name('Explosion=')

    def test_name_from_signature(self, xelib):
        # should succeed for top-level record names
        assert xelib.name_from_signature('ARMO') == 'Armor'
        assert xelib.name_from_signature('WEAP') == 'Weapon'
        assert xelib.name_from_signature('CELL') == 'Cell'
        assert xelib.name_from_signature('NPC_') == 'Non-Player Character (Actor)'
        assert xelib.name_from_signature('COBJ') == 'Constructible Object'
        assert xelib.name_from_signature('EXPL') == 'Explosion'
        assert xelib.name_from_signature('WOOP') == 'Word of Power'

        # should succeed for other names
        assert xelib.name_from_signature('REFR') == 'Placed Object'
        assert xelib.name_from_signature('NAVM') == 'Navigation Mesh'
        assert xelib.name_from_signature('ACHR') == 'Placed NPC'
        assert xelib.name_from_signature('PGRE') == 'Placed Projectile'
        assert xelib.name_from_signature('PMIS') == 'Placed Missile'
        assert xelib.name_from_signature('PARW') == 'Placed Arrow'
        assert xelib.name_from_signature('PBEA') == 'Placed Beam'
        assert xelib.name_from_signature('PFLA') == 'Placed Flame'
        assert xelib.name_from_signature('PCON') == 'Placed Cone/Voice'
        assert xelib.name_from_signature('PBAR') == 'Placed Barrier'
        assert xelib.name_from_signature('PHZD') == 'Placed Hazard'
        assert xelib.name_from_signature('HAIR') == 'HAIR'

        # should fail if name does not correspond to a signature
        with pytest.raises(XelibError):
            xelib.name_from_signature('')
        with pytest.raises(XelibError):
            xelib.name_from_signature('FAKE')
        with pytest.raises(XelibError):
            xelib.name_from_signature('armo')
        with pytest.raises(XelibError):
            xelib.name_from_signature('COBJ_')
        with pytest.raises(XelibError):
            xelib.name_from_signature('NPC')

    def test_get_signature_name_map(self, xelib):
        signature_name_map = xelib.get_signature_name_map()
        assert signature_name_map['ARMO'] == 'Armor'
        assert signature_name_map['REFR'] == 'Placed Object'
        assert signature_name_map['PHZD'] == 'Placed Hazard'
        assert signature_name_map['PWAT'] == 'PWAT'
        assert signature_name_map['NPC_'] == 'Non-Player Character (Actor)'

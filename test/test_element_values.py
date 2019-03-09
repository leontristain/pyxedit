from collections import namedtuple
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

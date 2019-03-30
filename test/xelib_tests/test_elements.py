from collections import namedtuple
import functools
import pytest

from xedit import XelibError

from . fixtures import xelib  # NOQA: for pytest


class TestElements:
    def get_data(self, xelib):
        test_data = namedtuple('TestData', 'skyrim armo1 ar1 keywords keyword '
                                           'dnam ar2 armature xt3 xt4 xt5 '
                                           'armo2 ar3 refr lvli entries')

        skyrim = xelib.get_element(0, path='Skyrim.esm')
        armo1 = xelib.get_element(skyrim, path='ARMO')
        ar1 = xelib.get_element(armo1, path='00012E46')
        keywords = xelib.get_element(ar1, path='KWDA')
        keyword = xelib.get_element(keywords, path='[0]')
        dnam = xelib.get_element(ar1, path='DNAM')
        ar2 = xelib.get_element(0, path='xtest-2.esp\\00012E46')
        armature = xelib.get_element(ar2, path='Armature')
        xt3 = xelib.get_element(0, path='xtest-3.esp')
        xt4 = xelib.get_element(0, path='xtest-4.esp')
        xt5 = xelib.get_element(0, path='xtest-5.esp')
        armo2 = xelib.get_element(xt3, path='ARMO')
        ar3 = xelib.get_element(armo2, path='00012E46')
        refr = xelib.get_element(0, path='xtest-2.esp\\000170F0')
        lvli = xelib.get_element(0, path='xtest-2.esp\\00013739')
        entries = xelib.get_element(lvli, path='Leveled List Entries')

        return test_data(skyrim=skyrim,
                         armo1=armo1,
                         ar1=ar1,
                         keywords=keywords,
                         keyword=keyword,
                         dnam=dnam,
                         ar2=ar2,
                         armature=armature,
                         xt3=xt3,
                         xt4=xt4,
                         xt5=xt5,
                         armo2=armo2,
                         ar3=ar3,
                         refr=refr,
                         lvli=lvli,
                         entries=entries)

    def test_has_element(self, xelib):
        data = self.get_data(xelib)

        # should return true for files that exist
        assert xelib.has_element(0, path='Skyrim.esm')

        # should return true for elements that exist
        assert xelib.has_element(data.ar1, path='Male world model')

        # should return true for handles that are assigned
        assert xelib.has_element(data.ar1, path='')

        # should return false for files that do not exist
        assert not xelib.has_element(0, 'NonExistingFile.esp')

        # should return false for elements that do not exist
        assert not xelib.has_element(data.ar1, 'KWDA\\[5]')

        # should fail if the handle is not assigned
        with pytest.raises(XelibError):
            xelib.has_element(0xffffff, path='')

    def test_get_element(self, xelib):
        data = self.get_data(xelib)
        get_element = functools.partial(xelib.get_element, ex=True)

        # should return a handle if the index is in bounds
        assert get_element(0, path='[0]',)

        # should fail if index is out of bounds
        with pytest.raises(XelibError):
            get_element(0, path='[-9]')

        # should return a handle if matching file is loaded
        assert get_element(0, path='Skyrim.esm')

        # should fail if matching file is not loaded
        with pytest.raises(XelibError):
            get_element(0, path='NonExistingPlugin.esp')

        # should return a handle if the index is in bounds
        assert get_element(data.skyrim, path='[0]')

        # should fail if index is out of bounds
        with pytest.raises(XelibError):
            get_element(data.skyrim, path='[-9]')

        # should return a handle if the group signature exists
        assert get_element(data.skyrim, path='ARMO')

        # should fail if group signature does not exist
        with pytest.raises(XelibError):
            get_element(data.skyrim, path='ABCD')

        # should return a handle if the group name exists
        assert get_element(data.skyrim, path='Armor')

        # should fail if group name does not exist
        with pytest.raises(XelibError):
            get_element(data.xt3, path='Ammunition')

        # should return a handle if the group exists (block/sub-block)
        assert get_element(
                   data.skyrim, path='0000003C\\Child Group\\Block -1, 0')
        assert get_element(
                   data.skyrim, path='0000003C\\Child Group\\Block -1, 0\\'
                                     'Sub-block -1, 0')
        assert get_element(data.skyrim, path='CELL\\Block 0')
        assert get_element(data.skyrim, path='CELL\\Block 0\\Sub-Block 0')

        # should fail if the group does not exist (block/sub-block)
        with pytest.raises(XelibError):
            get_element(data.skyrim, path='0000003C\\Child Group\\Block -99, 99')
        with pytest.raises(XelibError):
            get_element(data.skyrim, path='0000003C\\Child Group\\Block -1, 0\\'
                                          'Sub-block -99, 99')
        with pytest.raises(XelibError):
            get_element(data.skyrim, path='CELL\\Block 10')
        with pytest.raises(XelibError):
            get_element(data.skyrim, path='CELL\\Block 0\\Sub-Block 10')

        # should return a handle if the group exists (temp/persistent groups)
        assert get_element(data.skyrim, path='00027D1C\\Child Group\\Temporary')
        assert get_element(data.skyrim, path='00027D1C\\Child Group\\Persistent')

        # should fail if the group does not exist (temp/persistent groups)
        with pytest.raises(XelibError):
            get_element(data.skyrim, path='000094BD\\Child Group\\Persistent')

        # should return a handle if the record exists (by FormID)
        assert get_element(data.skyrim, path='00012E46')

        # should fail if the record does not exist (by FormID)
        with pytest.raises(XelibError):
            get_element(data.skyrim, path='00FFFFFF')

        # should return a handle if the record exists (by FileFormID)
        assert get_element(data.xt4, path='&03000802')
        assert get_element(data.xt4, path='&02000800')

        # should fail if the record does not exist (by FileFormID)
        with pytest.raises(XelibError):
            get_element(data.xt4, path='&03FFFFFF')

        # should return a handle if the record exists (by EditorID)
        assert get_element(data.xt3, path='ArmorIronGauntlets')

        # should fail if the record does not exist (by EditorID)
        with pytest.raises(XelibError):
            get_element(data.xt3, path='NonExistentEditorID')

        # should return a handle if the record exists (by Name)
        assert get_element(data.xt3, path='"Iron Gauntlets"')

        # should fail if the record does not exist (by Name)
        with pytest.raises(XelibError):
            get_element(data.xt3, path='"U. N. Owen"')

        # should return a handle if the record exists (group, FormID)
        assert get_element(data.armo1, path='00012E46')

        # should fail if the record does not exist (group, FormID)
        with pytest.raises(XelibError):
            get_element(data.armo1, path='00000000')

        # should return a handle if the index is in bounds
        assert get_element(data.ar1, path='[0]')

        # should fail if index is out of bounds
        with pytest.raises(XelibError):
            get_element(data.ar1, path='[-9]')
        with pytest.raises(XelibError):
            get_element(data.ar1, path='[99999]')

        # should return a handle if the element exists (by signature)
        assert get_element(data.ar1, path='FULL')

        # should fail if the element does not exist (by signature)
        with pytest.raises(XelibError):
            get_element(data.ar1, path='ABCD')

        # should return a handle if the element exists (by name)
        assert get_element(data.ar1, path='Male world model')
        assert get_element(data.ar1, path='BODT - Body Template')

        # should fail if the element does not exist (by name)
        with pytest.raises(XelibError):
            get_element(data.ar1, path='Does not exist')

        # should return a handle of the element exists (pipe resolution)
        assert get_element(data.ar1, path='[BOD2|BODT]')

        # should fail if the element does not exist (pipe resolution)
        with pytest.raises(XelibError):
            get_element(data.ar1, path='[Does not exist|Nope]')

        # should resolve nested indexes correctly if the indexes are all in bounds
        assert get_element(0, path='[0]\\[1]\\[2]\\[1]')

        # should fail if any index is out of bounds
        with pytest.raises(XelibError):
            get_element(0, path='[0]\\[1]\\[9999999]\\[1]')

        # should resolve paths correctly if valid
        assert get_element(0, path='Skyrim.esm\\ARMO\\00012E46\\KWDA\\[0]')

        # should fail if any subpath is invalid
        with pytest.raises(XelibError):
            get_element(0, path='Skyrim.esm\\ARMO\\00012E46\\ABCD')

    def test_add_element_remove_element(self, xelib):
        data = self.get_data(xelib)

        # should create a new file if no handle given
        # should NOT be able to remove files
        assert not xelib.get_element(0, path='NewFile-1.esp')
        xelib.add_element(0, path='NewFile-1.esp')
        assert xelib.get_element(0, path='NewFile-1.esp')
        with pytest.raises(XelibError):
            xelib.remove_element(0, path='NewFile-1.esp')
        assert xelib.get_element(0, path='NewFile-1.esp')

        # should be able to add groups to files, even existing ones
        # should be able to remove groups from files
        assert xelib.get_element(data.xt3, path='ARMO')
        assert not xelib.get_element(data.xt3, path='CELL')
        xelib.add_element(data.xt3, path='ARMO')
        xelib.add_element(data.xt3, path='CELL')
        assert xelib.get_element(data.xt3, path='ARMO')
        assert xelib.get_element(data.xt3, path='CELL')
        xelib.remove_element(data.xt3, path='CELL')
        assert xelib.get_element(data.xt3, path='ARMO')
        assert not xelib.get_element(data.xt3, path='CELL')

        # should be able to override records in files
        assert not xelib.get_element(data.xt3, path='0001392A')
        assert xelib.element_count(data.armo2) == 1
        xelib.add_element(data.xt3, path='0001392A')
        assert xelib.get_element(data.xt3, path='0001392A')
        assert xelib.element_count(data.armo2) == 2

        # record override should not work if record being overridden is not a
        # master, but should work if is a master
        assert not xelib.get_element(data.xt3, path='0403C0F6')
        # TODO: apparently this causes xedit-lib to hang; probably why xedit-lib
        # did not have this check prior to setting the master
        # with pytest.raises(XelibError):
        #     xelib.add_element(data.xt3, path='0403C0F6')
        assert not xelib.get_element(data.xt3, path='0403C0F6')

        assert xelib.get_master_names(data.xt3) == ['Skyrim.esm', 'Update.esm']
        xelib.add_master(data.xt3, 'Dragonborn.esm')
        assert xelib.get_master_names(data.xt3) == ['Skyrim.esm',
                                                    'Update.esm',
                                                    'Dragonborn.esm']

        assert not xelib.get_element(data.xt3, path='0403C0F6')
        xelib.add_element(data.xt3, path='0403C0F6')
        assert xelib.get_element(data.xt3, path='0403C0F6')
        xelib.remove_element(data.xt3, path='0403C0F6')
        assert not xelib.get_element(data.xt3, path='0403C0F6')

        # should be able to add records to groups
        # should be able to remove records from groups
        assert xelib.element_count(data.armo2) == 2
        xelib.add_element(data.armo2, path='ARMO')
        assert xelib.element_count(data.armo2) == 3
        xelib.remove_element(data.armo2, path='[2]')
        assert xelib.element_count(data.armo2) == 2
        xelib.remove_element(data.armo2, path='[1]')
        assert xelib.element_count(data.armo2) == 1

        # should be able to create a new element on a record, even existing ones
        # should be able to remove elements from records
        assert xelib.get_element(data.ar2, path='EDID - Editor ID')
        assert not xelib.get_element(data.ar2, path='Destructible')
        xelib.add_element(data.ar2, path='EDID - Editor ID')
        xelib.add_element(data.ar2, path='Destructible')
        assert xelib.get_element(data.ar2, path='EDID - Editor ID')
        assert xelib.get_element(data.ar2, path='Destructible')
        xelib.remove_element(data.ar2, path='Destructible')
        assert not xelib.get_element(data.ar2, path='Destructible')

        # should be able to push a new element onto an array
        # should be able to insert an element at an index in an array
        # should be able to remove an element from an array
        assert xelib.element_count(data.keywords) == 5
        assert xelib.element_count(data.armature) == 1
        xelib.add_element(data.keywords, path='.')
        xelib.add_element(data.armature, path='.')
        assert xelib.element_count(data.keywords) == 6
        assert xelib.element_count(data.armature) == 2
        xelib.add_element(data.armature, '^0')
        assert xelib.element_count(data.armature) == 3
        xelib.remove_element(data.keywords, '[0]')
        xelib.remove_element(data.armature, '[0]')
        assert xelib.element_count(data.keywords) == 5
        assert xelib.element_count(data.armature) == 2

        # should be able to remove the last element in an array
        # TODO: this test is not working for some reason, in xedit I also don't
        # see such a path under xtest-4.esp, yet it works with xedit-lib tests;
        # somehow... I might need help with this one
        # assert xelib.get_element(0, 'xtest-4.esp\\05000802\\Armature\\[0]')
        # xelib.remove_element(0, 'xtest-4.esp\\05000802\\Armature\\[0]')
        # assert not xelib.get_element(0, 'xtest-4.esp\\05000802\\Armature\\[0]')

        # should fail to add element if interface is not a container
        element = xelib.get_element(data.ar2, path='FULL')
        with pytest.raises(XelibError):
            xelib.add_element(element, path='.')

        # should fail to remove if null handle is passed
        with pytest.raises(XelibError):
            xelib.remove_element(0, '')

        # should fail if no element exists at the given path
        with pytest.raises(XelibError):
            xelib.remove_element(data.ar3, 'YNAM')

    def test_set_element(self, xelib):
        data = self.get_data(xelib)

        # should work with value elements
        ar2_edid = xelib.get_element(data.ar2, path='EDID')
        ar3_edid = xelib.get_element(data.ar3, path='EDID')
        assert xelib.set_element(ar2_edid, ar3_edid)

        ar2_dnam = xelib.get_element(data.ar2, path='DNAM')
        ar3_dnam = xelib.get_element(data.ar3, path='DNAM')
        assert xelib.set_element(ar2_dnam, ar3_dnam)

        ar2_armature_0 = xelib.get_element(data.ar2, path='Armature\\[0]')
        ar3_armature_0 = xelib.get_element(data.ar3, path='Armature\\[0]')
        assert xelib.set_element(ar2_armature_0, ar3_armature_0)

        ar2_znam = xelib.get_element(data.ar2, path='ZNAM')
        ar3_znam = xelib.get_element(data.ar3, path='ZNAM')
        assert xelib.set_element(ar2_znam, ar3_znam)

        ar2_bodt_fpf = xelib.get_element(data.ar2, path='BODT\\First Person Flags')
        ar3_bodt_fpf = xelib.get_element(data.ar3, path='BODT\\First Person Flags')
        assert xelib.set_element(ar2_bodt_fpf, ar3_bodt_fpf)

        # should work with struct elements
        ar2_obnd = xelib.get_element(data.ar2, path='OBND')
        ar3_obnd = xelib.get_element(data.ar3, path='OBND')
        assert xelib.set_element(ar2_obnd, ar3_obnd)

        ar2_fwm = xelib.get_element(data.ar2, path='Female world model')
        ar3_fwm = xelib.get_element(data.ar3, path='Female world model')
        assert xelib.set_element(ar2_fwm, ar3_fwm)

        # should work with array elements
        ar2_kwda = xelib.get_element(data.ar2, path='KWDA')
        ar3_kwda = xelib.get_element(data.ar3, path='KWDA')
        assert xelib.set_element(ar2_kwda, ar3_kwda)

        ar2_armature = xelib.get_element(data.ar2, path='Armature')
        ar3_armature = xelib.get_element(data.ar3, path='Armature')
        assert xelib.set_element(ar2_armature, ar3_armature)

        # should fail if a file, group, or record is passed
        with pytest.raises(XelibError):
            xelib.set_element(data.xt3, data.xt3)
        with pytest.raises(XelibError):
            xelib.set_element(data.armo2, data.armo2)
        with pytest.raises(XelibError):
            xelib.set_element(data.ar2, data.ar2)

        # should fail if a null handle is passed
        with pytest.raises(XelibError):
            xelib.set_element(0, 0)
        with pytest.raises(XelibError):
            xelib.set_element(data.skyrim, 0)
        with pytest.raises(XelibError):
            xelib.set_element(0, data.skyrim)

    def test_get_elements(self, xelib):
        data = self.get_data(xelib)

        def get_elements_names(*args, **kwargs):
            return [xelib.name(id_)
                    for id_ in xelib.get_elements(*args, **kwargs)]

        def get_elements_edids(*args, **kwargs):
            return [xelib.get_value(id_, path='EDID')
                    for id_ in xelib.get_elements(*args, **kwargs)]

        # should resolve root children (files)
        files = get_elements_names(0)
        files = [file_ for file_ in files if file_ != 'NewFile-1.esp']
        assert len(files) == 11
        assert 'Skyrim.esm' in files

        # should resolve file children (file header and groups)
        children = get_elements_names(data.skyrim)
        assert len(children) == 118
        assert 'File Header' in children
        assert 'Reverb Parameters' in children

        # should resolve group children (records)
        records = get_elements_edids(data.armo1)
        assert len(records) == 2762
        assert 'DremoraBoots' in records
        assert 'SkinNaked' in records

        # should resolve record children (subrecords/elements)
        subrecords = get_elements_names(data.ar1)
        assert len(subrecords) == 13
        assert 'Record Header' in subrecords
        assert 'DNAM - Armor Rating' in subrecords

        # should resolve element children
        children = get_elements_names(data.keywords)
        assert len(children) == 5
        assert all(child == 'Keyword' for child in children)

        # should resolve paths
        paths = xelib.get_elements(data.ar2, path='KWDA')
        assert len(paths) == 5

        # should be able to return sorted elements
        try:
            xelib.set_sort_mode(xelib.SortBy.FormID)
            children = get_elements_names(data.skyrim, sort=True)
            assert 'File Header' == children[0]
            assert 'Weather' == children[-1]
            files = get_elements_names(0, sort=True)
            assert 'Skyrim.esm' == files[0]
            xelib.set_sort_mode(xelib.SortBy.FormID, reverse=True)
            files = get_elements_names(0, sort=True)
            assert 'Skyrim.esm' == files[-1]
        finally:
            xelib.set_sort_mode(xelib.SortBy.None_)

        # should not include child groups
        children = xelib.get_elements(0, path='Skyrim.esm\\DIAL')
        assert len(children) == 15037

    def test_get_def_names(self, xelib):
        data = self.get_data(xelib)

        # should work with main records
        assert xelib.get_def_names(data.ar1) == [
                   'Record Header',
                   'EDID - Editor ID',
                   'VMAD - Virtual Machine Adapter',
                   'OBND - Object Bounds',
                   'FULL - Name',
                   'EITM - Object Effect',
                   'EAMT - Enchantment Amount',
                   'Male world model',
                   'Icon',
                   'Female world model',
                   'Icon 2 (female)',
                   'Biped Body Template',
                   'Destructible',
                   'YNAM - Sound - Pick Up',
                   'ZNAM - Sound - Put Down',
                   'BMCT - Ragdoll Constraint Template',
                   'ETYP - Equipment Type',
                   'BIDS - Bash Impact Data Set',
                   'BAMT - Alternate Block Material',
                   'RNAM - Race',
                   'KSIZ - Keyword Count',
                   'KWDA - Keywords',
                   'DESC - Description',
                   'Armature',
                   'DATA - Data',
                   'DNAM - Armor Rating',
                   'TNAM - Template Armor']

        # should include additional elements
        h = xelib.get_element(data.skyrim, path='000094BD')
        assert xelib.get_def_names(h) == [
                   'Worldspace',
                   'Record Header',
                   'EDID - Editor ID',
                   'FULL - Name',
                   'DATA - Flags',
                   'XCLC - Grid',
                   'XCLL - Lighting',
                   'TVDT - Occlusion Data',
                   'MHDT - Max Height Data',
                   'LTMP - Lighting Template',
                   'LNAM - Unknown',
                   'XCLW - Water Height',
                   'XNAM - Water Noise Texture',
                   'XCLR - Regions',
                   'XLCN - Location',
                   'XWCN - Unknown',
                   'XWCS - Unknown',
                   'XWCU - Water Velocity',
                   'XCWT - Water',
                   'Ownership',
                   'XILL - Lock List',
                   'XWEM - Water Environment Map',
                   'XCCM - Sky/Weather from Region',
                   'XCAS - Acoustic Space',
                   'XEZN - Encounter Zone',
                   'XCMO - Music Type',
                   'XCIM - Image Space']

        # should work with structs
        h = xelib.get_element(data.ar1, path='OBND')
        assert xelib.get_def_names(h) == [
                   'X1', 'Y1', 'Z1', 'X2', 'Y2', 'Z2']

        # should work with unions
        h = xelib.get_element(data.skyrim, path='00000DD6\\DATA')
        assert xelib.get_def_names(h) == ['Float']

        # should work with VMAD Object Unions
        h = xelib.get_element(0, path='Update.esm\\0100080E\\VMAD\\Scripts\\'
                                      '[0]\\Properties\\[0]\\Value\\'
                                      'Object Union')
        assert xelib.get_def_names(h) == ['Object v2']

        h = xelib.get_element(h, path='Object v2')
        assert xelib.get_def_names(h) == ['FormID', 'Alias', 'Unused']

    def test_get_container(self, xelib):
        data = self.get_data(xelib)

        # should return the file containing a group
        assert xelib.get_container(data.armo1)

        # should return the group containing a record
        assert xelib.get_container(data.ar1)

        # should return the record containing an element
        h = xelib.get_element(data.ar1, path='EDID')
        assert xelib.get_container(h)

        h = xelib.get_element(data.refr, path='Record Header')
        assert xelib.get_container(h)

        # should return the parent element containing a child element
        h = xelib.get_element(data.ar1, path='BODT\\Armor Type')
        assert xelib.get_container(h)

        # should fail if called on a file
        with pytest.raises(XelibError):
            xelib.get_container(data.skyrim, ex=True)

    def test_get_element_file(self, xelib):
        data = self.get_data(xelib)

        # should return the input if the input is a file
        assert xelib.name(xelib.get_element_file(data.skyrim)) == 'Skyrim.esm'

        # should return the file containing a group
        assert xelib.name(xelib.get_element_file(data.armo1)) == 'Skyrim.esm'

        # should return the file containing a record
        assert xelib.name(xelib.get_element_file(data.ar1)) == 'Skyrim.esm'
        assert xelib.name(xelib.get_element_file(data.ar2)) == 'xtest-2.esp'
        assert xelib.name(xelib.get_element_file(data.ar3)) == 'xtest-3.esp'

        # should return the file containing an element
        assert xelib.name(xelib.get_element_file(data.keywords)) == 'Skyrim.esm'
        assert xelib.name(xelib.get_element_file(data.entries)) == 'xtest-2.esp'

    def test_get_links_to(self, xelib):
        data = self.get_data(xelib)

        def get_links_to_name(*args, **kwargs):
            return xelib.name(xelib.get_links_to(*args, **kwargs))

        # should return the referenced record
        assert get_links_to_name(data.keyword) == 'PerkFistsIron'
        assert get_links_to_name(data.ar1, path='RNAM') == 'Default Race'

        # should work on unions
        assert get_links_to_name(
                   data.skyrim, path='0009CD51\\DATA\\Teaches') == 'Flames'

        # should work with navmesh edge links
        h = xelib.get_element(data.skyrim, path='000FF1DE')
        assert get_links_to_name(
                   h, path='NVNM\\Edge Links\\[0]\\Mesh') == '[NAVM:000FF1CB]'

        # should fail if called on a null reference
        with pytest.raises(XelibError):
            xelib.get_links_to(data.armo2, path='ZNAM', ex=True)

        # should fail if path is invalid
        with pytest.raises(XelibError):
            xelib.get_links_to(data.keywords, path='[99]', ex=True)

        # should fail on elements that cannot store a reference
        with pytest.raises(XelibError):
            xelib.get_links_to(0, ex=True)
        with pytest.raises(XelibError):
            xelib.get_links_to(data.skyrim, ex=True)
        with pytest.raises(XelibError):
            xelib.get_links_to(data.ar1, ex=True)
        with pytest.raises(XelibError):
            xelib.get_links_to(data.dnam, ex=True)

        # should be fast
        # NOTE: not implementing this one, seems weird to run a performance
        # test on a wrapper that just invokes the DLL which is already
        # performance-tested

    def test_set_links_to(self, xelib):
        data = self.get_data(xelib)

        # should set references
        h_start = xelib.get_links_to(data.keyword)
        h = xelib.get_element(0, path='Skyrim.esm\\0002C17B')
        assert xelib.name(h_start) == 'PerkFistsIron'
        xelib.set_links_to(data.keyword, h)
        assert xelib.name(xelib.get_links_to(data.keyword)) == 'PerkFistsDaedric'
        xelib.set_links_to(data.keyword, h_start)
        assert xelib.name(xelib.get_links_to(data.keyword)) == 'PerkFistsIron'

    def test_element_count(self, xelib):
        data = self.get_data(xelib)

        # should return number of files if null handle is passed
        assert xelib.element_count(0) == 12

        # should return the number of elements in a file
        assert xelib.element_count(data.skyrim) == 118

        # should return number of elements in a group
        assert xelib.element_count(data.armo1) == 2762

        # should return the number of elements in a record
        assert xelib.element_count(data.ar1) == 13

        # should return the number of elements in a subrecord
        assert xelib.element_count(data.keywords) == 5

        # should return 0 if there are no children
        assert xelib.element_count(data.dnam) == 0

    def test_element_equals(self, xelib):
        data = self.get_data(xelib)

        # should return true for same element
        h = xelib.get_element(0, path='Skyrim.esm')
        assert xelib.element_equals(data.skyrim, h)

        h = xelib.get_element(data.skyrim, path='ARMO')
        assert xelib.element_equals(data.armo1, h)

        h = xelib.get_element(data.armo1, path='00012E46')
        assert xelib.element_equals(data.ar1, h)

        h = xelib.get_element(data.ar1, path='KWDA')
        assert xelib.element_equals(data.keywords, h)

        h = xelib.get_element(data.ar1, path='DNAM')
        assert xelib.element_equals(data.dnam, h)

        # should return false for different elements holding the same value
        h = xelib.get_element(data.ar2, path='DNAM')
        assert not xelib.element_equals(data.dnam, h)

        h = xelib.get_element(data.ar2, path='KWDA')
        assert not xelib.element_equals(data.keywords, h)

        # should return false for different elements
        assert not xelib.element_equals(data.skyrim, data.armo1)
        assert not xelib.element_equals(data.armo1, data.ar1)
        assert not xelib.element_equals(data.ar1, data.keywords)
        assert not xelib.element_equals(data.keywords, data.dnam)

        # should fail if null handle passed
        with pytest.raises(XelibError):
            xelib.element_equals(0, 0)

    def test_element_matches(self, xelib):
        data = self.get_data(xelib)

        # should work on null references
        assert xelib.element_matches(
                   data.ar2, 'ZNAM', 'NULL - Null Reference [00000000]')
        assert not xelib.element_matches(data.ar2, 'ZNAM', '')

        # should work on string fields
        assert xelib.element_matches(data.ar2, 'EDID', 'ArmorIronGauntlets')
        assert not xelib.element_matches(data.ar2, 'EDID', 'Blarg')

        # should work on integer fields
        assert xelib.element_matches(data.ar2, 'OBND\\Z1', '-1')
        assert not xelib.element_matches(data.ar2, 'OBND\\Z1', '-69')

        # should work on float fields
        assert xelib.element_matches(data.ar2, 'DATA\\Weight', '5.0')
        assert not xelib.element_matches(data.ar2, 'DATA\\Weight', '5.01')
        assert xelib.element_matches(data.ar2, 'DATA\\Weight', '5')
        assert xelib.element_matches(data.ar2, 'DNAM', '10.0')
        assert xelib.element_matches(data.ar2, 'DNAM', '10')

        # should return true if FormID matches
        assert xelib.element_matches(data.keywords, '[0]', '000424EF')
        assert xelib.element_matches(data.ar2, 'ZNAM', '00000000')
        assert xelib.element_matches(data.ar2, 'RNAM', '00000019')

        # should return false if FormID does not match
        assert not xelib.element_matches(data.keywords, '[0]', '000A82BB')
        assert not xelib.element_matches(data.ar2, 'RNAM', '00000029')

        # should return true if Editor ID matches
        assert xelib.element_matches(data.keywords, '[0]', 'PerkFistsIron')
        assert xelib.element_matches(data.keywords, '[3]', 'ArmorGauntlets')
        assert xelib.element_matches(data.ar2, 'RNAM', 'DefaultRace')

        # should return false if Editor ID does not match
        assert not xelib.element_matches(data.keywords, '[0]', '"Vampire"')
        assert not xelib.element_matches(data.keywords, '[1]', '"ArMorHeAvY"')

        # should return true if FULL name matches
        assert xelib.element_matches(data.ar2, 'RNAM', '"Default Race"')
        assert xelib.element_matches(data.keywords, '[0]', '""')

        # should return false if FULL name does not match
        assert not xelib.element_matches(data.ar2, 'RNAM', '"Default RacE"')
        assert not xelib.element_matches(data.ar2, 'ZNAM', '"Null Reference"')

    def test_has_array_item(self, xelib):
        data = self.get_data(xelib)

        # should return true if array item is present (value arrays)
        assert xelib.has_array_item(data.ar2, 'KWDA', '', 'PerkFistsIron')
        assert xelib.has_array_item(data.keywords, '', '', 'ArmorGauntlets')
        assert xelib.has_array_item(data.keywords, '', '', '0006BBE3')
        assert xelib.has_array_item(data.ar2, 'Armature', '', 'IronGlovesAA')

        # should return false if array item is not present (value arrays)
        assert not xelib.has_array_item(data.keywords, '', '', 'PerkFistsSteel')
        assert not xelib.has_array_item(data.keywords, '', '', 'ArmorHelmet')
        assert not xelib.has_array_item(data.keywords, '', '', '0006BBD4')
        assert not xelib.has_array_item(data.ar2, 'Armature', '', 'IronHelmetAA')

        # should return true if array item is present (struct arrays)
        assert xelib.has_array_item(
                   data.entries, '', 'LVLO\\Reference', 'ArmorIronGauntlets')
        assert xelib.has_array_item(
                   data.entries, '', 'LVLO\\Reference', '"Iron Armor"')
        assert xelib.has_array_item(
                   data.entries, '', 'LVLO\\Reference', '00012E4B')
        assert xelib.has_array_item(
                   data.entries, '', 'LVLO\\Reference', '"Iron Helmet"')

        # should return false if array item is not present (struct arrays)
        assert not xelib.has_array_item(
                       data.entries, '', 'LVLO\\Reference', 'ArmorSteelHelmetA')
        assert not xelib.has_array_item(
                       data.entries, '', 'LVLO\\Reference', '"Steel Helmet"')
        assert not xelib.has_array_item(
                       data.entries, '', 'LVLO\\Reference', '00131954')

    def test_get_array_item(self, xelib):
        data = self.get_data(xelib)

        # should succeed if array item is present (value arrays)
        assert xelib.get_array_item(data.ar2, 'KWDA', '', 'PerkFistsIron')
        assert xelib.get_array_item(data.keywords, '', '', 'ArmorGauntlets')
        assert xelib.get_array_item(data.keywords, '', '', '0006BBE3')
        assert xelib.get_array_item(data.ar2, 'Armature', '', 'IronGlovesAA')

        # should fail if array item is not present (value arrays)
        with pytest.raises(XelibError):
            xelib.get_array_item(data.keywords, '', '', 'PerkFistsSteel')
        with pytest.raises(XelibError):
            xelib.get_array_item(data.keywords, '', '', 'ArmorHelmet')
        with pytest.raises(XelibError):
            xelib.get_array_item(data.keywords, '', '', '0006BBD4')
        with pytest.raises(XelibError):
            xelib.get_array_item(data.ar2, 'Armature', '', 'IronHelmetAA')

        # should succeed if array item is present (struct arrays)
        assert xelib.get_array_item(
                   data.entries, '', 'LVLO\\Reference', 'ArmorIronGauntlets')
        assert xelib.get_array_item(
                   data.entries, '', 'LVLO\\Reference', '"Iron Armor"')
        assert xelib.get_array_item(
                   data.entries, '', 'LVLO\\Reference', '00012E4B')
        assert xelib.get_array_item(
                   data.entries, '', 'LVLO\\Reference', '"Iron Helmet"')

        # should fail if array item is not present (struct arrays)
        with pytest.raises(XelibError):
            xelib.get_array_item(
                      data.entries, '', 'LVLO\\Reference', 'ArmorSteelHelmetA')
        with pytest.raises(XelibError):
            xelib.get_array_item(
                      data.entries, '', 'LVLO\\Reference', '"Steel Helmet"')
        with pytest.raises(XelibError):
            xelib.get_array_item(
                      data.entries, '', 'LVLO\\Reference', '00131954')

    def test_add_array_item(self, xelib):
        data = self.get_data(xelib)

        # should add an array item (references)
        assert xelib.element_count(data.keywords) == 5
        assert xelib.add_array_item(data.keywords, '', '', '')
        assert xelib.element_count(data.keywords) == 6

        # should create the array if missing (references)
        assert xelib.remove_element(data.ar2, path='Armature')
        assert not xelib.has_element(data.ar2, path='Armature')
        h = xelib.add_array_item(data.ar2, 'Armature', '', '00012E47')
        assert h
        assert xelib.get_value(h) == 'IronGlovesAA [ARMA:00012E47]'
        assert xelib.has_element(data.ar2, path='Armature')
        h = xelib.get_element(data.ar2, path='Armature')
        assert xelib.element_count(h) == 1

        # should be able to set reference with FormID (references)
        assert xelib.element_count(data.keywords) == 6
        h = xelib.add_array_item(data.keywords, '', '', '0006BBD4')
        assert h
        assert xelib.get_value(h) == 'ArmorMaterialDaedric [KYWD:0006BBD4]'
        assert xelib.element_count(data.keywords) == 7

        # should be able to add reference with edit value (references)
        assert xelib.element_count(data.keywords) == 7
        h = xelib.add_array_item(
                      data.keywords, '', '', 'ArmorLight [KYWD:0006BBD3]')
        assert h
        assert xelib.get_value(h) == 'ArmorLight [KYWD:0006BBD3]'
        assert xelib.element_count(data.keywords) == 8

        # should add an aray item (struct arrays)
        assert xelib.element_count(data.entries) == 4
        assert xelib.add_array_item(data.entries, '', '', '')
        assert xelib.element_count(data.entries) == 5

        # should be able to set value at subpath (struct arrays)
        assert xelib.element_count(data.entries) == 5
        assert xelib.add_array_item(
                         data.entries,
                         '',
                         'LVLO\\Reference',
                         'ArmorLeatherBoots "Leather Boots" [ARMO:00013920]')
        assert xelib.element_count(data.entries) == 6

        # should fail if subpath is invalid (struct arrays)
        with pytest.raises(XelibError):
            xelib.add_array_item(
                      data.entries,
                      '',
                      'Fake\\Path',
                      'ArmorLeatherCuirass "Leather Armor" [ARMO:0003619E]')

        # should fail if element is not an array
        with pytest.raises(XelibError):
            xelib.add_array_item(data.ar1, '', '', '')

    def test_move_array_item(self, xelib):
        pytest.skip('xedit-lib has not yet implemented this one')

    def test_remove_array_item(self, xelib):
        pytest.skip('xedit-lib has not yet implemented this one')

    def test_copy_element(self, xelib):
        data = self.get_data(xelib)

        # before anything else, add xt2, xt4 as masters to xt5
        assert ([xelib.name(id_) for id_ in xelib.get_masters(data.xt5)] ==
                ['Skyrim.esm', 'Update.esm'])
        xelib.add_master(data.xt5, 'xtest-2.esp')
        xelib.add_master(data.xt5, 'xtest-4.esp')
        assert ([xelib.name(id_) for id_ in xelib.get_masters(data.xt5)] ==
                ['Skyrim.esm', 'Update.esm', 'xtest-2.esp', 'xtest-4.esp'])

        # should be able to deep copy groups
        source = xelib.get_element(0, 'xtest-2.esp\\ARMO')
        h = xelib.copy_element(source, data.xt5, as_new=True)
        assert xelib.name(xelib.get_element_file(h)) == 'xtest-5.esp'
        assert xelib.is_master(xelib.get_element(h, path='[0]'))

        # should be able to deep copy records
        source = xelib.get_element(0, 'xtest-2.esp\\00013739')
        h = xelib.copy_element(source, data.xt5, as_new=True)
        assert xelib.name(xelib.get_element_file(h)) == 'xtest-5.esp'
        assert xelib.is_master(h)

        # should be able to deep copy elements
        try:
            assert xelib.add_array_item(
                            0, 'xtest-3.esp\\00012E46\\KWDA', '', '0006BBD4')
            rec = xelib.get_element(0, path='xtest-5.esp\\ARMO\\[0]')
            assert rec
            source = xelib.get_element(0, 'xtest-3.esp\\00012E46\\KWDA')
            h = xelib.copy_element(source, rec, as_new=True)
            assert xelib.name(xelib.get_element_file(h)) == 'xtest-5.esp'
            assert xelib.element_count(h) == 6
        finally:
            assert xelib.remove_array_item(
                       0, 'xtest-3.esp\\00012E46\\KWDA', '', '0006BBD4')

        # should be able to copy array elements
        try:
            h = xelib.get_element(data.ar3, 'KWDA')
            assert h
            source = xelib.get_element(0, 'xtest-3.esp\\00012E46\\KWDA\\[0]')
            h = xelib.copy_element(source, h, as_new=True)
            assert xelib.name(xelib.get_element_file(h)) == 'xtest-3.esp'
            assert xelib.element_count(xelib.get_container(h)) == 6
        finally:
            assert xelib.remove_array_item(data.ar3, 'KWDA', '', '000424EF')

        # should be able to override records
        source = xelib.get_element(0, 'xtest-2.esp\\00012E46')
        h = xelib.copy_element(source, data.xt5)
        assert xelib.name(xelib.get_element_file(h)) == 'xtest-5.esp'
        assert not xelib.is_master(h)

        # should copy records with Deleted References (UDRs)
        source = xelib.get_element(0, 'xtest-4.esp\\00027DE7')
        h = xelib.copy_element(source, data.xt5)
        assert xelib.name(xelib.get_element_file(h)) == 'xtest-5.esp'

        # should copy records with Unexpected References (UERs)
        # should be able to remove the last element in an array
        # TODO: this test is not working for some reason, in xedit I also don't
        # see such a path under xtest-4.esp, yet it works with xedit-lib tests;
        # somehow... I might need help with this one
        # source = xelib.get_element(0, 'xtest-4.esp\\05000800')
        # assert source
        # h = xelib.copy_element(source, data.xt5)
        # assert xelib.name(xelib.get_element_file(h)) == 'xtest-5.esp'

        # should copy records with Unresolved References (URRs)
        # source = xelib.get_element(0, 'xtest-4.esp\\05000801')
        # h = xelib.copy_element(source, data.xt5)
        # assert xelib.name(xelib.get_element_file(h)) == 'xtest-5.esp'

        # should copy records with Unexpected Subrecords (UESs)
        # source = xelib.get_element(0, 'xtest-4.esp\\05000802')
        # h = xelib.copy_element(source, data.xt5)
        # assert xelib.name(xelib.get_element_file(h)) == 'xtest-5.esp'

        # remove masters we added at the beginning of this test
        xelib.clean_masters(data.xt5)
        xelib.add_master(data.xt5, 'Skyrim.esm')
        xelib.add_master(data.xt5, 'Update.esm')
        assert ([xelib.name(id_) for id_ in xelib.get_masters(data.xt5)] ==
                ['Skyrim.esm', 'Update.esm'])

    def test_get_signature_allowed(self, xelib):
        data = self.get_data(xelib)

        # should return true if signature is allowed
        assert xelib.get_signature_allowed(data.keyword, 'KYWD')
        assert xelib.get_signature_allowed(data.keyword, 'NULL')
        h = xelib.get_element(data.ar2, path='ZNAM')
        assert h
        assert xelib.get_signature_allowed(h, 'SNDR')
        h = xelib.get_element(0, 'Update.esm\\000E49CD\\VMAD\\Scripts\\[0]\\'
                                 'Properties\\[0]\\Value\\Object Union\\'
                                 'Object v2\\FormID')
        assert h
        assert xelib.get_signature_allowed(h, 'NULL')
        assert xelib.get_signature_allowed(h, 'ARMO')
        assert xelib.get_signature_allowed(h, 'WEAP')
        assert xelib.get_signature_allowed(h, 'COBJ')

        # should return false if signature is not allowed
        assert not xelib.get_signature_allowed(data.keyword, 'ARMO')
        assert not xelib.get_signature_allowed(data.keyword, 'NPC_')
        h = xelib.get_element(data.ar2, 'ZNAM')
        assert not xelib.get_signature_allowed(h, 'NULL')

        # should raise an exception if a null handle is passed
        with pytest.raises(XelibError):
            xelib.get_signature_allowed(0, 'TES4')

        # should raise an exception if element isn't an integer
        with pytest.raises(XelibError):
            xelib.get_signature_allowed(data.skyrim, 'TES4')
        with pytest.raises(XelibError):
            xelib.get_signature_allowed(data.armo1, 'ARMO')
        with pytest.raises(XelibError):
            xelib.get_signature_allowed(data.ar1, 'BODT')
        with pytest.raises(XelibError):
            xelib.get_signature_allowed(data.keywords, 'KYWD')

        # should raise an excxeption if element can't hold FormIDs
        with pytest.raises(XelibError):
            xelib.get_signature_allowed(data.dnam, 'ARMO')

    def test_get_allowed_signatures(self, xelib):
        data = self.get_data(xelib)

        # should work with checked references
        assert xelib.get_allowed_signatures(data.keyword) == ['KYWD', 'NULL']

        # should work with union elements
        h = xelib.get_element(
                      data.skyrim,
                      path='00000DD2\\Conditions\\[1]\\CTDA\\Parameter #1')
        assert xelib.get_allowed_signatures(h) == ['PERK']

        # should raise an exception if element isn't an integer
        with pytest.raises(XelibError):
            xelib.get_allowed_signatures(data.skyrim)
        with pytest.raises(XelibError):
            xelib.get_allowed_signatures(data.armo1)
        with pytest.raises(XelibError):
            xelib.get_allowed_signatures(data.ar1)
        with pytest.raises(XelibError):
            xelib.get_allowed_signatures(data.keywords)

        # should raise an exception if element can't hold FormIDs
        with pytest.raises(XelibError):
            xelib.get_allowed_signatures(data.dnam)

    def test_get_is_editable(self, xelib):
        data = self.get_data(xelib)

        # should return false for uneditable files
        assert not xelib.get_is_editable(data.skyrim)

        # should return false for uneditable records
        assert not xelib.get_is_editable(data.ar1)

        # should return true for editable files
        assert xelib.get_is_editable(data.xt3)

        # should return true for editable records
        assert xelib.get_is_editable(data.ar2)

    def test_get_can_add(self, xelib):
        data = self.get_data(xelib)

        # should return true for editable files
        h = xelib.get_element(0, path='Update.esm')
        assert h
        assert xelib.get_can_add(h)
        assert xelib.get_can_add(data.xt3)

        # should return true for editable groups
        h = xelib.get_element(0, path='Update.esm\\ARMO')
        assert h
        assert xelib.get_can_add(h)
        assert xelib.get_can_add(data.armo2)

        # should return false for uneditable files
        assert not xelib.get_can_add(data.skyrim)

        # should return false for uneditable groups
        assert not xelib.get_can_add(data.armo1)

    def test_get_add_list(self, xelib):
        data = self.get_data(xelib)

        # should return add list for editable files
        h = xelib.get_element(0, path='Update.esm')
        assert h
        add_list = xelib.get_add_list(h)
        assert add_list[0] == 'AACT - Action'
        assert add_list[-1] == 'WTHR - Weather'
        assert len(add_list) == 72

        # should return add list for editable groups
        assert xelib.get_add_list(data.armo2) == ['ARMO - Armor']

        # should fail on uneditable files
        with pytest.raises(XelibError):
            xelib.get_add_list(data.skyrim)

    def test_value_type(self, xelib):
        data = self.get_data(xelib)

        def value_type_at(id_, path=''):
            if path:
                return xelib.value_type(xelib.get_element(id_, path=path))
            return xelib.value_type(id_)

        # should return vtBytes for byte array elements
        assert (value_type_at(data.ar1, path='Male world model\\MO2T') ==
                    xelib.ValueTypes.vtBytes)

        # should return vtNumber for numeric elements
        assert (value_type_at(data.ar1, path='OBND\\X1') ==
                    xelib.ValueTypes.vtNumber)
        assert (value_type_at(data.ar1, path='DNAM') ==
                    xelib.ValueTypes.vtNumber)
        assert (value_type_at(data.ar1, path='DATA\\Weight') ==
                    xelib.ValueTypes.vtNumber)

        # should return vtString for string elements
        assert (value_type_at(data.ar1, path='EDID') ==
                    xelib.ValueTypes.vtString)
        assert (value_type_at(data.ar1, path='FULL') ==
                    xelib.ValueTypes.vtString)
        assert (value_type_at(data.ar1, path='Male world model\\MOD2') ==
                    xelib.ValueTypes.vtString)

        # should return vtText for multi-line string elements
        assert (value_type_at(data.skyrim, path='00015475\\DESC') ==
                    xelib.ValueTypes.vtText)
        assert (value_type_at(data.skyrim, path='0001362F\\Responses\\[0]\\NAM1') ==
                    xelib.ValueTypes.vtText)
        assert (value_type_at(0, path='xtest-1.esp\\File Header\\SNAM') ==
                    xelib.ValueTypes.vtText)
        assert (value_type_at(data.skyrim, path='0000014C\\DNAM') ==
                    xelib.ValueTypes.vtText)
        assert (value_type_at(data.skyrim, path='00015D24\\Stages\\[1]\\'
                                                'Log Entries\\[0]\\CNAM') ==
                    xelib.ValueTypes.vtText)

        # should return vtReference for FormID elements
        assert (value_type_at(data.ar1, path='KWDA\\[0]') ==
                    xelib.ValueTypes.vtReference)
        assert (value_type_at(data.ar1, path='Armature\\[0]') ==
                    xelib.ValueTypes.vtReference)

        # should return vtFlags for flags elements
        assert (value_type_at(data.ar1, path='BODT\\First Person Flags') ==
                    xelib.ValueTypes.vtFlags)
        assert (value_type_at(data.ar1, path='BODT\\General Flags') ==
                    xelib.ValueTypes.vtFlags)
        assert (value_type_at(data.ar1, path='Record Header\\Record Flags') ==
                    xelib.ValueTypes.vtFlags)

        # should return vtEnum for enumeration elements
        assert (value_type_at(data.ar1, path='BODT\\Armor Type') ==
                    xelib.ValueTypes.vtEnum)

        # should return vtColor for color elements
        assert (value_type_at(data.skyrim, path='0000001B\\PNAM') ==
                    xelib.ValueTypes.vtColor)
        assert (value_type_at(data.skyrim, path='00027D1C\\XCLL\\Ambient Color') ==
                    xelib.ValueTypes.vtColor)

        # should return vtStruct for struct elements
        assert (value_type_at(data.ar1, path='Male world model') ==
                    xelib.ValueTypes.vtStruct)
        assert (value_type_at(data.ar1, path='OBND') ==
                    xelib.ValueTypes.vtStruct)
        assert (value_type_at(data.ar1, path='DATA') ==
                    xelib.ValueTypes.vtStruct)
        assert (value_type_at(data.ar1, path='Record Header') ==
                    xelib.ValueTypes.vtStruct)

        # should resolve union defs correctly
        assert (value_type_at(data.skyrim, path='00000DD6\\DATA') ==
                    xelib.ValueTypes.vtNumber)

        # should fail on files, groups, and main records
        with pytest.raises(XelibError):
            value_type_at(data.skyrim)
        with pytest.raises(XelibError):
            value_type_at(data.armo1)
        with pytest.raises(XelibError):
            value_type_at(data.ar1)

        # should fail on null handles
        with pytest.raises(XelibError):
            value_type_at(0)

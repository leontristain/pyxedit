from collections import namedtuple
import functools
import pytest

from xelib import XelibError

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
        # I might need help with this one
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

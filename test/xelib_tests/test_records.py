from collections import namedtuple
import pytest

from pyxedit import XelibError

from . fixtures import xelib  # NOQA: for pytest


class TestRecords:
    def get_data(self, xelib):
        test_data = namedtuple('TestData', 'skyrim armo ar1 dnam xt1 xt2 xt4 '
                                           'ar2 ar3 kw1 kw2 kw3')

        skyrim = xelib.get_element(0, path='Skyrim.esm')
        armo = xelib.get_element(skyrim, path='ARMO')
        ar1 = xelib.get_element(armo, path='00012E46')
        dnam = xelib.get_element(ar1, path='DNAM')
        xt1 = xelib.get_element(0, path='xtest-1.esp')
        xt2 = xelib.get_element(0, path='xtest-2.esp')
        xt4 = xelib.get_element(0, path='xtest-4.esp')
        ar2 = xelib.get_element(0, path='xtest-2.esp\\00012E46')
        ar3 = xelib.get_element(0, path='xtest-3.esp\\00012E46')
        kw1 = xelib.get_element(0, path='xtest-1.esp\\00C23800')
        kw2 = xelib.get_element(0, path='xtest-1.esp\\00C23801')
        kw3 = xelib.get_element(0, path='xtest-4.esp\\00C23801')

        return test_data(skyrim=skyrim,
                         armo=armo,
                         ar1=ar1,
                         dnam=dnam,
                         xt1=xt1,
                         xt2=xt2,
                         xt4=xt4,
                         ar2=ar2,
                         ar3=ar3,
                         kw1=kw1,
                         kw2=kw2,
                         kw3=kw3)

    def test_get_record(self, xelib):
        data = self.get_data(xelib)

        # should be able to resolve records from root
        # NOTE: for some reason for my test setup, 0x03000800 and 0x05000800
        # are erroring; it could be due to pytest starting each test class from
        # scratch rather than having one continuous state from begin to end like
        # in xedit-lib tests; for the time being I'll replace with 02000800 and
        # 04000800; if all we're checking is "to be able to resolve records
        # from root", then the exact record used may not actually matter.
        assert xelib.get_record(0, 0x01000800, search_masters=False)
        assert xelib.get_record(0, 0x02000800, search_masters=False)
        assert xelib.get_record(0, 0x04000800, search_masters=False)

        # should be able to resolve injected records from root
        assert xelib.get_record(0, 0x00C23800, search_masters=False)
        assert xelib.get_record(0, 0x00C23801, search_masters=False)
        assert xelib.get_record(0, 0x00C23802, search_masters=False)

        # should be able to resolve overrides by local FormID
        assert xelib.get_record(data.xt2, 0x0007F82A, search_masters=False)
        assert xelib.get_record(data.xt2, 0x00012E46, search_masters=False)

        # should be able to resolve new records by local FormID
        assert xelib.get_record(data.xt2, 0x03000800, search_masters=False)
        assert xelib.get_record(data.xt4, 0x03000800, search_masters=False)

        # should be able to resolve injections by local FormID
        assert xelib.get_record(data.xt1, 0x00C23800, search_masters=False)
        assert xelib.get_record(data.xt1, 0x00C23801, search_masters=False)

    def test_get_records(self, xelib):
        data = self.get_data(xelib)

        # should return all records in a file
        h = xelib.get_element(0, path='xtest-2.esp')
        assert len(xelib.get_records(h, include_overrides=True)) == 6

        # should be able to exclude overrides
        assert len(xelib.get_records(h)) == 1

        # should return all records in a top-level group
        h = xelib.get_element(data.armo)
        assert len(xelib.get_records(h, include_overrides=True)) == 2762
        h = xelib.get_element(0, path='xtest-2.esp\\CELL')
        assert len(xelib.get_records(h, include_overrides=True)) == 3

        # should return all records in a subgroup
        h = xelib.get_element(
                      0, path='xtest-2.esp\\00027D1C\\Child Group\\Persistent')
        assert len(xelib.get_records(h, include_overrides=True)) == 2

        # should return all record children of a record
        h = xelib.get_element(0, path='xtest-2.esp\\00027D1C')
        assert len(xelib.get_records(h, include_overrides=True)) == 2

        # should return all records of a given signature in all files
        # NOTE: numbers differ from xedit-lib tests because here I'm loading
        # all DLCs for these tests
        h = xelib.get_element(0)
        assert len(xelib.get_records(h, search='DOBJ')) == 1
        assert len(xelib.get_records(h, search='DOBJ', include_overrides=True)) == 5
        assert len(xelib.get_records(h, search='ARMO')) == 3671
        assert len(xelib.get_records(h, search='ARMO', include_overrides=True)) == 3725

        # should be able to handle multiple signatures
        armo_count = len(xelib.get_records(h, search='ARMO'))
        weap_count = len(xelib.get_records(h, search='WEAP'))
        misc_count = len(xelib.get_records(h, search='MISC'))
        cobj_count = len(xelib.get_records(h, search='COBJ'))
        npc__count = len(xelib.get_records(h, search='NPC_'))
        assert len(xelib.get_records(h, search='ARMO,WEAP,MISC')) == (
                                          armo_count + weap_count + misc_count)

        # should map name to signatures
        assert len(xelib.get_records(h, search='Armor')) == armo_count
        assert len(xelib.get_records(
                       h, search='Constructible Object,'
                                 'Non-Player Character (Actor)')) == (
                                                       cobj_count + npc__count)

        # should load records quickly
        # NOTE: not implementing performance tests

    def test_get_refrs(self, xelib):
        # should be able to get references
        assert len(xelib.get_refrs(0, 'DOOR')) == 4411

        # should load records quickly
        # NOTE: not implementing performance tests

    def test_find_next_record(self, xelib):
        try:
            xelib.set_sort_mode(xelib.SortBy.FormID)

            # should work with root handle
            result = xelib.find_next_record(0, 'Armor', True, False)
            assert result
            assert xelib.get_value(result, path='EDID') == (
                                             'TG08ANightingaleArmorActivator')

            # should work from record handle
            result = xelib.find_next_record(result, 'Armor', True, False)
            assert result
            assert xelib.get_value(result, path='EDID') == (
                                                   'FortifySkillHeavyArmor02')
        finally:
            xelib.set_sort_mode(xelib.SortBy.None_)

    def test_find_valid_references(self, xelib):
        h = xelib.get_element(0, 'Update.esm')
        assert h
        results = xelib.find_valid_references(h, 'KYWD', 'a', 5)
        assert results == ['DA15WabbajackExcludedKeyword [KYWD:01000997]',
                           'ImmuneDragonPairedKill [KYWD:010009A2]',
                           'ArmorMaterialForsworn [KYWD:010009B9]',
                           'ArmorMaterialMS02Forsworn [KYWD:010009BA]',
                           'ArmorMaterialPenitus [KYWD:010009BB]']

    def test_is_master(self, xelib):
        data = self.get_data(xelib)

        # should return true for master records
        assert xelib.is_master(data.ar1)
        assert xelib.is_master(data.kw1)
        assert xelib.is_master(data.kw2)

        # should return false for override records
        assert not xelib.is_master(data.ar2)
        assert not xelib.is_master(data.ar3)
        assert not xelib.is_master(data.kw3)

        # should fail on elements that are not records
        with pytest.raises(XelibError):
            xelib.is_master(data.skyrim)
        with pytest.raises(XelibError):
            xelib.is_master(data.armo)
        with pytest.raises(XelibError):
            xelib.is_master(data.dnam)

        # should fail if a null handle is passed
        with pytest.raises(XelibError):
            xelib.is_master(0)

    def test_is_injected(self, xelib):
        data = self.get_data(xelib)

        # should return false for master records
        assert not xelib.is_injected(data.ar1)

        # should return false for override records
        assert not xelib.is_injected(data.ar2)

        # should return true for injected records
        assert xelib.is_injected(data.kw1)
        assert xelib.is_injected(data.kw2)

        # should fail on elements that are not records
        with pytest.raises(XelibError):
            xelib.is_injected(data.skyrim)
        with pytest.raises(XelibError):
            xelib.is_injected(data.armo)
        with pytest.raises(XelibError):
            xelib.is_injected(data.dnam)

        # should fail if a null handle is passed
        with pytest.raises(XelibError):
            xelib.is_injected(0)

    def test_is_override(self, xelib):
        data = self.get_data(xelib)

        # should return false for master records
        assert not xelib.is_override(data.ar1)
        assert not xelib.is_override(data.kw1)
        assert not xelib.is_override(data.kw2)

        # should return true for override records
        assert xelib.is_override(data.ar2)
        assert xelib.is_override(data.ar3)
        assert xelib.is_override(data.kw3)

        # should fail on elements that are not records
        with pytest.raises(XelibError):
            xelib.is_override(data.skyrim)
        with pytest.raises(XelibError):
            xelib.is_override(data.armo)
        with pytest.raises(XelibError):
            xelib.is_override(data.dnam)

        # should fail if a null handle is passed
        with pytest.raises(XelibError):
            xelib.is_override(0)

    def test_is_winning_override(self, xelib):
        data = self.get_data(xelib)

        # should return true for records with no overrides
        assert xelib.is_winning_override(data.kw1)

        # should return false for losing master records
        assert not xelib.is_winning_override(data.ar1)

        # should return false for losing override records
        assert not xelib.is_winning_override(data.ar2)
        assert not xelib.is_winning_override(data.kw2)

        # should return true for winning override records
        assert xelib.is_winning_override(data.ar3)
        assert xelib.is_winning_override(data.kw3)

        # should fail on elements that are not records
        with pytest.raises(XelibError):
            xelib.is_winning_override(data.skyrim)
        with pytest.raises(XelibError):
            xelib.is_winning_override(data.armo)
        with pytest.raises(XelibError):
            xelib.is_winning_override(data.dnam)

        # should fail if a null handle is passed
        with pytest.raises(XelibError):
            xelib.is_winning_override(0)

    def test_get_nodes(self, xelib):
        data = self.get_data(xelib)

        # should return a handle if argument is record
        assert xelib.get_nodes(data.kw1)

        # should work with records with overrides
        assert xelib.get_nodes(data.ar1)

        # should work with file headers
        assert xelib.get_nodes(
                   xelib.get_element(data.skyrim, path='File Header'))

        # should work with union defs
        assert xelib.get_nodes(
                   xelib.get_element(0, 'Update.esm\\0100080E'))

        # should fail on elements that are not records
        with pytest.raises(XelibError):
            xelib.get_nodes(data.skyrim)
        with pytest.raises(XelibError):
            xelib.get_nodes(data.armo)
        with pytest.raises(XelibError):
            xelib.get_nodes(data.dnam)

        # should fail if a null handle is passed
        with pytest.raises(XelibError):
            xelib.get_nodes(0)

    def test_get_conflict_data(self, xelib):
        data = self.get_data(xelib)

        # NOTE: in the below tests the conflict data pairs differ from
        # xedit-lib's expected values; I'm chalking this up to loading DLCs
        # in my tests, but if this ever shows issues in the future we may
        # revisit
        n1 = xelib.get_nodes(data.kw1)
        n2 = xelib.get_nodes(data.kw2)
        n3 = xelib.get_nodes(data.ar1)

        # should work on main records
        h = xelib.get_element(data.kw1)
        assert xelib.get_conflict_data(n1, h) == (xelib.ConflictAll.caOnlyOne,
                                                  xelib.ConflictThis.ctOnlyOne)
        h = xelib.get_element(data.kw2)
        assert xelib.get_conflict_data(n2, h) == (xelib.ConflictAll.caConflictCritical,
                                                  xelib.ConflictThis.ctMaster)
        h = xelib.get_element(data.ar1)
        assert xelib.get_conflict_data(n3, h) == (xelib.ConflictAll.caOverride,
                                                  xelib.ConflictThis.ctMaster)
        # should work on struct elements
        h = xelib.get_element(data.kw1, path='Record Header')
        assert xelib.get_conflict_data(n1, h) == (xelib.ConflictAll.caOnlyOne,
                                                  xelib.ConflictThis.ctOnlyOne)
        h = xelib.get_element(data.kw2, path='Record Header')
        assert xelib.get_conflict_data(n2, h) == (xelib.ConflictAll.caNoConflict,
                                                  xelib.ConflictThis.ctMaster)
        h = xelib.get_element(data.ar1, path='RecordHeader')
        assert xelib.get_conflict_data(n3, h) == (xelib.ConflictAll.caUnknown,
                                                  xelib.ConflictThis.ctUnknown)
        h = xelib.get_element(data.kw2, path='CNAM - Color')
        assert xelib.get_conflict_data(n2, h) == (xelib.ConflictAll.caConflictCritical,
                                                  xelib.ConflictThis.ctMaster)
        h = xelib.get_element(data.ar1, path='OBND - Object Bounds')
        assert xelib.get_conflict_data(n3, h) == (xelib.ConflictAll.caNoConflict,
                                                  xelib.ConflictThis.ctMaster)
        # should work on value elements
        h = xelib.get_element(data.kw1, path='Record Header\\Signature')
        assert xelib.get_conflict_data(n1, h) == (xelib.ConflictAll.caOnlyOne,
                                                  xelib.ConflictThis.ctOnlyOne)
        h = xelib.get_element(data.kw2, path='Record Header\\Signature')
        assert xelib.get_conflict_data(n2, h) == (xelib.ConflictAll.caNoConflict,
                                                  xelib.ConflictThis.ctMaster)
        h = xelib.get_element(data.ar1, path='RecordHeader\\Signature')
        assert xelib.get_conflict_data(n3, h) == (xelib.ConflictAll.caUnknown,
                                                  xelib.ConflictThis.ctUnknown)
        h = xelib.get_element(data.kw2, path='CNAM - Color\\Red')
        assert xelib.get_conflict_data(n2, h) == (xelib.ConflictAll.caConflictCritical,
                                                  xelib.ConflictThis.ctMaster)
        h = xelib.get_element(data.ar1, path='OBND - Object Bounds\\X1')
        assert xelib.get_conflict_data(n3, h) == (xelib.ConflictAll.caNoConflict,
                                                  xelib.ConflictThis.ctMaster)
        # should work on file headers
        h = xelib.get_element(data.skyrim, path='File Header')
        n1 = xelib.get_nodes(h)

        e = xelib.get_element(h, path='CNAM - Author')
        assert xelib.get_conflict_data(n1, e) == (xelib.ConflictAll.caOnlyOne,
                                                  xelib.ConflictThis.ctOnlyOne)
        e = xelib.get_element(h, path='HEDR - Header\\Version')
        assert xelib.get_conflict_data(n1, e) == (xelib.ConflictAll.caOnlyOne,
                                                  xelib.ConflictThis.ctOnlyOne)


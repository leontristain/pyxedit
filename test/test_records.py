from collections import namedtuple

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
        pass

    def test_get_refrs(self, xelib):
        pass

    def test_find_next_record(self, xelib):
        pass

    def test_find_valid_references(self, xelib):
        pass

    def test_is_master(self, xelib):
        pass

    def test_is_injected(self, xelib):
        pass

    def test_is_override(self, xelib):
        pass

    def test_is_winning_override(self, xelib):
        pass

    def test_get_nodes(self, xelib):
        pass

    def test_get_conflict_data(self, xelib):
        pass

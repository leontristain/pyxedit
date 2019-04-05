from collections import namedtuple
import pytest

from pyxedit import XelibError

from . fixtures import xelib  # NOQA: for pytest


class TestMasters:
    def get_data(self, xelib):
        test_data = namedtuple('TestData', 'skyrim xt5')

        skyrim = xelib.get_element(0, path='Skyrim.esm')
        xt5 = xelib.get_element(0, path='xtest-5.esp')

        return test_data(skyrim=skyrim, xt5=xt5)

    def test_add_master(self, xelib):
        data = self.get_data(xelib)

        # should add master if matching file is present
        assert xelib.add_master(data.xt5, 'xtest-3.esp')
        masters = xelib.get_element(data.xt5, 'File Header\\Master Files')
        assert xelib.element_count(masters) == 3

        # should not duplicate masters
        assert xelib.add_master(data.xt5, 'xtest-3.esp')
        masters = xelib.get_element(data.xt5, 'File Header\\Master Files')
        assert xelib.element_count(masters) == 3

        # should fail if matching file is not present
        with pytest.raises(XelibError):
            xelib.add_master(data.xt5, 'NonExistingFile.esp')
        masters = xelib.get_element(data.xt5, 'File Header\\Master Files')
        assert xelib.element_count(masters) == 3

    def test_add_masters(self, xelib):
        pytest.skip('Not implementing this one since there is no xelib wrapper')

    def test_get_masters(self, xelib):
        data = self.get_data(xelib)

        # should get master file handles
        assert ([xelib.name(id_) for id_ in xelib.get_masters(data.xt5)] ==
                ['Skyrim.esm', 'Update.esm', 'xtest-3.esp'])

    def test_get_required_by(self, xelib):
        data = self.get_data(xelib)

        # should get required by file handles
        assert ([xelib.name(id_) for id_ in xelib.get_required_by(data.skyrim)] ==
                ['Update.esm',
                 'Dawnguard.esm',
                 'HearthFires.esm',
                 'Dragonborn.esm',
                 'xtest-1.esp',
                 'xtest-2.esp',
                 'xtest-3.esp',
                 'xtest-4.esp',
                 'xtest-5.esp'])

    def test_sort_masters(self, xelib):
        data = self.get_data(xelib)

        # should order masters by load order
        assert xelib.sort_masters(data.xt5)
        masters = xelib.get_elements(data.xt5, 'File Header\\Master Files')
        assert ([xelib.get_value(master, 'MAST') for master in masters] ==
                ['Skyrim.esm', 'Update.esm', 'xtest-3.esp'])

    def test_clean_masters(self, xelib):
        data = self.get_data(xelib)

        # should remove unneeded masters
        assert xelib.clean_masters(data.xt5)
        masters = xelib.get_element(data.xt5, 'File Header\\Master Files')
        assert xelib.element_count(masters) == 0

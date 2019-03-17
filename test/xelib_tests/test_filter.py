from collections import namedtuple
import pytest

from xelib import XelibError

from . fixtures import xelib  # NOQA: for pytest


class TestFilter:
    def get_data(self, xelib):
        test_data = namedtuple('TestData', 'test_file armo rec cell refr dnam')

        test_file = xelib.get_element(0, path='xtest-2.esp')
        armo = xelib.get_element(test_file, path='ARMO')
        rec = xelib.get_element(armo, path='00012E46')
        cell = xelib.get_element(test_file, path='CELL')
        refr = xelib.get_element(test_file, path='000170F0')
        dnam = xelib.get_element(rec, path='DNAM')

        return test_data(test_file=test_file,
                         armo=armo,
                         rec=rec,
                         cell=cell,
                         refr=refr,
                         dnam=dnam)

    def test_filter_record_reset_filter(self, xelib):
        data = self.get_data(xelib)

        # should succeed on records
        assert xelib.filter_record(data.rec)
        assert xelib.filter_record(data.refr)

        # should fail on files
        with pytest.raises(XelibError):
            xelib.filter_record(data.test_file)

        # should fail on groups
        with pytest.raises(XelibError):
            xelib.filter_record(data.armo)

        # should fail on elements
        with pytest.raises(XelibError):
            xelib.filter_record(data.dnam)

        # should filter files
        assert len(xelib.get_elements(0, sort=False, filter=True)) == 1

        # should filter groups
        assert len(xelib.get_elements(
                       data.test_file, sort=False, filter=True)) == 2

        # should filter records
        assert len(xelib.get_elements(
                       data.armo, sort=False, filter=True)) == 1

        # should succeed in resetting filter
        assert xelib.reset_filter()

        # should reset files
        assert len(xelib.get_elements(0, sort=False, filter=True)) == 0

        # should reset groups
        assert len(xelib.get_elements(
                       data.test_file, sort=False, filter=True)) == 0

        # should reset records
        assert len(xelib.get_elements(
                       data.armo, sort=False, filter=True)) == 0

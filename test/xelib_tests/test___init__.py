import pytest
import time

from pyxedit import Xelib, XelibError

from . utils import stripped_block

from . fixtures import xelib  # NOQA: for pytest


TEST_PLUGINS = ['Skyrim.esm',
                'Update.esm',
                'Dawnguard.esm',
                'HearthFires.esm',
                'Dragonborn.esm',
                'xtest-1.esp',
                'xtest-2.esp',
                'xtest-3.esp',
                'xtest-4.esp',
                'xtest-5.esp']


class TestInit:
    def test_manage_handles(self, xelib):
        # helper method to assert xelib error on one line
        def assert_xelib_error(method, handle):
            with pytest.raises(XelibError):
                method(handle)

        # get a bunch of handles
        assert xelib.file_by_name('Skyrim.esm') == 1
        assert xelib.file_by_name('Skyrim.esm') == 2
        assert xelib.file_by_name('Skyrim.esm') == 3
        assert xelib.file_by_name('Skyrim.esm') == 4
        assert xelib.file_by_name('Skyrim.esm') == 5

        # they should all be immediately releasable
        assert xelib.release(1)
        assert xelib.release(2)
        assert xelib.release(3)
        assert xelib.release(4)
        assert xelib.release(5)

        # afterwards they should not be releasable
        assert_xelib_error(xelib.release, 1)
        assert_xelib_error(xelib.release, 2)
        assert_xelib_error(xelib.release, 3)
        assert_xelib_error(xelib.release, 4)
        assert_xelib_error(xelib.release, 5)

        # get a bunch more handles, do some in a a handle management
        # context, make sure they have already been released outside the
        # context
        assert xelib.file_by_name('Skyrim.esm') == 1
        assert xelib.file_by_name('Skyrim.esm') == 2
        with xelib.manage_handles():
            assert xelib.file_by_name('Skyrim.esm') == 3
            assert xelib.file_by_name('Skyrim.esm') == 4
            assert xelib.file_by_name('Skyrim.esm') == 5
        assert_xelib_error(xelib.release, 3)
        assert_xelib_error(xelib.release, 4)
        assert_xelib_error(xelib.release, 5)
        assert xelib.release(1)
        assert xelib.release(2)
        assert_xelib_error(xelib.release, 1)
        assert_xelib_error(xelib.release, 2)

        # multiple levels of nesting, ensure it all works
        assert xelib.file_by_name('Skyrim.esm') == 1
        assert xelib.file_by_name('Skyrim.esm') == 2
        with xelib.manage_handles():
            assert xelib.file_by_name('Skyrim.esm') == 3
            assert xelib.file_by_name('Skyrim.esm') == 4
            with xelib.manage_handles():
                assert xelib.file_by_name('Skyrim.esm') == 5
            assert_xelib_error(xelib.release, 5)
        assert_xelib_error(xelib.release, 3)
        assert_xelib_error(xelib.release, 4)
        assert xelib.release(1)
        assert xelib.release(2)
        assert_xelib_error(xelib.release, 1)
        assert_xelib_error(xelib.release, 2)

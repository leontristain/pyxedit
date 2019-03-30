import pytest
import time

from xedit import Xelib, XelibError

from . utils import stripped_block


class TestInit:
    def test_manage_handles(self):
        # helper method to assert xelib error on one line
        def assert_xelib_error(method, handle):
            with pytest.raises(XelibError):
                method(handle)

        # should save new files
        with Xelib() as xelib:
            # initialize and load plugins
            xelib.set_game_mode(xelib.Games.Skyrim)
            xelib.load_plugins(stripped_block('''
                        Skyrim.esm
                        Update.esm
                        Dawnguard.esm
                        HearthFires.esm
                        Dragonborn.esm
                        xtest-1.esp
                        xtest-2.esp
                        xtest-3.esp
                        xtest-4.esp
                        xtest-5.esp
                        '''))
            assert xelib.get_loader_status() == xelib.LoaderStates.lsActive
            while xelib.get_loader_status() == xelib.LoaderStates.lsActive:
                time.sleep(0.1)

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

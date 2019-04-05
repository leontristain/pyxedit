import pytest

from pyxedit import XelibError

from . fixtures import xelib  # NOQA: for pytest


class TestMeta:
    def test_get_global(self, xelib):
        # should have following globals
        assert xelib.get_global('ProgramPath')
        assert xelib.get_global('Version')
        assert xelib.get_global('GameName')
        assert xelib.get_global('AppName')
        assert xelib.get_global('LongGameName')
        assert xelib.get_global('DataPath')
        assert xelib.get_global('AppDataPath')
        assert xelib.get_global('MyGamesPath')
        assert xelib.get_global('GameIniPath')
        assert xelib.get_global('FileCount')

        # should fail if global does not exist
        with pytest.raises(XelibError):
            xelib.get_global('DoesNotExist')

    def test_set_sort_mode(self, xelib):
        # should succeed for all available sort modes
        assert xelib.set_sort_mode(xelib.SortBy.FormID)
        assert xelib.set_sort_mode(xelib.SortBy.EditorID)
        assert xelib.set_sort_mode(xelib.SortBy.Name)
        assert xelib.set_sort_mode(xelib.SortBy.None_)

    def test_release(self, xelib):
        # should fail if handle is not allocated
        with pytest.raises(XelibError):
            assert xelib.release(100)

        # should fail if null handle is passed
        with pytest.raises(XelibError):
            assert xelib.release(0)

        # should free an allocated handle
        h1 = xelib.file_by_name('Skyrim.esm')
        assert xelib.release(h1)
        h2 = xelib.file_by_name('Skyrim.esm')
        assert xelib.release(h2)
        assert h1 == h2  # next allocation should use the freed handle

    def test_get_duplicate_handles(self, xelib):
        xelib.reset_store()

        # should fail if handle is not allocated
        with pytest.raises(XelibError):
            xelib.get_duplicate_handles(100)

        # should return an empty array if there are no duplicates
        h1 = xelib.file_by_name('Skyrim.esm')
        assert xelib.get_duplicate_handles(h1) == []
        xelib.release(h1)

        # should return duplicates
        h1 = xelib.file_by_name('Skyrim.esm')
        h1 = xelib.file_by_name('Skyrim.esm')
        h1 = xelib.file_by_name('Skyrim.esm')
        h1 = xelib.file_by_name('Skyrim.esm')
        h1 = xelib.file_by_name('Skyrim.esm')
        duplicates = xelib.get_duplicate_handles(h1)
        assert duplicates
        assert len(duplicates) == 4

    def test_reset_store(self, xelib):
        # should clear all handles, where first handle allocated after resetting
        # store should be 1
        xelib.file_by_name('Update.esm')
        assert xelib.file_by_name('Skyrim.esm') != 1
        assert xelib.reset_store()
        assert xelib.file_by_name('Skyrim.esm') == 1

    def test_finalize(self, xelib):
        pytest.skip('Not really sure what to do with this one, xedit-lib test '
                    'implementation may depend on what other test files have '
                    'done, since it mentions an xtest-6.esp which I do not '
                    'have in this scope. Will need to revisit')

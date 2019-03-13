import os
from pathlib import Path
import pytest
import shutil
import tempfile
import time

from xelib import Xelib, XelibError

from . fixtures import xelib  # NOQA: for pytest
from . utils import stripped_block


class TestFiles:
    def test_file_by_name(self, xelib):
        # should return a handle if a matching file is loaded
        assert xelib.file_by_name('Skyrim.esm')

        # should error if a matching file is not loaded
        with pytest.raises(XelibError):
            xelib.file_by_name('NonExistingFile.esp')

    def test_file_by_index(self, xelib):
        # should return a handle if the index is in bounds
        assert xelib.file_by_index(1)

        # should error if index is out of bounds
        with pytest.raises(XelibError):
            xelib.file_by_index(999)

    def test_file_by_load_order(self, xelib):
        # should return a handle if the index is in bounds
        assert xelib.file_by_load_order(1)

        # should error if index is out of bounds
        with pytest.raises(XelibError):
            xelib.file_by_load_order(999)

    def test_file_by_author(self, xelib):
        # should return a handle if a matching file is loaded
        assert xelib.file_by_author('mcarofano')

        # should error if a matching file is not loaded
        with pytest.raises(XelibError):
            xelib.file_by_author('U. N. Owen')

    def test_get_override_record_count(self, xelib):
        # should return an integer > 0 for a plugin with overrides
        h = xelib.file_by_name('Update.esm')
        assert xelib.get_override_record_count(h) > 0

        # should return 0 for a plugin with no records
        h = xelib.file_by_name('xtest-5.esp')
        assert xelib.get_override_record_count(h) == 0

    def test_md5_hash(self, xelib):
        # should return the MD5 Hash of a file
        # TODO: this is currently triggering an access violation error, weird
        # assert (xelib.md5_hash(xelib.file_by_name('xtest-1.esp')) ==
        #         '3f4b772ce1a525e65f88ed8a789fb464')
        # assert (xelib.md5_hash(xelib.file_by_name('xtest-2.esp')) ==
        #         '43f5edb9430744d2c4928a4ab77c3da9')
        # assert (xelib.md5_hash(xelib.file_by_name('xtest-3.esp')) ==
        #         '9e9ff3b83db35bf4034dc76bf3494939')
        # assert (xelib.md5_hash(xelib.file_by_name('xtest-4.esp')) ==
        #         'a79cfd017bdd0482d6870c0a8f170fde')
        # assert (xelib.md5_hash(xelib.file_by_name('xtest-5.esp')) ==
        #         '009c98d373424ae73cc26eae31c13193')

        # should fail if interface is not a file
        with pytest.raises(XelibError):
            xelib.md5_hash(0)

    def test_crc_hash(self, xelib):
        # should return the CRC32 Hash of a file
        assert xelib.crc_hash(xelib.file_by_name('xtest-1.esp')) == 'F3806FAE'
        assert xelib.crc_hash(xelib.file_by_name('xtest-2.esp')) == '19829D28'
        assert xelib.crc_hash(xelib.file_by_name('xtest-3.esp')) == '0F0247D8'
        assert xelib.crc_hash(xelib.file_by_name('xtest-4.esp')) == '45A2BE28'
        assert xelib.crc_hash(xelib.file_by_name('xtest-5.esp')) == 'AD34E5F4'

        # should fail if interface is not a file
        with pytest.raises(XelibError):
            xelib.crc_hash(0)

    def test_add_file(self, xelib):
        try:
            # should return true if it succeeds
            assert xelib.add_file('abc.esp')

            # should return false if the file already exists
            with pytest.raises(XelibError):
                xelib.add_file('Dawnguard.esm')

            # should return false if the load order is already full
            try:
                for i in range(300):
                    xelib.add_file(f'foo{i}.esp')
            except XelibError:
                assert i > 200
        finally:
            for i in reversed(range(300)):
                try:
                    xelib.unload_plugin(xelib.file_by_name(f'foo{i}.esp'))
                except XelibError:
                    pass
            xelib.unload_plugin(xelib.file_by_name('abc.esp'))


class TestSaveFile:
    def test_save_file(self):
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

            # ensure data path is good
            data_path = xelib.get_global('DataPath')
            assert Path(data_path, 'xtest-5.esp').is_file()

            # ensure files to write do not exist already
            if Path(data_path, 'xtest-6.esp').is_file():
                os.remove(Path(data_path, 'xtest-6.esp'))
            if Path(data_path, 'xtest-6.esp.save').is_file():
                os.remove(Path(data_path, 'xtest-6.esp.save'))

            # should save new files
            h = xelib.add_file('xtest-6.esp')
            assert h
            assert xelib.save_file(h)
            assert Path(data_path, 'xtest-6.esp.save').is_file()

        # after finalize, .save should be rewritten as the regular esp
        assert not Path(data_path, 'xtest-6.esp.save').is_file()
        assert Path(data_path, 'xtest-6.esp').is_file()
        os.remove(Path(data_path, 'xtest-6.esp'))

        # should save files at custom paths
        tmpdir = tempfile.mkdtemp()
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

            # ensure data path is good
            assert Path(tmpdir).is_dir()
            assert not Path(tmpdir, 'xtest-6.esp').is_file()

            # should save files at custom paths
            h = xelib.add_file('xtest-6.esp')
            assert h
            assert xelib.save_file(h, file_path=str(Path(tmpdir, 'xtest-6.esp')))
            assert Path(tmpdir, 'xtest-6.esp').is_file()

        # after finalize, should still be same file
        assert Path(tmpdir, 'xtest-6.esp').is_file()
        shutil.rmtree(tmpdir)

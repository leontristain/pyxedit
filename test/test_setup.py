from contextlib import contextmanager
import os
from pathlib import Path
import pytest
import shutil
from textwrap import dedent
import time


from xelib import Xelib, XelibError


@contextmanager
def backed_up(path):
    path = Path(path)
    back_up = path.parent / f'{path.name}.bak'
    try:
        if path.is_file():
            shutil.copyfile(path, back_up)
        elif path.is_dir():
            shutil.copytree(path, back_up)
        elif path.exists():
            raise ValueError(f'backed_up expected file or folder, got '
                             f'something else')
        yield
    finally:
        if back_up.is_file():
            shutil.copyfile(back_up, path)
            os.remove(back_up)
        elif back_up.is_dir():
            if path.exists():
                shutil.rmtree(path)
            shutil.move(back_up, path)


class Timer:
    def __init__(self):
        self._start = None
        self._end = None

    def __enter__(self):
        self._start = time.time()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._end = time.time()

    @property
    def start(self):
        if self._start is None:
            raise ValueError('Timer has not started execution')
        return self._start

    @property
    def end(self):
        if self._end is None:
            raise ValueError('Timer has not finished execution')
        return self._end

    @property
    def seconds(self):
        return self.end - self.start


def stripped_block(text):
    return dedent(text).strip()


@pytest.fixture
def xelib():
    with Xelib() as xelib:
        xelib.set_game_mode(xelib.Games.Skyrim)
        yield xelib


@pytest.fixture(scope='class')
def loaded_xelib():
    with Xelib() as xelib:
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
        with Timer() as load_time:
            while xelib.get_loader_status() == xelib.LoaderStates.lsActive:
                time.sleep(0.1)
        assert load_time.seconds < 10.0
        yield xelib


class TestSetGameMode:
    def test_set_game_mode(self):
        with Xelib() as xelib:
            # AppDataPath should not be set at the beginning
            with pytest.raises(XelibError):
                xelib.get_global('AppDataPath')

            # should succeed for the first time for Skyrim game mode
            xelib.set_game_mode(xelib.Games.Skyrim)

            # Should fail the second time
            with pytest.raises(XelibError):
                xelib.set_game_mode(xelib.Games.SkyrimSE)

            # AppDataPath should now be accessible
            assert xelib.get_global('AppDataPath')


class TestPluginsInspection:
    def app_data_path(self, file_name):
        with Xelib() as xelib:
            xelib.set_game_mode(xelib.Games.Skyrim)
            app_data_path = xelib.get_global('AppDataPath')
            assert app_data_path
        return Path(app_data_path, file_name)

    def test_get_load_order(self):
        plugins_file = self.app_data_path('plugins.txt')
        with backed_up(plugins_file):
            plugins_file.write_text(stripped_block('''
                xtest-5.esp

                # comment
                NonExistingPlugin.esp
                '''))
            with Xelib() as xelib:
                xelib.set_game_mode(xelib.Games.Skyrim)
                load_order = xelib.get_load_order().split()

                # xtest-5.esp should exist
                assert 'xtest-5.esp' in load_order

                # comments should not exist
                assert '# comment' not in load_order

                # empty lines should not exist
                assert all(item.strip() for item in load_order)

                # files that do not exist should not be added
                assert 'NonExistingPlugin.esp' not in load_order

                # missing plugins should be added _after_ the non-missing one
                assert all(
                    load_order.index('xtest-5.esp') < load_order.index(esp)
                    for esp in ['xtest-1.esp',
                                'xtest-2.esp',
                                'xtest-3.esp',
                                'xtest-4.esp'])

                # required plugins should exist in correct positions
                assert (load_order.index('Skyrim.esm') <
                        load_order.index('Update.esm') <
                        load_order.index('xtest-5.esp'))

    def test_get_active_plugins(self):
        plugins_file = self.app_data_path('plugins.txt')
        with backed_up(plugins_file):
            plugins_file.write_text(stripped_block('''
                xtest-5.esp

                # comment
                NonExistingPlugin.esp
                '''))
            with Xelib() as xelib:
                xelib.set_game_mode(xelib.Games.Skyrim)
                plugins = xelib.get_active_plugins().split()

                # xtest-5.esp should exist
                assert 'xtest-5.esp' in plugins

                # comments should not exist
                assert '# comment' not in plugins

                # empty lines should not exist
                assert all(item.strip() for item in plugins)

                # should add required plugins
                assert 'Skyrim.esm' in plugins
                assert 'Update.esm' in plugins


class TestSetup:
    def test_load_plugins(self, loaded_xelib):
        # there should be 10 files
        assert loaded_xelib.get_global('FileCount') == '10'

    def test_build_references(self, loaded_xelib):
        file_handle = loaded_xelib.file_by_name('xtest-2.esp')

        with Timer() as build_references_time:
            assert loaded_xelib.build_references(file_handle, sync=False)
        assert build_references_time.seconds < 2

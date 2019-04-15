from pathlib import Path
import pytest
import time

from pyxedit import Xelib, XelibError

from . fixtures import xelib  # NOQA: for pytest
from . utils import backed_up, Timer, stripped_block


class TestSetup:
    def app_data_path(self, file_name):
        with (Xelib(game_mode=Xelib.GameModes.TES5)
                  .session(load_plugins=False)) as xelib:
            app_data_path = xelib.get_global('AppDataPath')
            assert app_data_path
        return Path(app_data_path, file_name)

    def test_set_game_mode(self):
        with Xelib(game_mode=None).session(load_plugins=False) as xelib:
            # AppDataPath should not be set at the beginning
            with pytest.raises(XelibError):
                xelib.get_global('AppDataPath')

            # should succeed for the first time for Skyrim game mode
            xelib.set_game_mode(xelib.GameModes.TES5)

            # Should fail the second time
            with pytest.raises(XelibError):
                xelib.set_game_mode(xelib.GameModes.SSE)

            # AppDataPath should now be accessible
            assert xelib.get_global('AppDataPath')

    def test_get_load_order(self):
        plugins_file = self.app_data_path('plugins.txt')
        with backed_up(plugins_file):
            plugins_file.write_text(stripped_block('''
                xtest-5.esp

                # comment
                NonExistingPlugin.esp
                '''))
            with (Xelib(game_mode=Xelib.GameModes.TES5)
                      .session(load_plugins=False)) as xelib:
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
            with (Xelib(game_mode=Xelib.GameModes.TES5)
                      .session(load_plugins=False)) as xelib:
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

    def test_load_plugins(self, xelib):
        # there should be 11 files
        # (hardcoded + Skyrim + Update + 3 DLCs + 5 test esps)
        assert xelib.get_global('FileCount') == '11'

    def test_build_references(self, xelib):
        handle = xelib.file_by_name('xtest-2.esp')

        with Timer() as build_references_time:
            assert xelib.build_references(handle, sync=False)
        assert build_references_time.seconds < 2

    def test_unload_load_plugin(self, xelib):
        # should fail if required by other loaded plugins
        handle = xelib.file_by_name('Update.esm')
        with pytest.raises(XelibError):
            xelib.unload_plugin(handle)

        # otherwise, unload should be successful
        handle = xelib.file_by_name('xtest-5.esp')
        assert xelib.unload_plugin(handle)

        # should update FileCount global
        assert xelib.get_global('FileCount') == '10'

        # should be able to load it back in
        xelib.load_plugin('xtest-5.esp')
        assert xelib.get_loader_status() == xelib.LoaderStates.Active
        with Timer() as load_time:
            while xelib.get_loader_status() == xelib.LoaderStates.Active:
                time.sleep(0.1)
        assert load_time.seconds < 0.5

        # should update FileCount global
        assert xelib.get_global('FileCount') == '11'

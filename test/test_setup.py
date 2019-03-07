from contextlib import contextmanager
import os
from pathlib import Path
import shutil
import unittest
from textwrap import dedent


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


class SetupTests(unittest.TestCase):
    def test_set_game_mode(self):
        with Xelib() as xelib:
            # AppDataPath should not be set at the beginning
            with self.assertRaises(XelibError):
                self.assertFalse(xelib.get_global('AppDataPath'))

            # should succeed for the first time for Skyrim game mode
            xelib.set_game_mode(xelib.Games.Skyrim)

            # Should fail the second time
            with self.assertRaises(XelibError):
                xelib.set_game_mode(xelib.Games.SkyrimSE)

            # AppDataPath should now be accessible
            self.assertTrue(xelib.get_global('AppDataPath'))

    def test_get_load_order(self):
        with Xelib() as xelib:
            xelib.set_game_mode(xelib.Games.Skyrim)
            app_data_path = xelib.get_global('AppDataPath')

        plugins_file = Path(app_data_path, 'plugins.txt')
        with backed_up(plugins_file):
            plugins_file.write_text(dedent('''
                xtest-5.esp

                # comment
                NonExistingPlugin.esp
                ''').strip())
            with Xelib() as xelib:
                xelib.set_game_mode(xelib.Games.Skyrim)
                load_order = xelib.get_load_order().split()

                # xtest-5.esp should exist
                self.assertIn('xtest-5.esp', load_order)

                # comments should not exist
                self.assertNotIn('# comment', load_order)

                # empty lines should not exist
                self.assertTrue(all(item.strip() for item in load_order))

                # files that do not exist should not be added
                self.assertNotIn('NonExistingPlugin.esp', load_order)

                # missing plugins should be added _after_ the non-missing one
                self.assertGreater(load_order.index('xtest-1.esp'),
                                   load_order.index('xtest-5.esp'))
                self.assertGreater(load_order.index('xtest-2.esp'),
                                   load_order.index('xtest-5.esp'))
                self.assertGreater(load_order.index('xtest-3.esp'),
                                   load_order.index('xtest-5.esp'))
                self.assertGreater(load_order.index('xtest-4.esp'),
                                   load_order.index('xtest-5.esp'))

                # required plugins should exist in correct positions
                self.assertGreater(load_order.index('xtest-5.esp'),
                                   load_order.index('Update.esm'))
                self.assertGreater(load_order.index('Update.esm'),
                                   load_order.index('Skyrim.esm'))


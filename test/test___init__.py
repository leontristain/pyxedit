import unittest

from xelib import Xelib


class InitTests(unittest.TestCase):
    def test_load_unload_lib(self):
        with Xelib() as lib:
            lib.set_game_mode(lib.Games.Skyrim)
            with self.assertRaises(Exception):
                lib.set_game_mode(lib.Games.SkyrimSE)
        with Xelib() as lib:
            lib.set_game_mode(lib.Games.SkyrimSE)
        with Xelib() as lib:
            pass

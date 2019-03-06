import unittest


from xelib import Xelib, XelibError


class SetupTests(unittest.TestCase):
    def test_set_game_mode(self):
        with Xelib() as xelib:
            # should succeed for the first time for Skyrim game mode
            xelib.set_game_mode(xelib.Games.Skyrim)

            # Should fail the second time
            with self.assertRaises(XelibError):
                xelib.set_game_mode(xelib.Games.SkyrimSE)

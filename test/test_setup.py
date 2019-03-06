import unittest

from xelib.helpers import XelibError
from xelib import setup


class SetupTests(unittest.TestCase):
    def test_set_game_mode(self):
        # should succeed for the first time for Skyrim game mode
        setup.set_game_mode(setup.Games.Skyrim)

        # Should fail the second time
        with self.assertRaises(XelibError):
            setup.set_game_mode(setup.Games.SkyrimSE)

import pytest
import time

from xedit import Xelib

from . utils import stripped_block, Timer


@pytest.fixture(scope='class')
def xelib():
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

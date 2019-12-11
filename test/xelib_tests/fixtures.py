import pytest

from pyxedit import Xelib


@pytest.fixture(scope='class')
def xelib():
    plugins = ['Skyrim.esm',
               'Update.esm',
               'Dawnguard.esm',
               'HearthFires.esm',
               'Dragonborn.esm',
               'xtest-1.esp',
               'xtest-2.esp',
               'xtest-3.esp',
               'xtest-4.esp',
               'xtest-5.esp']

    with Xelib(game_mode=Xelib.GameModes.TES5,
               plugins=plugins,
               xeditlib_path='D:\\git\\xedit-lib\\XEditLib.dll').session() as xelib:
        yield xelib

from pathlib import Path
import pytest

from pyxedit import XelibError

from . fixtures import xelib  # NOQA: for pytest


class TestResources:
    def test_get_container_files(self, xelib):
        # should fail if container is not loaded
        with pytest.raises(XelibError):
            xelib.get_container_files('blah', '')

        # should return files in container
        p = str(Path(xelib.get_global('DataPath'), 'Skyrim - Shaders.bsa'))
        assert len(xelib.get_container_files(p, '')) == 122

        # should filter properly
        p = str(Path(xelib.get_global('DataPath'), 'Skyrim - Textures.bsa'))
        assert len(xelib.get_container_files(p, 'textures\\sky\\')) == 47

    def test_get_texture_data(self, xelib):
        pytest.skip('this method is not yet implemented on my side')
        # should fail if the resource does not exist
        # with pytest.raises(XelibError):
        #     xelib.get_texture_data('abcdefghijk')

        # should return correct bitmap if resource exists
        # w, h = xelib.get_texture_data('textures\\sky\\skyrimclouds01.dds')

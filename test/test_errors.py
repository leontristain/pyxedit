import pytest
import time

from xelib import XelibError

from . fixtures import xelib  # NOQA: for pytest


class TestErrors:
    def test_get_errors(self, xelib):
        raise pytest.skip('figure out why this is failing later')
        # should fail if no error check has been performed
        with pytest.raises(XelibError):
            xelib.get_errors()

        # should return errors
        h = xelib.file_by_name('xtest-4.esp')
        xelib.check_for_errors(h)
        while not xelib.get_error_thread_done():
            time.sleep(0.1)
        errors = xelib.get_errors()
        assert errors and len(errors) > 0  # TODO: why is this failing?

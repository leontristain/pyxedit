from . fixtures import xelib  # NOQA: for pytest


class TestMessages:
    def test_get_exception_message(self, xelib):
        # should get the last exception message
        xelib.file_by_name('b.esp', ex=False)
        xelib.file_by_name('a.esp', ex=False)
        exception_message = xelib.get_exception_message()
        assert 'Failed to find file with name: a.esp' in exception_message

        # should clear exception message after retrieval
        assert xelib.get_exception_message() == ''

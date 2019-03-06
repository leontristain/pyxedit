import unittest

from xelib import meta


class MetaTests(unittest.TestCase):
    def test_xelib_context(self):
        with meta.xelib_context():
            pass


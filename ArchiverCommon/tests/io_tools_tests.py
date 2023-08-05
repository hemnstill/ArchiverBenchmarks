import unittest

from ArchiverCommon.io_tools import get_name_without_extensions


class IOToolsTests(unittest.TestCase):
    def test_without_ext(self):
        self.assertEqual('a1', get_name_without_extensions('/home/a1'))

    def test_without_suffixes(self):
        self.assertEqual('a1', get_name_without_extensions('/home/a1.tar'))

    def test_without_many_suffixes(self):
        self.assertEqual('a1.many.suffixes', get_name_without_extensions('/home/a1.many.suffixes.tar.gz'))

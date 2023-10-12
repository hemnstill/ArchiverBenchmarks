import unittest

import test_tools

from ArchiverCommon.archiver_tools import bsdtar_tool, zstd_tool


class ZstdVersionTest(unittest.TestCase):
    def test_version(self):
        self.assertEqual('*** Zstandard CLI (64-bit) v1.5.5, by Yann Collet ***',
                         zstd_tool.get_version())

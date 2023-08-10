import unittest

import test_tools

from ArchiverCommon.archiver_tools import bsdtar_tool


class BsdtarVersionTest(unittest.TestCase):
    def test_362_version(self):
        self.assertEqual('bsdtar 3.6.2 - libarchive 3.6.2 zlib/1.2.12 liblzma/5.2.5 libzstd/1.5.2',
                         bsdtar_tool.get_version(bsdtar_tool.version_362))

    def test_371_version(self):
        self.assertEqual('bsdtar 3.7.1 - libarchive 3.7.1 zlib/1.2.12 liblzma/5.2.5 libzstd/1.5.2',
                         bsdtar_tool.get_version(bsdtar_tool.version_371))
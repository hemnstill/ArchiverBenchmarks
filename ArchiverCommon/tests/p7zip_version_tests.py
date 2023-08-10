import unittest

import test_tools

from ArchiverCommon.archiver_tools import p7zip_tool


class P7ZipVersionTest(unittest.TestCase):
    def test_21_07_version(self):
        self.assertEqual('7-Zip 21.07 (x64) : Copyright (c) 1999-2021 Igor Pavlov : 2021-12-26',
                         p7zip_tool.get_version(p7zip_tool.version_21_07))

    def test_23_01_version(self):
        self.assertEqual('7-Zip (z) 23.01 (x64) : Copyright (c) 1999-2023 Igor Pavlov : 2023-06-20',
                         p7zip_tool.get_version(p7zip_tool.version_23_01))
import os.path
import pathlib
import unittest

import test_tools

_self_path: str = os.path.dirname(os.path.realpath(__file__))

from ArchiverCommon import io_tools, common_paths
from ArchiverCommon.archiver_tools import bsdtar_tool, p7zip_tool, python_archiver_tool


class PaxHeadersTests(unittest.TestCase):
    def setUp(self) -> None:
        if not io_tools.try_create_or_clean_dir(common_paths.temp_path):
            raise IOError('try_create_or_clean_dir')

        self.test_archive_dirpath = common_paths.create_temp_path('PaxHeadersTests')
        self.test_archive_filepath = os.path.join(self.test_archive_dirpath, 'with_pax.tar')

    def create_tar_with_pax_headers_with_python(self):
        test_archive_dirpath = test_tools.create_dir_with_utf8_filename('test_archive')
        python_archiver_tool.create_tar_with_pax_headers(test_archive_dirpath, self.test_archive_filepath)

    def create_tar_with_pax_headers_with_bsdtar(self):
        test_archive_dirpath = test_tools.create_dir_with_utf8_filename('test_archive_python')
        python_archiver_tool.create_tar_with_pax_headers(test_archive_dirpath, self.test_archive_filepath)

        test_archive_dirpath = test_tools.create_dir_with_utf8_filename('test_archive')
        bsdtar_tool.append_tar(test_archive_dirpath, self.test_archive_filepath)

    def test_get_pax_header_from_python(self):
        self.create_tar_with_pax_headers_with_python()
        self.assertEqual({'test_header': 'test_header_value'}, python_archiver_tool.get_pax_headers(self.test_archive_filepath))

    def test_get_pax_header_from_bsdtar(self):
        self.create_tar_with_pax_headers_with_bsdtar()
        self.assertEqual({'test_header': 'test_header_value'}, python_archiver_tool.get_pax_headers(self.test_archive_filepath))
import os.path
import pathlib
import sys
import unittest

import test_tools

_self_path: str = os.path.dirname(os.path.realpath(__file__))

from ArchiverCommon import io_tools, common_paths
from ArchiverCommon.archiver_tools import bsdtar_tool, p7zip_tool, python_archiver_tool


class FileNameCheckerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.etalon_windows_dirpath = os.path.join(_self_path, 'windows')
        self.etalon_linux_dirpath = os.path.join(_self_path, 'linux')

    def test_check_utf8_file_names_linux(self):
        for archive_file in pathlib.Path(self.etalon_linux_dirpath).iterdir():
            if not archive_file.is_file():
                continue
            non_ascii_filename = python_archiver_tool.get_first_non_ascii_filename(str(archive_file))
            if not non_ascii_filename:
                print(f"Not found utf-8: '{non_ascii_filename}' in '{archive_file}'")

    def test_check_utf8_file_names_windows(self):
        for archive_file in pathlib.Path(self.etalon_windows_dirpath).iterdir():
            if not archive_file.is_file():
                continue
            non_ascii_filename = python_archiver_tool.get_first_non_ascii_filename(str(archive_file))
            if not non_ascii_filename:
                print(f"Not found utf-8: '{non_ascii_filename}' in '{archive_file}'")
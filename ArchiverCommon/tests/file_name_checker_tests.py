import os.path
import pathlib
import subprocess
import unittest

import test_tools

_self_path: str = os.path.dirname(os.path.realpath(__file__))

from ArchiverCommon import artifact_tools


class FileNameCheckerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.etalon_windows_dirpath = os.path.join(_self_path, 'windows')
        self.etalon_linux_dirpath = os.path.join(_self_path, 'linux')

    def test_check_utf8_file_names_linux(self):
        for archive_file in pathlib.Path(self.etalon_linux_dirpath).iterdir():
            if not archive_file.is_file():
                continue
            try:
                artifact_tools.check_first_utf8_filename(str(archive_file))
            except subprocess.CalledProcessError as ex:
                print(str(ex).encode('utf-8', 'replace'))

    def test_check_utf8_file_names_windows(self):
        for archive_file in pathlib.Path(self.etalon_windows_dirpath).iterdir():
            if not archive_file.is_file():
                continue
            try:
                artifact_tools.check_first_utf8_filename(str(archive_file))
            except subprocess.CalledProcessError as ex:
                print(str(ex).encode('utf-8', 'replace'))
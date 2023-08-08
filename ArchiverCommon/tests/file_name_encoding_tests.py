import os.path
import pathlib
import sys
import unittest

import test_tools

_self_path: str = os.path.dirname(os.path.realpath(__file__))

from ArchiverCommon import io_tools, common_paths
from ArchiverCommon.archiver_tools import bsdtar_tool, p7zip_tool, python_archiver_tool


class FileNameEncodingTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        if not io_tools.try_create_or_clean_dir(common_paths.temp_path):
            raise IOError('try_create_or_clean_dir')

        cls.archive_formats = ['.zip',
                               '.tar.gz',
                               ]
        cls.archiver_tools_extract = [
            bsdtar_tool,
            p7zip_tool,
            python_archiver_tool
        ]
        cls.archiver_tools_create = [
            bsdtar_tool,
            p7zip_tool,
            python_archiver_tool
        ]
        cls.etalon_windows_dirpath = os.path.join(_self_path, 'windows')
        cls.etalon_linux_dirpath = os.path.join(_self_path, 'linux')

    def setUp(self) -> None:
        self.result_dirpath = common_paths.create_temp_path('result')
        self.result_extracted_dirpath = common_paths.create_temp_path('result_extract')
        self.create_utf8()

    @classmethod
    def get_tool_name(cls, archiver_tool):
        return pathlib.Path(archiver_tool.__name__).suffix.strip('.')

    def create_utf8(self):
        test_archive_dirpath = test_tools.create_dir_with_utf8_filename('test_archive_python')

        for archive_format in self.archive_formats:
            for archiver_tool in self.archiver_tools_create:
                archive_file_path = os.path.join(self.result_dirpath,
                                                 f'{self.get_tool_name(archiver_tool)}{archive_format}')
                archiver_tool.create(test_archive_dirpath, archive_file_path)

    def check_filename(self, extract_dir_path: str):
        utf8_file_path = os.path.join(extract_dir_path, 'test_archive', test_tools.utf_8_filename)
        utf8_file_path2 = os.path.join(extract_dir_path, test_tools.utf_8_filename)
        if not pathlib.Path(utf8_file_path).is_file() and not pathlib.Path(utf8_file_path2).is_file():
            print(f"{self._testMethodName} '{extract_dir_path}' failed.")

    def test_extract_utf8(self):
        for archiver_tool_from in self.archiver_tools_create:
            for archiver_tool in self.archiver_tools_extract:
                for archive_format in self.archive_formats:
                    archive_file_path = os.path.join(self.result_dirpath,
                                                     f'{self.get_tool_name(archiver_tool_from)}{archive_format}')
                    extracted_dir_path = os.path.join(self.result_extracted_dirpath,
                                                      f"{self.get_tool_name(archiver_tool)}-{self.get_tool_name(archiver_tool_from)}{archive_format}")
                    archiver_tool.extract(archive_file_path, extracted_dir_path)
                    self.check_filename(extracted_dir_path)

    @unittest.skipIf(sys.platform.startswith('win'), 'same as test_extract_utf8')
    def test_extract_etalon_data_windows(self):
        for archiver_tool_from in self.archiver_tools_create:
            for archiver_tool in self.archiver_tools_extract:
                for archive_format in self.archive_formats:
                    archive_file_path = os.path.join(self.etalon_windows_dirpath,
                                                     f'{self.get_tool_name(archiver_tool_from)}{archive_format}')
                    extracted_dir_path = os.path.join(self.result_extracted_dirpath,
                                                      f"{self.get_tool_name(archiver_tool)}-{self.get_tool_name(archiver_tool_from)}{archive_format}")
                    if not os.path.isfile(archive_file_path):
                        print(f"'skip '{archive_file_path}'")
                        continue
                    archiver_tool.extract(archive_file_path, extracted_dir_path)
                    self.check_filename(extracted_dir_path)

    @unittest.skipIf(not sys.platform.startswith('win'), 'same as test_extract_utf8')
    def test_extract_etalon_data_linux(self):
        for archiver_tool_from in self.archiver_tools_create:
            for archiver_tool in self.archiver_tools_extract:
                for archive_format in self.archive_formats:
                    archive_file_path = os.path.join(self.etalon_linux_dirpath,
                                                     f'{self.get_tool_name(archiver_tool_from)}{archive_format}')
                    extracted_dir_path = os.path.join(self.result_extracted_dirpath,
                                                      f"{self.get_tool_name(archiver_tool)}-{self.get_tool_name(archiver_tool_from)}{archive_format}")
                    if not os.path.isfile(archive_file_path):
                        print(f"'skip '{archive_file_path}'")
                        continue
                    archiver_tool.extract(archive_file_path, extracted_dir_path)
                    self.check_filename(extracted_dir_path)

import os.path
import pathlib
import unittest

import test_tools

_self_path: str = os.path.dirname(os.path.realpath(__file__))

from ArchiverCommon import io_tools, common_paths
from ArchiverCommon.archiver_tools import bsdtar_tool, p7zip_tool


class FileNameEncodingTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        if not io_tools.try_create_or_clean_dir(common_paths.temp_path):
            raise IOError('try_create_or_clean_dir')
        cls.result_dirpath = common_paths.create_temp_path('result')
        cls.result_extracted_dirpath = common_paths.create_temp_path('result_extract')
        cls.archive_formats = ['.zip',
                               '.tar.gz',
                               ]
        cls.archiver_tools_extract = [
            bsdtar_tool,
            p7zip_tool,
        ]

        cls.archiver_tools_create = [bsdtar_tool,
                                     p7zip_tool,
                                     ]
        cls.utf_8_filename = 'พลัง'
        cls.create_utf8()

        cls.etalon_windows_dirpath = os.path.join(_self_path, 'windows')
        cls.etalon_linux_dirpath = os.path.join(_self_path, 'linux')

    @classmethod
    def get_tool_name(cls, archiver_tool):
        return pathlib.Path(archiver_tool.__name__).suffix.strip('.')

    @classmethod
    def create_utf8(cls):
        test_archive_dirpath = common_paths.create_temp_path('test_archive')
        utf8_file_path = os.path.join(test_archive_dirpath, cls.utf_8_filename)
        io_tools.write_text(utf8_file_path, 'test content')

        for archive_format in cls.archive_formats:
            for archiver_tool in cls.archiver_tools_create:
                archive_file_path = os.path.join(cls.result_dirpath,
                                                 f'{cls.get_tool_name(archiver_tool)}{archive_format}')
                archiver_tool.create(test_archive_dirpath, archive_file_path)

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

    def check_filename(self, extract_dir_path: str):
        utf8_file_path = os.path.join(extract_dir_path, 'test_archive', self.utf_8_filename)
        utf8_file_path2 = os.path.join(extract_dir_path, self.utf_8_filename)
        if not pathlib.Path(utf8_file_path).is_file() and not pathlib.Path(utf8_file_path2).is_file():
            print(f"'{extract_dir_path}' failed.")

    def test_extract_etalon_data_windows(self):
        for archiver_tool_from in self.archiver_tools_create:
            for archiver_tool in self.archiver_tools_extract:
                for archive_format in self.archive_formats:
                    archive_file_path = os.path.join(self.etalon_windows_dirpath,
                                                     f'{self.get_tool_name(archiver_tool_from)}{archive_format}')
                    extracted_dir_path = os.path.join(self.result_extracted_dirpath,
                                                      f"{self.get_tool_name(archiver_tool)}-{self.get_tool_name(archiver_tool_from)}{archive_format}")
                    archiver_tool.extract(archive_file_path, extracted_dir_path)
                    self.check_filename(extracted_dir_path)

    def test_extract_etalon_data_linux(self):
        for archiver_tool_from in self.archiver_tools_create:
            for archiver_tool in self.archiver_tools_extract:
                for archive_format in self.archive_formats:
                    archive_file_path = os.path.join(self.etalon_linux_dirpath,
                                                     f'{self.get_tool_name(archiver_tool_from)}{archive_format}')
                    extracted_dir_path = os.path.join(self.result_extracted_dirpath,
                                                      f"{self.get_tool_name(archiver_tool)}-{self.get_tool_name(archiver_tool_from)}{archive_format}")
                    archiver_tool.extract(archive_file_path, extracted_dir_path)
                    self.check_filename(extracted_dir_path)
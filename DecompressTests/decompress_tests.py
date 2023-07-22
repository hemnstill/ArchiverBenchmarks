import os
import shutil
import unittest

from DecompressTests import wget_tool, bsdtar_tool, io_tools

_self_path: str = os.path.dirname(os.path.realpath(__file__))
data_path: str = os.path.join(_self_path, 'data')
extracted_data_path: str = os.path.join(_self_path, 'extracted_data')


def download_artifact(name: str) -> None:
    artifact_file_path = os.path.join(data_path, name)
    artifact_url = f'https://github.com/hemnstill/ArchiverBenchmarks/releases/download/init/{name}'
    if not os.path.isfile(artifact_file_path):
        wget_tool.download_url(artifact_url, artifact_file_path)


class DecompressTests(unittest.TestCase):

    def setUp(self) -> None:
        download_artifact('7MB.7z')
        if not io_tools.try_create_or_clean_dir(extracted_data_path):
            raise IOError(f'Cannot try_create_or_clean_dir: {extracted_data_path}')

    def test_extract_zip(self):
        output_dir_path = os.path.join(extracted_data_path, '7MB.7z_content')
        os.makedirs(output_dir_path, exist_ok=True)
        bsdtar_tool.extract(os.path.join(data_path, '7MB.7z'), output_dir_path)

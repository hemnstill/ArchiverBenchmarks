import os
import sys
import unittest
from contextlib import suppress
from timeit import timeit

_self_path: str = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.dirname(_self_path)
if root_path not in sys.path:
    sys.path.append(root_path)

from DecompressTests import wget_tool, bsdtar_tool, io_tools, p7zip_tool, common_paths, models, execution_renderer, \
    python_archiver_tool, p7zip_zstd_tool, zstd_tool, pigz_tool


def artifacts_data() -> dict[str, models.ArtifactInfo]:
    return {
        # '5MB.tar': models.ArtifactInfo(name='5MB.tar', size=5918720),
        '7MB.7z': models.ArtifactInfo(name='7MB.7z', size=8023251),
        '12MB.tar.gz': models.ArtifactInfo(name='12MB.tar.gz', size=13047645),
        '33MB.tar.zst': models.ArtifactInfo(name='33MB.tar.zst', size=34635880),
        '116MB.zip': models.ArtifactInfo(name='116MB.zip', size=122518995),
        '154MB.tar.gz': models.ArtifactInfo(name='154MB.tar.gz', size=162315691),
    }


def archiver_tools() -> dict[str, models.ArchiverInfo]:
    return {
        'bsdtar-3.6.2': models.ArchiverInfo(name='bsdtar-3.6.2', extract=bsdtar_tool.extract),
        '7zip-21.07': models.ArchiverInfo(name='7zip-21.07', extract=p7zip_tool.extract),
        '7z22.01-zstd': models.ArchiverInfo(name='7z22.01-zstd', extract=p7zip_zstd_tool.extract),
        'python-3.11': models.ArchiverInfo(name='python-3.11', extract=python_archiver_tool.extract),
        'zstd-1.5.5': models.ArchiverInfo(name='zstd-1.5.5', extract=zstd_tool.extract),
        'pigz-2.4': models.ArchiverInfo(name='pigz-2.4', extract=pigz_tool.extract),
    }


def download_artifact(artifact: models.ArtifactInfo) -> None:
    artifact_file_path = os.path.join(common_paths.data_path, artifact.name)
    artifact_url = f'https://github.com/hemnstill/ArchiverBenchmarks/releases/download/init/{artifact.name}'
    if not os.path.isfile(artifact_file_path) or os.path.getsize(artifact_file_path) != artifact.size:
        wget_tool.download_url(artifact_url, artifact_file_path)
    if os.path.getsize(artifact_file_path) != artifact.size:
        raise IOError(f"Download failed: '{artifact_url}'\n'{artifact.name}' file size {os.path.getsize(artifact_file_path)}, but should be {artifact.size}")


class DecompressTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.execution_info: list[models.ExecutionInfo] = []
        print(f'clean_dir {common_paths.extracted_data_path} ...')
        if not io_tools.try_create_or_clean_dir(common_paths.extracted_data_path):
            raise IOError(f'Cannot try_create_or_clean_dir: {common_paths.extracted_data_path}')

    @classmethod
    def tearDownClass(cls) -> None:
        execution_renderer.render(cls.execution_info)

    def setUp(self) -> None:
        for artifact in artifacts_data().values():
            download_artifact(artifact)

    def test_extract(self):
        for artifact in artifacts_data().values():
            for archiver in archiver_tools().values():
                print(f"test_extract '{artifact.name}' with '{archiver.name}'")
                output_dir_path = os.path.join(common_paths.extracted_data_path, f"{artifact.name}_{archiver.name}")
                execution_time = None
                with suppress(NotImplementedError):
                    execution_time = round(0.5 * timeit(lambda: archiver.extract(os.path.join(common_paths.data_path, artifact.name), output_dir_path), number=2), 3)
                self.execution_info.append(models.ExecutionInfo(execution_time=execution_time,
                                                         artifact=artifact,
                                                         archiver=archiver.name))
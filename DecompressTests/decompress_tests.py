import dataclasses
import os
import pprint
import unittest
from timeit import timeit
from typing import Callable

from DecompressTests import wget_tool, bsdtar_tool, io_tools, p7zip_tool

_self_path: str = os.path.dirname(os.path.realpath(__file__))
data_path: str = os.path.join(_self_path, 'data')
extracted_data_path: str = os.path.join(_self_path, 'extracted_data')


@dataclasses.dataclass
class ArtifactInfo:
    name: str
    size: int


@dataclasses.dataclass
class ArchiverInfo:
    name: str
    extract: Callable


@dataclasses.dataclass
class ExecutionInfo:
    execution_time: float
    artifact: ArtifactInfo
    archiver: str


def artifacts_data() -> dict[str, ArtifactInfo]:
    return {
        '7MB.7z': ArtifactInfo(name='7MB.7z', size=8023251),
        # '116MB.zip': ArtifactInfo(name='116MB.zip', size=122518995),
    }


def archiver_tools() -> dict[str, ArchiverInfo]:
    return {
        'bsdtar-3.6.2': ArchiverInfo(name='bsdtar-3.6.2', extract=bsdtar_tool.extract),
        '7zip-21.07': ArchiverInfo(name='7zip-21.07', extract=p7zip_tool.extract),
    }


def download_artifact(artifact: ArtifactInfo) -> None:
    artifact_file_path = os.path.join(data_path, artifact.name)
    artifact_url = f'https://github.com/hemnstill/ArchiverBenchmarks/releases/download/init/{artifact.name}'
    if not os.path.isfile(artifact_file_path) or os.path.getsize(artifact_file_path) != artifact.size:
        wget_tool.download_url(artifact_url, artifact_file_path)
    if os.path.getsize(artifact_file_path) != artifact.size:
        raise IOError(f"Download failed: '{artifact_url}'\n'{artifact.name}' file size {os.path.getsize(artifact_file_path)}, but should be {artifact.size}")


class DecompressTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.execution_info: list[ExecutionInfo] = []
        if not io_tools.try_create_or_clean_dir(extracted_data_path):
            raise IOError(f'Cannot try_create_or_clean_dir: {extracted_data_path}')

    @classmethod
    def tearDownClass(cls) -> None:
        pprint.pprint(cls.execution_info)

    def setUp(self) -> None:
        for artifact in artifacts_data().values():
            download_artifact(artifact)

    def test_extract(self):
        for artifact in artifacts_data().values():
            for archiver in archiver_tools().values():
                output_dir_path = os.path.join(extracted_data_path, f"{artifact.name}_{archiver.name}")
                os.makedirs(output_dir_path, exist_ok=True)

                execution_time = round(0.5 * timeit(lambda: archiver.extract(os.path.join(data_path, artifact.name), output_dir_path), number=2), 3)
                self.execution_info.append(ExecutionInfo(execution_time=execution_time,
                                                         artifact=artifact,
                                                         archiver=archiver.name))
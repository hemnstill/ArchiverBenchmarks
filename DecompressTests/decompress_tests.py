import os
import sys
import unittest
from contextlib import suppress
from timeit import timeit
from airium import Airium

_self_path: str = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.dirname(_self_path)
if root_path not in sys.path:
    sys.path.append(root_path)

from DecompressTests import wget_tool, io_tools, common_paths, models, execution_renderer
from DecompressTests import archiver_tools


def artifacts_data() -> dict[str, models.ArtifactInfo]:
    if os.environ['self_toolset_name'] == 'build-local':
        return {'116MB.zip': models.ArtifactInfo(name='116MB.zip', size=122518995, files_count=2123)}

    if os.environ['self_toolset_name'] in ('build-windows-single', 'build-linux-single'):
        return {'git-sdk-64-main.zip': models.ArtifactInfo(name='git-sdk-64-main.zip', size=1407960952, files_count=108168)}

    return {
        '200MB.tar': models.ArtifactInfo(name='200MB.tar', size=214394880, files_count=5800),
        '7MB.7z': models.ArtifactInfo(name='7MB.7z', size=8023251, files_count=949),
        '12MB.tar.gz': models.ArtifactInfo(name='12MB.tar.gz', size=13047645, files_count=2056),
        '33MB.tar.zst': models.ArtifactInfo(name='33MB.tar.zst', size=34635880, files_count=5800),
        '116MB.zip': models.ArtifactInfo(name='116MB.zip', size=122518995, files_count=2123),
        '154MB.tar.gz': models.ArtifactInfo(name='154MB.tar.gz', size=162315691, files_count=2150),
    }


def get_archiver_tools() -> dict[str, models.ArchiverInfo]:
    return {
        'bsdtar-3.6.2': models.ArchiverInfo(name='bsdtar-3.6.2', extract=archiver_tools.bsdtar_tool.extract),
        '7zip-21.07': models.ArchiverInfo(name='7zip-21.07', extract=archiver_tools.p7zip_tool.extract),
        '7z22.01-zstd': models.ArchiverInfo(name='7z22.01-zstd', extract=archiver_tools.p7zip_zstd_tool.extract),
        'zstd-1.5.5': models.ArchiverInfo(name='zstd-1.5.5', extract=archiver_tools.zstd_tool.extract),
        'igzip-2.30': models.ArchiverInfo(name='igzip-2.30', extract=archiver_tools.igzip_tool.extract),
        'pigz-2.4': models.ArchiverInfo(name='pigz-2.4', extract=archiver_tools.pigz_tool.extract),
        'rapidgzip-0.7.0': models.ArchiverInfo(name='rapidgzip-0.7.0', extract=archiver_tools.rapidgzip_tool.extract),
        'ripunzip-0.4.0': models.ArchiverInfo(name='ripunzip-0.4.0', extract=archiver_tools.ripunzip_tool.extract),
        'archiver-3.5.1': models.ArchiverInfo(name='archiver-3.5.1', extract=archiver_tools.archiver_tool.extract),
        'unar-1.8.1': models.ArchiverInfo(name='unar-1.8.1', extract=archiver_tools.unar_tool.extract),
        'python-3.11': models.ArchiverInfo(name='python-3.11', extract=archiver_tools.python_archiver_tool.extract),
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
        if not os.environ.get('self_toolset_name'):
            os.environ['self_toolset_name'] = 'build-local'

        print(f"self_toolset_name: {os.environ['self_toolset_name']}")

    @classmethod
    def tearDownClass(cls) -> None:
        execution_renderer.render(cls.execution_info)

    def setUp(self) -> None:
        for artifact in artifacts_data().values():
            download_artifact(artifact)

    def check_content(self, artifact: models.ArtifactInfo, output_dir_path: str):
        if not os.path.isdir(output_dir_path):
            return False

        output_dir_path_files_count = sum([len(files) for r, d, files in os.walk(output_dir_path)])
        if artifact.files_count != output_dir_path_files_count:
            print(f'files_count mismatch: {artifact.files_count} != {output_dir_path_files_count}')
            return False
        return True

    def test_render_html(self):
        a = Airium()

        a('<!DOCTYPE html>')
        with a.html(lang="en"):
            with a.head():
                a.meta(charset="utf-8")
                a.title(_t="Execution info")

            with a.body(style="margin: 0;"):
                a.embed(type="image/svg+xml", src=f'build-linux.svg', style="height: calc(100vh - 5px);")
                a.embed(type="image/svg+xml", src=f'build-windows.svg', style="height: calc(100vh - 5px);")
                a.embed(type="image/svg+xml", src=f'build-linux-single.svg', style="height: calc(100vh - 5px);")
                a.embed(type="image/svg+xml", src=f'build-windows-single.svg', style="height: calc(100vh - 5px);")

        os.makedirs(common_paths.render_path, exist_ok=True)
        io_tools.write_text(os.path.join(common_paths.render_path, 'index.html'), str(a))

    def test_extract(self):
        for artifact in artifacts_data().values():
            for archiver in get_archiver_tools().values():
                print(f"test_extract '{artifact.name}' with '{archiver.name}'")

                if not io_tools.try_create_or_clean_dir(common_paths.extracted_data_path):
                    raise IOError(f'Cannot try_create_or_clean_dir: {common_paths.extracted_data_path}')

                output_dir_path = os.path.join(common_paths.extracted_data_path, f"{artifact.name}_{archiver.name}")
                execution_time = None
                with suppress(NotImplementedError):
                    execution_time = round(0.5 * timeit(lambda: archiver.extract(os.path.join(common_paths.data_path, artifact.name), output_dir_path), number=2), 3)
                if execution_time and not self.check_content(artifact, output_dir_path):
                    execution_time = None
                self.execution_info.append(models.ExecutionInfo(execution_time=execution_time,
                                                         artifact=artifact,
                                                         archiver=archiver.name))
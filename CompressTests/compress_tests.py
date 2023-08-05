import sys
import unittest
import os
from contextlib import suppress
from timeit import timeit
from airium import Airium

from ArchiverCommon import artifact_tools, models, common_paths, io_tools, archiver_tools, execution_renderer
from ArchiverCommon.io_tools import get_name_without_extensions

_self_path: str = os.path.dirname(os.path.realpath(__file__))


def artifacts_data() -> dict[str, models.ArtifactInfo]:
    return {
        '13MB.zip': models.ArtifactInfo(name='13MB.zip', size=13748886, files_count=2056),
        '116MB.zip': models.ArtifactInfo(name='116MB.zip', size=122518995, files_count=2123),
        '1GB.zip': models.ArtifactInfo(name='git-sdk-64-main.zip', size=1407960952, files_count=108168),
    }


def get_archiver_tools() -> dict[str, models.ArchiverInfo]:
    archivers = {
        'bsdtar-3.6.2': models.ArchiverInfo(name='bsdtar-3.6.2', create=archiver_tools.bsdtar_tool.create),
        '7zip-21.07': models.ArchiverInfo(name='7zip-21.07', create=archiver_tools.p7zip_tool.create),
        '7z22.01-zstd': models.ArchiverInfo(name='7z22.01-zstd', create=archiver_tools.p7zip_zstd_tool.create),
    }

    if sys.platform.startswith('win') and '7zip-21.07' in archivers:
        # Not used: same as 7z22.01-zstd
        archivers.pop('7zip-21.07')

    if not sys.platform.startswith('win') and '7z22.01-zstd' in archivers:
        # Not working on linux.
        archivers.pop('7z22.01-zstd')

    return archivers


class CompressTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.execution_info: list[models.ExecutionInfo] = []
        cls.first_sizes: dict[str, int] = {}
        if not os.environ.get('self_toolset_name'):
            os.environ['self_toolset_name'] = 'build-local'

        print(f"self_toolset_name: {os.environ['self_toolset_name']}")

    @classmethod
    def tearDownClass(cls) -> None:
        render_path = common_paths.create_render_path(_self_path)
        execution_renderer.render(cls.execution_info, render_path)

    def test_render_html(self):
        a = Airium()

        a('<!DOCTYPE html>')
        with a.html(lang="en"):
            with a.head():
                a.meta(charset="utf-8")
                a.title(_t="Execution info")

            with a.body(style="margin: 0;"):
                a.embed(type="image/svg+xml", src=f'build-linux-small.svg', style="height: calc(100vh - 5px);")
                a.embed(type="image/svg+xml", src=f'build-windows-small.svg', style="height: calc(100vh - 5px);")
                a.embed(type="image/svg+xml", src=f'build-linux.svg', style="height: calc(100vh - 5px);")
                a.embed(type="image/svg+xml", src=f'build-windows.svg', style="height: calc(100vh - 5px);")

        render_path = common_paths.create_render_path(_self_path)
        io_tools.write_text(os.path.join(render_path, 'index.html'), str(a))

    def check_create(self, archiver: models.ArchiverInfo, artifact_target: models.ArtifactTargetInfo, extension: str):
        artifact_name = f"{artifact_target.name}{extension}"
        print(f"test_create '{artifact_name}' with '{archiver.name}'")
        if not io_tools.try_create_or_clean_dir(common_paths.extracted_data_path):
            raise IOError(f'Cannot try_create_or_clean_dir: {common_paths.extracted_data_path}')

        source_dir_path = os.path.join(common_paths.data_path, f"{get_name_without_extensions(artifact_target.name)}")
        output_file_path = os.path.join(common_paths.extracted_data_path, artifact_name)
        execution_time = None
        with suppress(NotImplementedError):
            execution_time = round(0.5 * timeit(
                lambda: archiver.create(source_dir_path, output_file_path),
                number=2), 3)
        # todo: check_content
        output_file_path = os.path.join(common_paths.extracted_data_path, artifact_name)
        if not os.path.isfile(output_file_path):
            execution_time = None

        if artifact_name not in self.first_sizes:
            self.first_sizes[artifact_name] = os.path.getsize(output_file_path)


        artifact_info = models.ArtifactInfo(name=artifact_name,
                                            size=self.first_sizes[artifact_name],
                                            files_count=artifact_target.files_count)
        self.execution_info.append(models.ExecutionInfo(execution_time=execution_time,
                                                        artifact=artifact_info,
                                                        archiver=archiver.name))

    def test_create_small(self):
        if os.environ['self_toolset_name'] not in ('build-windows-small', 'build-linux-small', 'build-local'):
            return

        zip_artifact = artifacts_data()['13MB.zip']
        extract_info = artifact_tools.extract_artifact(zip_artifact)

        for archiver in get_archiver_tools().values():
            self.check_create(archiver, extract_info, '.tar')
            self.check_create(archiver, extract_info, '.zip')
            self.check_create(archiver, extract_info, '.tar.gz')
            self.check_create(archiver, extract_info, '.tar.zst')
            self.check_create(archiver, extract_info, '.7z')

    def test_create(self):
        if os.environ['self_toolset_name'] not in ('build-windows', 'build-linux', 'build-local'):
            return

        zip_artifact = artifacts_data()['116MB.zip']
        extract_info = artifact_tools.extract_artifact(zip_artifact)

        for archiver in get_archiver_tools().values():
            self.check_create(archiver, extract_info, '.tar')
            self.check_create(archiver, extract_info, '.zip')
            self.check_create(archiver, extract_info, '.tar.gz')
            self.check_create(archiver, extract_info, '.tar.zst')
            self.check_create(archiver, extract_info, '.7z')
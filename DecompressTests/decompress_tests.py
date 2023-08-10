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


from ArchiverCommon import archiver_tools, artifact_tools, io_tools, common_paths, models, execution_renderer, \
    common_consts


def artifacts_data() -> dict[str, models.ArtifactInfo]:
    return {
        '13MB.zip': models.ArtifactInfo(name='13MB.zip', size=13748886, files_count=2056),
        '116MB.zip': models.ArtifactInfo(name='116MB.zip', size=122518995, files_count=2123),
        '1GB.zip': models.ArtifactInfo(name='git-sdk-64-main.zip', size=1407960952, files_count=108168),
    }


def get_archiver_tools() -> dict[str, models.ArchiverInfo]:
    archivers = {
        'bsdtar-3.7.1': models.ArchiverInfo(name='bsdtar-3.7.1',
                                            extract=archiver_tools.bsdtar_tool.get_extract_func(common_consts.latest)),
        '7zip-21.07': models.ArchiverInfo(name='7zip-21.07',
                                          extract=archiver_tools.p7zip_tool.get_extract_func(archiver_tools.p7zip_tool.version_21_07)),
        '7z22.01-zstd': models.ArchiverInfo(name='7z22.01-zstd',
                                            extract=archiver_tools.p7zip_zstd_tool.get_extract_func(archiver_tools.p7zip_tool.version_22_01_zstd)),
        'zstd-1.5.5': models.ArchiverInfo(name='zstd-1.5.5', extract=archiver_tools.zstd_tool.extract),
        'igzip-2.30': models.ArchiverInfo(name='igzip-2.30', extract=archiver_tools.igzip_tool.extract),
        'pigz-2.4': models.ArchiverInfo(name='pigz-2.4', extract=archiver_tools.pigz_tool.extract),
        'rapidgzip-0.7.0': models.ArchiverInfo(name='rapidgzip-0.7.0', extract=archiver_tools.rapidgzip_tool.extract),
        'ripunzip-0.4.0': models.ArchiverInfo(name='ripunzip-0.4.0', extract=archiver_tools.ripunzip_tool.extract),
        'py7zr-0.20.5': models.ArchiverInfo(name='py7zr-0.20.5', extract=archiver_tools.py7zr_tool.extract),
        'python-3.11': models.ArchiverInfo(name='python-3.11',
                                           extract=archiver_tools.python_archiver_tool.get_extract_func(common_consts.latest)),
    }

    if sys.platform.startswith('win') and '7zip-21.07' in archivers:
        # Not used: same as 7z22.01-zstd
        archivers.pop('7zip-21.07')

    if not sys.platform.startswith('win') and '7z22.01-zstd' in archivers:
        # Not working on linux.
        archivers.pop('7z22.01-zstd')

    return archivers


class DecompressTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.execution_info: list[models.ExecutionInfo] = []
        if not os.environ.get('self_toolset_name'):
            os.environ['self_toolset_name'] = 'build-local'

        print(f"self_toolset_name: {os.environ['self_toolset_name']}")

    @classmethod
    def tearDownClass(cls) -> None:
        render_path = common_paths.create_render_path(_self_path)
        execution_renderer.render(cls.execution_info, render_path)

    def check_extract(self, archiver: models.ArchiverInfo, artifact: models.ArtifactInfo):
        print(f"test_extract '{artifact.name}' with '{archiver.name}'")
        if not io_tools.try_create_or_clean_dir(common_paths.extracted_data_path):
            raise IOError(f'Cannot try_create_or_clean_dir: {common_paths.extracted_data_path}')
        output_dir_path = os.path.join(common_paths.extracted_data_path, f"{artifact.name}_{archiver.name}")
        execution_time = None
        with suppress(NotImplementedError):
            execution_time = round(0.5 * timeit(
                lambda: archiver.extract(os.path.join(common_paths.data_path, artifact.name), output_dir_path),
                number=2), 3)
        if execution_time and not artifact_tools.check_content(artifact, output_dir_path):
            execution_time = None
        self.execution_info.append(models.ExecutionInfo(execution_time=execution_time,
                                                        artifact=artifact,
                                                        archiver=archiver.name))

    def check_extract_create_from_zip(self, zip_artifact):
        tar_artifact = artifact_tools.create_tar_artifact(zip_artifact)
        tar_gz_artifact = artifact_tools.create_tar_gz_artifact(tar_artifact)
        tar_zst_artifact = artifact_tools.create_tar_zst_artifact(tar_artifact)
        p7zip_artifact = artifact_tools.create_7z_artifact(zip_artifact)

        for archiver in get_archiver_tools().values():
            self.check_extract(archiver, tar_artifact)
            self.check_extract(archiver, zip_artifact)
            self.check_extract(archiver, tar_gz_artifact)
            self.check_extract(archiver, tar_zst_artifact)
            self.check_extract(archiver, p7zip_artifact)

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

                if os.environ.get('DISABLE_HEAVY_TESTS') != '1':
                    a.embed(type="image/svg+xml", src=f'build-linux-large.svg', style="height: calc(100vh - 5px);")
                    a.embed(type="image/svg+xml", src=f'build-windows-large.svg', style="height: calc(100vh - 5px);")

        render_path = common_paths.create_render_path(_self_path)
        io_tools.write_text(os.path.join(render_path, 'index.html'), str(a))

    def test_extract_small(self):
        if os.environ['self_toolset_name'] not in ('build-windows-small', 'build-linux-small', 'build-local'):
            return

        zip_artifact = artifacts_data()['13MB.zip']
        self.check_extract_create_from_zip(zip_artifact)

    def test_extract(self):
        if os.environ['self_toolset_name'] not in ('build-windows', 'build-linux', 'build-local'):
            return

        zip_artifact = artifacts_data()['116MB.zip']
        self.check_extract_create_from_zip(zip_artifact)

    def test_extract_large(self):
        if os.environ.get('DISABLE_HEAVY_TESTS') == '1':
            print("DISABLE_HEAVY_TESTS")
            return

        if os.environ['self_toolset_name'] not in ('build-windows-large', 'build-linux-large', 'build-local'):
            return

        zip_artifact = artifacts_data()['1GB.zip']
        self.check_extract_create_from_zip(zip_artifact)

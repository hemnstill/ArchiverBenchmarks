import os
import subprocess
import sys

from ArchiverCommon import common_paths, common_consts

version_362 = '3.6.2'
version_371 = '3.7.1'


def get_bsdtar_362_exe_path():
    if sys.platform.startswith('win'):
        return os.path.join(common_paths.tools_path, 'bsdtar-3.6.2.exe')

    return os.path.join(common_paths.tools_path, 'bsdtar-3.6.2')


def get_bsdtar_exe_path(version: str):
    if version == version_362:
        return get_bsdtar_362_exe_path()

    if version == common_consts.latest:
        version = version_371

    if sys.platform.startswith('win'):
        return os.path.join(common_paths.tools_path, f'bsdtar-{version}', 'bsdtar.exe')

    return os.path.join(common_paths.tools_path, f'bsdtar-{version}', 'bsdtar')


def get_version_from_stdout(b_stdout: bytes) -> str:
    for b_line in b_stdout.splitlines():
        if b_line.startswith(b'bsdtar'):
            return b_line.decode().strip()


def get_version(tool_version: str):
    result = subprocess.run([get_bsdtar_exe_path(tool_version), '--version'], check=True, stdout=subprocess.PIPE)
    return get_version_from_stdout(result.stdout)


def extract(file_path: str, output_dir_path: str, version: str):
    os.makedirs(output_dir_path, exist_ok=True)
    subprocess.run([get_bsdtar_exe_path(version), '-xf', file_path, '-C', output_dir_path], check=True)


def create_tar(source_dir_path: str, file_path: str, version: str):
    if not os.path.isdir(source_dir_path):
        raise IOError(f"'{source_dir_path}' should be directory.")

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    subprocess.run([get_bsdtar_exe_path(version), '-cf', file_path, '-C', source_dir_path, '.'], check=True)


def append_tar(source_dir_path: str, file_path: str):
    if not os.path.isdir(source_dir_path):
        raise IOError(f"'{source_dir_path}' should be directory.")

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    subprocess.run([get_bsdtar_exe_path(version_362), '-rf', file_path, '-C', source_dir_path, '.'], check=True)


def create_tar_gz(source_dir_path: str, file_path: str, version: str):
    if not os.path.isdir(source_dir_path):
        raise IOError(f"'{source_dir_path}' should be directory.")

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    subprocess.run([get_bsdtar_exe_path(version), '--options', 'gzip:compression-level=1', '-czf', file_path,  '-C', source_dir_path, '.'], check=True)


def create_tar_zstd(source_dir_path: str, file_path: str, version: str):
    if not os.path.isdir(source_dir_path):
        raise IOError(f"'{source_dir_path}' should be directory.")

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    subprocess.run([get_bsdtar_exe_path(version), '--zstd', '--options', 'zstd:compression-level=1', '-cf', file_path, '-C', source_dir_path, '.'], check=True)


def create_zip(source_dir_path: str, file_path: str, version: str):
    if not os.path.isdir(source_dir_path):
        raise IOError(f"'{source_dir_path}' should be directory.")

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    subprocess.run([get_bsdtar_exe_path(version), '--auto-compress', '--options', 'zip:compression-level=1', '-cf', file_path, '-C', source_dir_path, '.'], check=True)


def create_7zip(source_dir_path: str, file_path: str, version: str):
    if not os.path.isdir(source_dir_path):
        raise IOError(f"'{source_dir_path}' should be directory.")

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    subprocess.run([get_bsdtar_exe_path(version), '--auto-compress', '--options', '7zip:compression-level=1', '-cf', file_path, '-C', source_dir_path, '.'], check=True)


def create(source_dir_path: str, file_path: str, version: str):

    if os.path.exists(file_path):
        os.remove(file_path)

    if file_path.endswith('.tar'):
        create_tar(source_dir_path, file_path, version)
        return

    if file_path.endswith('.zip'):
        create_zip(source_dir_path, file_path, version)
        return

    if file_path.endswith('.tar.gz'):
        create_tar_gz(source_dir_path, file_path, version)
        return

    if file_path.endswith('.tar.zst'):
        create_tar_zstd(source_dir_path, file_path, version)
        return

    if file_path.endswith('.7z'):
        create_7zip(source_dir_path, file_path, version)
        return

    raise NotImplementedError(f"bsdtar create does not support: '{file_path}'")


def extract_file(file_path: str, inside_archive_file_path, output_dir_path: str):
    os.makedirs(output_dir_path, exist_ok=True)
    subprocess.run([get_bsdtar_exe_path(version_362), '-xf', file_path, '-C', output_dir_path, inside_archive_file_path], check=True)


def get_create_func(version: str):
    return lambda source_dir_path, file_path: create(source_dir_path, file_path, version)


def get_extract_func(version: str):
    return lambda file_path, output_dir_path: extract(file_path, output_dir_path, version)
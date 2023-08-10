import os
import subprocess
import sys

from ArchiverCommon import common_paths


def get_bsdtar_exe_path():
    if sys.platform.startswith('win'):
        return os.path.join(common_paths.tools_path, 'bsdtar-3.7.1', 'bsdtar.exe')

    return os.path.join(common_paths.tools_path, 'bsdtar-3.7.1', 'bsdtar')


def extract(file_path: str, output_dir_path: str):
    os.makedirs(output_dir_path, exist_ok=True)
    subprocess.run([get_bsdtar_exe_path(), '-xf', file_path, '-C', output_dir_path], check=True)


def create_tar(source_dir_path: str, file_path: str):
    if not os.path.isdir(source_dir_path):
        raise IOError(f"'{source_dir_path}' should be directory.")

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    subprocess.run([get_bsdtar_exe_path(), '-cf', file_path, '-C', source_dir_path, '.'], check=True)


def append_tar(source_dir_path: str, file_path: str):
    if not os.path.isdir(source_dir_path):
        raise IOError(f"'{source_dir_path}' should be directory.")

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    subprocess.run([get_bsdtar_exe_path(), '-rf', file_path, '-C', source_dir_path, '.'], check=True)


def create_tar_gz(source_dir_path: str, file_path: str):
    if not os.path.isdir(source_dir_path):
        raise IOError(f"'{source_dir_path}' should be directory.")

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    subprocess.run([get_bsdtar_exe_path(), '--options', 'gzip:compression-level=1', '-czf', file_path,  '-C', source_dir_path, '.'], check=True)


def create_tar_zstd(source_dir_path: str, file_path: str):
    if not os.path.isdir(source_dir_path):
        raise IOError(f"'{source_dir_path}' should be directory.")

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    subprocess.run([get_bsdtar_exe_path(), '--zstd', '--options', 'zstd:compression-level=1', '-cf', file_path, '-C', source_dir_path, '.'], check=True)


def create_zip(source_dir_path: str, file_path: str):
    if not os.path.isdir(source_dir_path):
        raise IOError(f"'{source_dir_path}' should be directory.")

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    subprocess.run([get_bsdtar_exe_path(), '--auto-compress', '--options', 'zip:compression-level=1', '-cf', file_path, '-C', source_dir_path, '.'], check=True)


def create_7zip(source_dir_path: str, file_path: str):
    if not os.path.isdir(source_dir_path):
        raise IOError(f"'{source_dir_path}' should be directory.")

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    subprocess.run([get_bsdtar_exe_path(), '--auto-compress', '--options', '7zip:compression-level=1', '-cf', file_path, '-C', source_dir_path, '.'], check=True)


def create(source_dir_path: str, file_path: str):

    if os.path.exists(file_path):
        os.remove(file_path)

    if file_path.endswith('.tar'):
        create_tar(source_dir_path, file_path)
        return

    if file_path.endswith('.zip'):
        create_zip(source_dir_path, file_path)
        return

    if file_path.endswith('.tar.gz'):
        create_tar_gz(source_dir_path, file_path)
        return

    if file_path.endswith('.tar.zst'):
        create_tar_zstd(source_dir_path, file_path)
        return

    if file_path.endswith('.7z'):
        create_7zip(source_dir_path, file_path)
        return

    raise NotImplementedError(f"bsdtar create does not support: '{file_path}'")


def extract_file(file_path: str, inside_archive_file_path, output_dir_path: str):
    os.makedirs(output_dir_path, exist_ok=True)
    subprocess.run([get_bsdtar_exe_path(), '-xf', file_path, '-C', output_dir_path, inside_archive_file_path], check=True)
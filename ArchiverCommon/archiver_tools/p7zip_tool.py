import os
import subprocess
import sys

from ArchiverCommon import common_paths


def get_7zip_exe_path():
    if sys.platform.startswith('win'):
        return os.path.join(common_paths.tools_path, '7z-23.01', '7zz.exe')

    return os.path.join(common_paths.tools_path, '7z-23.01', '7zz')


def extract(file_path: str, output_dir_path: str):
    if file_path.endswith('.zst'):
        raise NotImplementedError(f"7z does not support zstd: '{file_path}'")

    if file_path.endswith(('.7z', '.tar', '.zip')):
        subprocess.run([get_7zip_exe_path(), '-bso0', '-bd', 'x', file_path, f'-o{output_dir_path}', '-aoa'], check=True)
        return

    subprocess.run(f'"{get_7zip_exe_path()}" -bso0 -bd x "{file_path}" -so | "{get_7zip_exe_path()}" -bso0 -bd x -si -ttar "-o{output_dir_path}" -aoa',
                   check=True, shell=True)


def create_7z(source_dir_path: str, file_path: str):
    if not os.path.isdir(source_dir_path):
        raise IOError(f"'{source_dir_path}' should be directory.")

    subprocess.run([get_7zip_exe_path(), '-bso0', '-bd', '-mx=1', 'a', file_path, source_dir_path], check=True)


def create_tar_gz(source_dir_path: str, file_path: str):
    if not os.path.isdir(source_dir_path):
        raise IOError(f"'{source_dir_path}' should be directory.")

    subprocess.run(args=f'"{get_7zip_exe_path()}" -bso0 -bd a -ttar -so -an "{source_dir_path}" | "{get_7zip_exe_path()}" -bso0 -bd a -tgzip -mx=1 -si "{file_path}"',
                   check=True, shell=True)


def create_tar(source_dir_path: str, file_path: str):
    if not os.path.isdir(source_dir_path):
        raise IOError(f"'{source_dir_path}' should be directory.")

    subprocess.run([get_7zip_exe_path(), '-bso0', '-bd', 'a', '-ttar', file_path, source_dir_path], check=True)


def create(source_dir_path: str, file_path: str):

    if os.path.exists(file_path):
        # 'tar | gzip' cannot overwrite archive.
        os.remove(file_path)

    if file_path.endswith('.tar'):
        create_tar(source_dir_path, file_path)
        return

    if file_path.endswith(('.7z', '.zip')):
        create_7z(source_dir_path, file_path)
        return

    if file_path.endswith('.tar.gz'):
        create_tar_gz(source_dir_path, file_path)
        return

    raise NotImplementedError(f"7-zip create does not support: '{file_path}'")
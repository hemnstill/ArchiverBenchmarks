import os
import subprocess

from ArchiverCommon import common_consts
from ArchiverCommon.archiver_tools import p7zip_tool


def extract(file_path: str, output_dir_path: str, version: str) -> None:
    if version == common_consts.latest:
        version = p7zip_tool.version_22_01_zstd

    if file_path.endswith(('.7z', '.tar', '.zip')):
        subprocess.run([p7zip_tool.get_7zip_exe_path(version), '-bso0', '-bd', 'x', file_path, f'-o{output_dir_path}', '-aoa'],
                       check=True)
        return

    subprocess.run(f'"{p7zip_tool.get_7zip_exe_path(version)}" -bso0 -bd x "{file_path}" -so | "{p7zip_tool.get_7zip_exe_path(version)}" -bso0 -bd x -si -ttar "-o{output_dir_path}" -aoa',
        check=True, shell=True)


def create_tar_zstd(source_dir_path: str, file_path: str, version: str):
    if not os.path.isdir(source_dir_path):
        raise IOError(f"'{source_dir_path}' should be directory.")

    subprocess.run(args=f'"{p7zip_tool.get_7zip_exe_path(version)}" -bso0 -bd a -ttar -so -an "{source_dir_path}" | "{p7zip_tool.get_7zip_exe_path(version)}" -bso0 -bd a -tzstd -mx=1 -si "{file_path}"',
                   check=True, shell=True)


def create(source_dir_path: str, file_path: str, version: str):
    if version == common_consts.latest:
        version = p7zip_tool.version_22_01_zstd

    if os.path.exists(file_path):
        # 'tar | gzip' cannot overwrite archive.
        os.remove(file_path)

    if file_path.endswith('.tar'):
        p7zip_tool.create_tar(source_dir_path, file_path, version)
        return

    if file_path.endswith(('.7z', '.zip')):
        p7zip_tool.create_7z(source_dir_path, file_path, version)
        return

    if file_path.endswith('.tar.gz'):
        p7zip_tool.create_tar_gz(source_dir_path, file_path, version)
        return

    if file_path.endswith('.tar.zst'):
        create_tar_zstd(source_dir_path, file_path, version)
        return

    raise NotImplementedError(f"7-zip-zstd create does not support: '{file_path}'")


def get_create_func(version: str):
    return lambda source_dir_path, file_path: create(source_dir_path, file_path, version)


def get_extract_func(version: str):
    return lambda file_path, output_dir_path: extract(file_path, output_dir_path, version)
import os
import subprocess
import sys

from ArchiverCommon import common_paths, common_consts

version_21_07 = '21.07'
version_23_01 = '23.01'
version_22_01_zstd = '22.01-zstd'


def get_7zip_21_07_exe_path():
    if sys.platform.startswith('win'):
        return os.path.join(common_paths.tools_path, '7z-21.07', '7z.exe')

    return os.path.join(common_paths.tools_path, '7z-21.07', '7zzs')


def get_7zip_22_01_zstd_exe_path():
    if sys.platform.startswith('win'):
        return os.path.join(common_paths.tools_path, '7z22.01-zstd', '7z.exe')

    raise NotImplementedError(f"platform not supported: '{sys.platform}'")


def get_7zip_exe_path(version: str):
    if version == version_21_07:
        return get_7zip_21_07_exe_path()

    if version == version_22_01_zstd:
        return get_7zip_22_01_zstd_exe_path()

    if version == common_consts.latest:
        version = version_23_01

    if sys.platform.startswith('win'):
        return os.path.join(common_paths.tools_path, f'7z-{version}', '7zz.exe')

    return os.path.join(common_paths.tools_path, f'7z-{version}', '7zz')


def get_version_from_stdout(b_stdout: bytes) -> str:
    for b_line in b_stdout.splitlines():
        if b_line.startswith(b'7-Zip'):
            return b_line.decode().strip()


def get_version(tool_version: str):
    result = subprocess.run([get_7zip_exe_path(tool_version)], check=True, stdout=subprocess.PIPE)
    return get_version_from_stdout(result.stdout)


def extract(file_path: str, output_dir_path: str, version: str) -> None:
    if file_path.endswith('.zst'):
        raise NotImplementedError(f"7z does not support zstd: '{file_path}'")

    if file_path.endswith(('.7z', '.tar', '.zip')):
        subprocess.run([get_7zip_exe_path(version), '-bso0', '-bd', 'x', file_path, f'-o{output_dir_path}', '-aoa'], check=True)
        return

    subprocess.run(f'"{get_7zip_exe_path(version)}" -bso0 -bd x "{file_path}" -so | "{get_7zip_exe_path(version)}" -bso0 -bd x -si -ttar "-o{output_dir_path}" -aoa',
                   check=True, shell=True)


def create_7z(source_dir_path: str, file_path: str, version: str):
    if not os.path.isdir(source_dir_path):
        raise IOError(f"'{source_dir_path}' should be directory.")

    subprocess.run([get_7zip_exe_path(version), '-bso0', '-bd', '-mx=1', 'a', file_path, source_dir_path], check=True)


def create_tar_gz(source_dir_path: str, file_path: str, version: str):
    if not os.path.isdir(source_dir_path):
        raise IOError(f"'{source_dir_path}' should be directory.")

    subprocess.run(args=f'"{get_7zip_exe_path(version)}" -bso0 -bd a -ttar -so -an "{source_dir_path}" | "{get_7zip_exe_path(version)}" -bso0 -bd a -tgzip -mx=1 -si "{file_path}"',
                   check=True, shell=True)


def create_tar(source_dir_path: str, file_path: str, version: str):
    if not os.path.isdir(source_dir_path):
        raise IOError(f"'{source_dir_path}' should be directory.")

    subprocess.run([get_7zip_exe_path(version), '-bso0', '-bd', 'a', '-ttar', file_path, source_dir_path], check=True)


def create(source_dir_path: str, file_path: str, version: str):
    if os.path.exists(file_path):
        # 'tar | gzip' cannot overwrite archive.
        os.remove(file_path)

    if file_path.endswith('.tar'):
        create_tar(source_dir_path, file_path, version)
        return

    if file_path.endswith(('.7z', '.zip')):
        create_7z(source_dir_path, file_path, version)
        return

    if file_path.endswith('.tar.gz'):
        create_tar_gz(source_dir_path, file_path, version)
        return

    raise NotImplementedError(f"7-zip create does not support: '{file_path}'")


def get_create_func(version: str):
    return lambda source_dir_path, file_path: create(source_dir_path, file_path, version)


def get_extract_func(version: str):
    return lambda file_path, output_dir_path: extract(file_path, output_dir_path, version)

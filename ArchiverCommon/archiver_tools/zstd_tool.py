import os
import subprocess
import sys

from ArchiverCommon import common_paths, common_consts

from .bsdtar_tool import get_bsdtar_exe_path


def get_zstd_exe_path():
    if sys.platform.startswith('win'):
        return os.path.join(common_paths.tools_path,'zstd-1.5.5.exe')

    return 'zstd'


def extract(file_path: str, output_dir_path: str):
    supported_formats = ('.zst', '.tzst', '.gz', '.tgz')
    if not file_path.endswith(supported_formats):
        raise NotImplementedError(f"zstd does not support: '{file_path}'")
    os.makedirs(output_dir_path, exist_ok=True)
    subprocess.run(args=f'"{get_zstd_exe_path()}" --force --keep -d "{file_path}" --stdout | "{get_bsdtar_exe_path(common_consts.latest)}" -xf - -C "{output_dir_path}"',
                   check=True, shell=True)


def create_tar_zst(source_tar_path: str):
    if not os.path.isfile(source_tar_path) or not source_tar_path.endswith('.tar'):
        raise IOError(f"'{source_tar_path}' should be a '.tar' file.")

    subprocess.run(args=f'"{get_zstd_exe_path()}" --force --keep "{source_tar_path}"',
                   check=True, shell=True)
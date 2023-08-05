import os
import subprocess
import sys

from .bsdtar_tool import get_bsdtar_exe_path


def extract(file_path: str, output_dir_path: str):
    supported_formats = ('.gz', '.tgz')
    if not file_path.endswith(supported_formats):
        raise NotImplementedError(f"igzip does not support: '{file_path}'")
    os.makedirs(output_dir_path, exist_ok=True)
    subprocess.run(args=f'"{sys.executable}" -m isal.igzip --force -d "{file_path}" --stdout | "{get_bsdtar_exe_path()}" -xf - -C "{output_dir_path}"',
                   check=True, shell=True)


def create_tar_gz(source_tar_path: str):
    if not os.path.isfile(source_tar_path) or not source_tar_path.endswith('.tar'):
        raise IOError(f"'{source_tar_path}' should be a '.tar' file.")

    subprocess.run(args=f'"{sys.executable}" -m isal.igzip --force "{source_tar_path}"',
                   check=True, shell=True)

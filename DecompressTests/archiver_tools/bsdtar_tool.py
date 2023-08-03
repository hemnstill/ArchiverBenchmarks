import os
import subprocess
import sys

from DecompressTests import common_paths


def get_bsdtar_exe_path():
    if sys.platform.startswith('win'):
        return os.path.join(common_paths.tools_path, 'bsdtar-3.6.2.exe')

    return os.path.join(common_paths.tools_path, 'bsdtar-3.6.2')


def extract(file_path: str, output_dir_path: str):
    os.makedirs(output_dir_path, exist_ok=True)
    subprocess.run([get_bsdtar_exe_path(), '-xf', file_path, '-C', output_dir_path], check=True)


def create(source_dir_path: str, file_path: str):
    if not os.path.isdir(source_dir_path):
        raise IOError(f"'{source_dir_path}' should be directory.")

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    subprocess.run([get_bsdtar_exe_path(), '-cf', file_path, '-C', source_dir_path, '.'], check=True)

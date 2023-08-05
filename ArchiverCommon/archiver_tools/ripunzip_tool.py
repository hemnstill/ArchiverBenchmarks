import os
import subprocess
import sys

from ArchiverCommon import common_paths


def get_ripunzip_exe_path():
    if sys.platform.startswith('win'):
        return os.path.join(common_paths.tools_path, 'ripunzip-0.4.0.exe')

    return os.path.join(common_paths.tools_path, 'ripunzip-0.4.0')


def extract(file_path: str, output_dir_path: str):
    supported_formats = '.zip'
    if not file_path.endswith(supported_formats):
        raise NotImplementedError(f"ripunzip does not support: '{file_path}'")
    os.makedirs(output_dir_path, exist_ok=True)
    subprocess.run(args=f'"{get_ripunzip_exe_path()}" --output-directory "{output_dir_path}" file "{file_path}"',
                   check=True, shell=True)

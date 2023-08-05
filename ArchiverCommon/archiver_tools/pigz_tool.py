import os
import subprocess
import sys

from ArchiverCommon import common_paths
from .bsdtar_tool import get_bsdtar_exe_path


def get_pigz_exe_path():
    if sys.platform.startswith('win'):
        return os.path.join(common_paths.tools_path, 'pigz-2.4.exe')

    return 'pigz'


def extract(file_path: str, output_dir_path: str):
    supported_formats = ('.gz', '.tgz')
    if not file_path.endswith(supported_formats):
        raise NotImplementedError(f"pigz does not support: '{file_path}'")
    os.makedirs(output_dir_path, exist_ok=True)
    subprocess.run(args=f'"{get_pigz_exe_path()}" --force --keep -d "{file_path}" --stdout | "{get_bsdtar_exe_path()}" -xf - -C "{output_dir_path}"',
                   check=True, shell=True)

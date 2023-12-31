import os
import subprocess
import sys

from .bsdtar_tool import get_bsdtar_exe_path
from .. import common_consts


def get_rapidgzip_exe_path():
    if sys.platform.startswith('win'):
        return os.path.join(os.path.dirname(sys.executable), 'Scripts', 'rapidgzip.exe')

    return os.path.join(os.path.dirname(sys.executable), 'rapidgzip')


def extract(file_path: str, output_dir_path: str):
    supported_formats = ('.gz', '.tgz')
    if not file_path.endswith(supported_formats):
        raise NotImplementedError(f"rapidgzip does not support: '{file_path}'")
    os.makedirs(output_dir_path, exist_ok=True)
    subprocess.run(args=f'"{get_rapidgzip_exe_path()}" --force -d "{file_path}" --stdout | "{get_bsdtar_exe_path(common_consts.latest)}" -xf - -C "{output_dir_path}"',
                   check=True, shell=True)

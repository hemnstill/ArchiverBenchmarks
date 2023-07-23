import os
import subprocess
import sys

from DecompressTests import common_paths


def get_pigz_exe_path():
    if sys.platform.startswith('win'):
        return os.path.join(common_paths.tools_path,'pigz-2.4.exe')

    raise NotImplementedError(f"platform not supported: '{sys.platform}'")


def extract(file_path: str, output_dir_path: str):
    supported_formats = ('.gz', '.tgz')
    if not file_path.endswith(supported_formats):
        raise NotImplementedError(f"pigz does not support: '{file_path}'")
    os.makedirs(output_dir_path, exist_ok=True)
    output_file_path = os.path.join(output_dir_path, 'stdout')
    subprocess.run(args=f'"{get_pigz_exe_path()}" --force --keep -d "{file_path}" --stdout > "{output_file_path}"', check=True, shell=True)

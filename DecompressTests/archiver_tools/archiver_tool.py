import os
import subprocess
import sys

from DecompressTests import common_paths


def get_archiver_exe_path():
    if sys.platform.startswith('win'):
        return os.path.join(common_paths.tools_path,'archiver-3.5.1.exe')

    return os.path.join(common_paths.tools_path,'archiver-3.5.1')


def extract(file_path: str, output_dir_path: str):
    unsupported_formats = '.7z'
    if file_path.endswith(unsupported_formats):
        raise NotImplementedError(f"archiver does not support: '{file_path}'")

    subprocess.run(args=f'"{get_archiver_exe_path()}" --overwrite unarchive "{file_path}" "{output_dir_path}"',
                   check=True)

import os
import subprocess
import sys

from DecompressTests import common_paths


def get_zstd_exe_path():
    if sys.platform.startswith('win'):
        return os.path.join(common_paths.tools_path,'zstd-1.5.5.exe')

    raise NotImplementedError(f"platform not supported: '{sys.platform}'")


def extract(file_path: str, output_dir_path: str):
    supported_formats = ('.zst', '.tzst', '.gz', '.tgz')
    if not file_path.endswith(supported_formats):
        raise NotImplementedError(f"zstd does not support: '{file_path}'")
    os.makedirs(output_dir_path, exist_ok=True)
    subprocess.run([get_zstd_exe_path(), '--force', '-d', file_path, f'--output-dir-flat', output_dir_path], check=True)

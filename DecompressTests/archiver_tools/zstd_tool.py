import os
import subprocess
import sys

from DecompressTests import common_paths


def get_zstd_exe_path():
    if sys.platform.startswith('win'):
        return os.path.join(common_paths.tools_path,'zstd-1.5.5.exe')

    raise NotImplementedError(f"platform not supported: '{sys.platform}'")


def extract(file_path: str, output_dir_path: str):
    if file_path.endswith('.7z'):
        raise NotImplementedError(f"zstd does not support 7z: '{file_path}'")
    if file_path.endswith('.zip'):
        raise NotImplementedError(f"zstd does not support zip: '{file_path}'")
    os.makedirs(output_dir_path, exist_ok=True)
    subprocess.run([get_zstd_exe_path(), '--force', '-d', file_path, f'--output-dir-flat', output_dir_path], check=True)

import os
import subprocess
import sys

from DecompressTests import common_paths


def get_7zip_exe_path():
    if sys.platform.startswith('win'):
        return os.path.join(common_paths.tools_path,'7z-21.07', '7z.exe')

    return os.path.join(common_paths.tools_path,'7z-21.07', '7zzs')


def extract(file_path: str, output_dir_path: str):
    subprocess.run([get_7zip_exe_path(), '-bso0', '-bd', 'x', file_path, f'-o{output_dir_path}', '-aoa'], check=True)

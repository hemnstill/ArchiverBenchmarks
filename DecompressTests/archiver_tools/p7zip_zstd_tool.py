import os
import subprocess
import sys

from DecompressTests import common_paths
from .bsdtar_tool import get_bsdtar_exe_path


def get_7zip_exe_path():
    if sys.platform.startswith('win'):
        return os.path.join(common_paths.tools_path,'7z22.01-zstd', '7z.exe')

    raise NotImplementedError(f"platform not supported: '{sys.platform}'")


def extract(file_path: str, output_dir_path: str):
    if file_path.endswith(('.7z', '.tar', '.zip')):
        subprocess.run([get_7zip_exe_path(), '-bso0', '-bd', 'x', file_path, f'-o{output_dir_path}', '-aoa'], check=True)
        return

    os.makedirs(output_dir_path, exist_ok=True)
    subprocess.run(f'"{get_7zip_exe_path()}" -bso0 -bd x "{file_path}" -so | "{get_bsdtar_exe_path()}" -xf - -C "{output_dir_path}"',
                   check=True, shell=True)

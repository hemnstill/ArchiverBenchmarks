import os
import subprocess
import sys

_self_path: str = os.path.dirname(os.path.realpath(__file__))
tools_path = os.path.join(os.path.dirname(_self_path), '.tools')


def get_7zip_exe_path():
    if sys.platform.startswith('win'):
        return os.path.join(tools_path,'7z-21.07', '7z.exe')

    return os.path.join(tools_path,'7z-21.07', '7z')


def extract(file_path: str, output_dir_path: str):
    subprocess.run([get_7zip_exe_path(), '-bso0', '-bd', 'x', file_path, f'-o{output_dir_path}', '-aoa'])

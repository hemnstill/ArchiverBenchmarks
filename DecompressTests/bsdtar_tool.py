import os
import subprocess
import sys

_self_path: str = os.path.dirname(os.path.realpath(__file__))
tools_path = os.path.join(os.path.dirname(_self_path), '.tools')


def get_bsdtar_exe_path():
    if sys.platform.startswith('win'):
        return os.path.join(tools_path, 'bsdtar-3.6.2.exe')

    return os.path.join(tools_path, 'bsdtar-3.6.2')


def extract(file_path: str, output_dir_path: str):
    subprocess.run([get_bsdtar_exe_path(), '-xf', file_path, '-C', output_dir_path])
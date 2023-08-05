""" Not used: too slow. """

import os
import subprocess
import sys

from ArchiverCommon import common_paths


def get_unar_exe_path():
    if sys.platform.startswith('win'):
        return os.path.join(common_paths.tools_path, 'unar-1.8.1', 'unar.exe')

    return 'unar'


def extract(file_path: str, output_dir_path: str):
    unsupported_formats = ('.7z', '.zst')
    if file_path.endswith(unsupported_formats):
        raise NotImplementedError(f"unar does not support: '{file_path}'")

    subprocess.run([get_unar_exe_path(), '-quiet', '-output-directory', output_dir_path, '-force-overwrite', file_path],
                   check=True)

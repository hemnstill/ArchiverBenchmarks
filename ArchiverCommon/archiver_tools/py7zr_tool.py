import subprocess
import sys

def extract(file_path: str, output_dir_path: str):
    supported_formats = '.7z'
    if not file_path.endswith(supported_formats):
        raise NotImplementedError(f"py7zr does not support: '{file_path}'")

    subprocess.run([sys.executable, '-m', 'py7zr', 'x', file_path, output_dir_path], check=True)
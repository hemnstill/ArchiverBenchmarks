import os
import shutil
import rapidgzip
import tarfile


def extract(file_path: str, output_dir_path: str):
    supported_formats = ('.gz', '.tgz')
    if not file_path.endswith(supported_formats):
        raise NotImplementedError(f"rapidgzip does not support: '{file_path}'")
    os.makedirs(output_dir_path, exist_ok=True)
    with rapidgzip.open(file_path) as rapidgzip_file:
        with tarfile.TarFile(fileobj=rapidgzip_file) as output_file:
            output_file.extractall(output_dir_path)

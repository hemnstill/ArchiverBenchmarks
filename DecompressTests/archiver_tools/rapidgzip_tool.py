import os
import shutil
import rapidgzip


def extract(file_path: str, output_dir_path: str):
    supported_formats = ('.gz', '.tgz')
    if not file_path.endswith(supported_formats):
        raise NotImplementedError(f"rapidgzip does not support: '{file_path}'")
    os.makedirs(output_dir_path, exist_ok=True)
    output_file_path = os.path.join(output_dir_path, 'stdout')
    with rapidgzip.open(file_path) as rapidgzip_file:
        with open(output_file_path, 'wb') as output_file:
            shutil.copyfileobj(rapidgzip_file, output_file)

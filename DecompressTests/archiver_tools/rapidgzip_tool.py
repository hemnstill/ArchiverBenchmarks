import os
import shutil
import rapidgzip


def extract(file_path: str, output_dir_path: str):
    if file_path.endswith('.7z'):
        raise NotImplementedError(f"rapidgzip does not support .7z: '{file_path}'")
    if file_path.endswith('.zst'):
        raise NotImplementedError(f"rapidgzip does not support .zst: '{file_path}'")
    if file_path.endswith('.zip'):
        raise NotImplementedError(f"rapidgzip does not support .zip: '{file_path}'")
    os.makedirs(output_dir_path, exist_ok=True)
    output_file_path = os.path.join(output_dir_path, 'stdout')
    with rapidgzip.open(file_path) as rapidgzip_file:
        with open(output_file_path, 'wb') as output_file:
            shutil.copyfileobj(rapidgzip_file, output_file)

import os
import zstandard
import tarfile


def extract(file_path: str, output_dir_path: str):
    supported_formats = ('.zst', '.tzst')
    if not file_path.endswith(supported_formats):
        raise NotImplementedError(f"python-zstandard does not support: '{file_path}'")
    os.makedirs(output_dir_path, exist_ok=True)
    with open(file_path, "rb") as f:
        with zstandard.ZstdDecompressor().stream_reader(f) as zstd_file:
            with tarfile.TarFile(fileobj=zstd_file) as output_file:
                output_file.extractall(output_dir_path)

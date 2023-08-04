from py7zr import py7zr


def extract(file_path: str, output_dir_path: str):
    supported_formats = ('.7z')
    if not file_path.endswith(supported_formats):
        raise NotImplementedError(f"py7zr does not support: '{file_path}'")
    #os.makedirs(output_dir_path, exist_ok=True)
    with py7zr.SevenZipFile(file_path, mode='r') as z:
        z.extractall(output_dir_path)
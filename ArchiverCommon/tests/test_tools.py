import os
import sys


_self_path: str = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.dirname(os.path.dirname(_self_path))
if root_path not in sys.path:
    sys.path.append(root_path)


from ArchiverCommon import common_paths, io_tools

utf_8_filename = 'พลัง'


def create_dir_with_utf8_filename(dir_name: str):
    test_archive_dirpath = common_paths.create_temp_path(dir_name)
    utf8_file_path = os.path.join(test_archive_dirpath, utf_8_filename)
    io_tools.write_text(utf8_file_path, 'test content')
    return test_archive_dirpath
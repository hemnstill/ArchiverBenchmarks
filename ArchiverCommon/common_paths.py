import os
import pathlib
import sys

_self_path: str = os.path.dirname(os.path.realpath(__file__))
tools_path = os.path.join(os.path.dirname(_self_path), '.tools')
data_path: str = os.path.join(tools_path, 'data')
extracted_data_path: str = os.path.join(tools_path, 'extracted_data')
if os.environ.get('RUNNER_TOOL_CACHE') and sys.platform.startswith('win'):
    # C drive has more free space in GitHub actions on Windows.
    data_path: str = os.path.join(os.environ['RUNNER_TOOL_CACHE'], 'DecompressTests', 'data')
    extracted_data_path: str = os.path.join(os.environ['RUNNER_TOOL_CACHE'], 'DecompressTests', 'extracted_data')

temp_path = os.path.join(_self_path, 'tmp')


def create_temp_path(name: str):
    _temp_path = os.path.join(temp_path, name)
    pathlib.Path(_temp_path).mkdir(parents=True, exist_ok=True)
    return _temp_path


def create_render_path(workflow_dir_path: str):
    render_path = os.path.join(workflow_dir_path, 'release', 'build')
    os.makedirs(render_path, exist_ok=True)
    return render_path

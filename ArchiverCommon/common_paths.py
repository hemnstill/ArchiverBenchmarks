import os
import sys

_self_path: str = os.path.dirname(os.path.realpath(__file__))
tools_path = os.path.join(os.path.dirname(_self_path), '.tools')
data_path: str = os.path.join(tools_path, 'data')
extracted_data_path: str = os.path.join(tools_path, 'extracted_data')
if os.environ.get('RUNNER_TOOL_CACHE') and sys.platform.startswith('win'):
    # C drive has more free space in GitHub actions on Windows.
    data_path: str = os.path.join(os.environ['RUNNER_TOOL_CACHE'], 'DecompressTests', 'data')
    extracted_data_path: str = os.path.join(os.environ['RUNNER_TOOL_CACHE'], 'DecompressTests', 'extracted_data')

render_path = os.path.join(tools_path, 'release', 'build')
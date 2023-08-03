import os
import sys

_self_path: str = os.path.dirname(os.path.realpath(__file__))
data_path: str = os.path.join(_self_path, 'data')
extracted_data_path: str = os.path.join(_self_path, 'extracted_data')
if os.environ.get('RUNNER_TOOL_CACHE') and sys.platform.startswith('win'):
    # C drive has more free space in GitHub actions on Windows.
    extracted_data_path: str = os.path.join(os.environ['RUNNER_TOOL_CACHE'], 'extracted_data')
tools_path = os.path.join(os.path.dirname(_self_path), '.tools')
render_path = os.path.join(_self_path, 'release', 'build')
import os

_self_path: str = os.path.dirname(os.path.realpath(__file__))
data_path: str = os.path.join(_self_path, 'data')
extracted_data_path: str = os.path.join(_self_path, 'extracted_data')
tools_path = os.path.join(os.path.dirname(_self_path), '.tools')
render_path = os.path.join(_self_path, '_rendered')
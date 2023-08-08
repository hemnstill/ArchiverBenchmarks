import os
import sys

_self_path: str = os.path.dirname(os.path.realpath(__file__))

root_path = os.path.dirname(os.path.dirname(_self_path))

if root_path not in sys.path:
    sys.path.append(root_path)
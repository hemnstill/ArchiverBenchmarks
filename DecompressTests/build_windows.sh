#!/bin/bash
dp0="$(realpath "$(dirname "$0")")"
set -e

self_toolset_name="build-windows"

release_version_dirpath="$dp0/_rendered"
mkdir -p "$release_version_dirpath"

python3 -m pip install pygal aurium
python3 -m unittest decompress_tests.py

cd "$release_version_dirpath"

tar -czvf "../$self_toolset_name.tar.gz" .

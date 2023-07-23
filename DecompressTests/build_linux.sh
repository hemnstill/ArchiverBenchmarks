#!/bin/bash
dp0="$(realpath "$(dirname "$0")")"
set -e

self_toolset_name="build-linux"

release_version_dirpath="$dp0/release/build"
mkdir -p "$release_version_dirpath"

python3 -m pip install pygal==3.0.0 airium==0.2.5 rapidgzip==0.7.0
python3 -m unittest "$dp0/decompress_tests.py"

cd "$release_version_dirpath"

tar -czvf "../$self_toolset_name.tar.gz" .

#!/bin/bash
dp0="$(realpath "$(dirname "$0")")"
set -e

self_name="python-3.11.3"
export self_toolset_name="build-linux-large"

release_version_dirpath="$dp0/release/build"
mkdir -p "$release_version_dirpath"

echo "download python install script ..."
python_bin_download_url="https://github.com/hemnstill/StandaloneTools/releases/download/$self_name/build-gnu.tar.gz"
python_download_zip="$dp0/release/$self_name.tar.gz"
[[ ! -f "$python_download_zip" ]] && wget "$python_bin_download_url" -O "$python_download_zip"

cpython_bin="$dp0/Scripts/bin/python3"
[[ ! -f "$cpython_bin" ]] && tar -xf "$python_download_zip" -C "$dp0"

"$cpython_bin" -m pip install pygal==3.0.0 airium==0.2.5 rapidgzip==0.7.0 isal==1.2.0 py7zr==0.20.5
"$cpython_bin" -m unittest "$dp0/decompress_tests.py"

cd "$release_version_dirpath"

tar -czvf "../$self_toolset_name.tar.gz" .

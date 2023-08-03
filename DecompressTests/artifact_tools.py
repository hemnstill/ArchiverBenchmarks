import os
import pathlib

from DecompressTests import wget_tool, io_tools, common_paths, models
from DecompressTests import archiver_tools


def download_artifact(artifact: models.ArtifactInfo) -> str:
    artifact_file_path = os.path.join(common_paths.data_path, artifact.name)
    artifact_url = f'https://github.com/hemnstill/ArchiverBenchmarks/releases/download/init/{artifact.name}'
    if not os.path.isfile(artifact_file_path) or os.path.getsize(artifact_file_path) != artifact.size:
        wget_tool.download_url(artifact_url, artifact_file_path)
    if os.path.getsize(artifact_file_path) != artifact.size:
        raise IOError(f"Download failed: '{artifact_url}'\n'{artifact.name}' file size {os.path.getsize(artifact_file_path)}, but should be {artifact.size}")

    return artifact_file_path


def create_artifact(zip_artifact: models.ArtifactInfo) -> models.ArtifactInfo:
    if not zip_artifact.name.endswith('.zip'):
        raise ValueError(f"Artifact should be '.zip', got: '{zip_artifact.name}'")

    tar_file_name = f'{pathlib.Path(zip_artifact.name).stem}.tar'
    tar_file_path = os.path.join(common_paths.data_path, tar_file_name)
    print(f'creating {tar_file_path}')
    if os.path.isfile(tar_file_path):
        print(f"'{tar_file_path}' already exists. ")
        return models.ArtifactInfo(tar_file_name, os.path.getsize(tar_file_path), zip_artifact.files_count)

    output_dir_path = os.path.join(common_paths.extracted_data_path, f"_{zip_artifact.name}")
    if not io_tools.try_create_or_clean_dir(output_dir_path):
        raise IOError(f'Cannot try_create_or_clean_dir: {output_dir_path}')

    zip_file_path = download_artifact(zip_artifact)
    archiver_tools.bsdtar_tool.extract(zip_file_path, output_dir_path)
    archiver_tools.bsdtar_tool.create(output_dir_path, tar_file_path)
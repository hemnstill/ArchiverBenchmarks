import os
import subprocess


def download_url(url: str, output_file_path: str) -> None:
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    print(f"download_url '{url}' ...")
    subprocess.run(['curl', '--no-progress-meter', '--location', url, '--output', output_file_path], check=True)
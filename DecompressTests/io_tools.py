import os
import pathlib
import shutil
import time
import zipfile
import importlib
from types import ModuleType

from typing import Type, Callable, Union
from os import path as os_path


def _create_or_clean_dir(dir_path: str) -> bool:
    _dir_path = pathlib.Path(dir_path)
    if _dir_path.is_file():
        _dir_path.unlink()

    if not _dir_path.exists():
        _dir_path.mkdir(parents=True, exist_ok=True)
        return True

    return _clean_dir(dir_path)


def _clean_dir(dir_path: str) -> bool:
    _dir_path = pathlib.Path(dir_path)
    for path in _dir_path.iterdir():
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)
    return not any(_dir_path.iterdir())


def wait_for(action: Callable[[], bool], err_message: Union[str, Callable[..., str]], timeout: float, retry_timeout: float, exception: Type[Exception]) -> bool:
    start = time.monotonic()
    last_exception_message: str = ''
    while True:
        try:
            result = action()
            if result:
                return result
        except exception as e:
            last_exception_message = f'{e}'
        finally:
            elapsed_time = time.monotonic() - start
            if elapsed_time > timeout:
                if callable(err_message):
                    err_message = err_message()
                print(f"{err_message}, timeout: {elapsed_time:.2f}s\n{last_exception_message}")
                return False  # pylint: disable=W0150 # NOSONAR

        time.sleep(retry_timeout)


def _get_clean_dir_error_message(dir_path: str) -> str:
    dir_path_is_empty = not any(pathlib.Path(dir_path).iterdir())
    if dir_path_is_empty:
        return f"Directory '{dir_path}' was cleaned, but timeout expired"

    return f"Cannot clean directory: '{dir_path}'"


def try_create_or_clean_dir(dir_path: str, timeout_in_seconds: float = 5, retry_timeout_in_seconds: float = 0.25) -> bool:
    wait_for(lambda: _create_or_clean_dir(dir_path),
             err_message=lambda: _get_clean_dir_error_message(dir_path),
             timeout=timeout_in_seconds,
             retry_timeout=retry_timeout_in_seconds,
             exception=OSError)
    dir_path_is_empty = not any(pathlib.Path(dir_path).iterdir())
    return dir_path_is_empty


def try_remove_dir(dir_path: str, retry_count: int = 1) -> bool:
    if not os_path.exists(dir_path):
        return True

    retries = range(retry_count)
    for _ in retries:
        try:
            if _clean_dir(dir_path):
                shutil.rmtree(dir_path)
                return True
        except OSError:
            pass
    return False


def extract_archive(archive_file_name: str, target_path: str) -> None:
    with zipfile.ZipFile(archive_file_name, 'r') as zip_file:
        zip_file.extractall(target_path)


def read_text(file_path: Union[str, pathlib.Path], encoding: str = 'utf-8') -> str:
    return pathlib.Path(file_path).read_text(encoding=encoding)


def write_text(file_path: Union[str, pathlib.Path], data: str, encoding: str = 'utf-8') -> int:
    return pathlib.Path(file_path).write_text(data=data, encoding=encoding)


def import_package_modules(package_file_path: str, package_name: str) -> list[ModuleType]:
    extension = '.py'
    imported_modules = []
    for p in sorted(pathlib.Path(os.path.dirname(package_file_path)).iterdir()):
        if p.name.endswith(extension) and p.is_file():
            module = p.name[:-len(extension)]
            if module != '__init__':
                imported_modules.append(importlib.import_module(f".{module}", package_name))
    return imported_modules
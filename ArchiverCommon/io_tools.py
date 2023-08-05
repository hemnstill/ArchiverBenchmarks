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


def byte_to_humanreadable_format(num: Union[int, float], metric: bool = False, precision: int = 1) -> str:
    """
    Human-readable formatting of bytes, using binary (powers of 1024)
    or metric (powers of 1000) representation.
    """
    metric_labels: list[str] = ["B", "kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    binary_labels: list[str] = ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"]
    precision_offsets: list[float] = [0.5, 0.05, 0.005, 0.0005]  # PREDEFINED FOR SPEED.
    precision_formats: list[str] = ["{}{:.0f} {}", "{}{:.1f} {}", "{}{:.2f} {}", "{}{:.3f} {}"]  # PREDEFINED FOR SPEED.

    assert isinstance(num, (int, float)), "num must be an int or float"
    assert isinstance(metric, bool), "metric must be a bool"
    assert isinstance(precision, int) and 0 <= precision <= 3, "precision must be an int (range 0-3)"

    unit_labels = metric_labels if metric else binary_labels
    last_label = unit_labels[-1]
    unit_step = 1000 if metric else 1024
    unit_step_thresh = unit_step - precision_offsets[precision]

    is_negative = num < 0
    if is_negative:  # Faster than ternary assignment or always running abs().
        num = abs(num)

    for unit in unit_labels:
        if num < unit_step_thresh:
            # VERY IMPORTANT:
            # Only accepts the CURRENT unit if we're BELOW the threshold where
            # float rounding behavior would place us into the NEXT unit: F.ex.
            # when rounding a float to 1 decimal, any number ">= 1023.95" will
            # be rounded to "1024.0". Obviously we don't want ugly output such
            # as "1024.0 KiB", since the proper term for that is "1.0 MiB".
            break
        if unit != last_label:
            # We only shrink the number if we HAVEN'T reached the last unit.
            # NOTE: These looped divisions accumulate floating point rounding
            # errors, but each new division pushes the rounding errors further
            # and further down in the decimals, so it doesn't matter at all.
            num /= unit_step

    return precision_formats[precision].format("-" if is_negative else "", num, unit)


def get_name_without_extensions(file_path: str) -> str:
    return pathlib.Path(pathlib.Path(file_path).stem).stem

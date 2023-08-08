from __future__ import annotations

import os
import tarfile
import zipfile
import pathlib
from contextlib import ContextDecorator
from typing import Optional, Tuple, Any, List, Type, Literal
from abc import abstractmethod


PathModeType = Literal['r', 'w', 'x', 'a']


def get_package_class_for_file(file_name: str) -> Optional[Type[PackageFile]]:

    package_classes: List[Type[PackageFile]] = [
        TarPackageFile,
        ZipPackageFile
    ]
    for package_class in package_classes:
        if package_class.can_open(file_name):
            return package_class
    return None


class PackageFile:
    def __init__(self, file_path: str, mode: PathModeType = 'r'):
        self.file_path = file_path
        self.mode = mode

    def __enter__(self) -> PackageFile:
        self.open(self.mode)
        return self

    def __exit__(self, *exc: Tuple[Any, ...]) -> None:
        self.close()

    @abstractmethod
    def add(self, source_path: str, relative_path: str) -> None:
        ...

    @abstractmethod
    def open(self, mode: PathModeType = 'r') -> None:
        ...

    @abstractmethod
    def close(self) -> None:
        ...

    @abstractmethod
    def extract_all(self, path_to_extract: str) -> None:
        ...

    @abstractmethod
    def read(self, file_name: str) -> bytes:
        ...


    @staticmethod
    @abstractmethod
    def can_open(file_name: str) -> bool:
        ...


class ZipPackageFile(PackageFile, ContextDecorator):
    def __init__(self, file_path: str, mode: PathModeType = 'r'):
        super().__init__(file_path, mode)
        self.zip_file: Optional[zipfile.ZipFile] = None

    def __enter__(self) -> ZipPackageFile:
        super().__enter__()
        return self

    def open(self, mode: PathModeType = 'r') -> None:
        self.zip_file = zipfile.ZipFile(self.file_path, mode=mode, compression=zipfile.ZIP_DEFLATED, compresslevel=1)

    def close(self) -> None:
        if self.zip_file:
            self.zip_file.close()
            self.zip_file = None

    def add(self, source_path: str, relative_path: str) -> None:
        if self.zip_file:
            if pathlib.Path(source_path).is_dir():
                for root_dir, _, files in os.walk(source_path):
                    for file in files:
                        file_path = os.path.join(root_dir, file)
                        relative_file_path = os.path.join(relative_path,
                                                          pathlib.Path(file_path).relative_to(source_path))
                        self.zip_file.write(file_path, relative_file_path)
            else:
                self.zip_file.write(source_path, relative_path)
        else:
            raise RuntimeError('The archive must be open before writing.')

    def extract_all(self, path_to_extract: str) -> None:
        self.zip_file.extractall(path_to_extract)

    def read(self, file_name: str) -> bytes:
        if not self.zip_file:
            raise RuntimeError('The archive must be open before reading.')
        return self.zip_file.read(file_name)

    @staticmethod
    def can_open(file_name: str) -> bool:
        return zipfile.is_zipfile(file_name)


class TarPackageFile(PackageFile):
    def __init__(self, file_path: str, mode: PathModeType = 'r', encoding: str = 'utf-8'):
        super().__init__(file_path, mode)
        self.tar_file: Optional[tarfile.TarFile] = None
        self.encoding = encoding

    def __enter__(self) -> PackageFile:
        super().__enter__()
        return self

    def close(self) -> None:
        if self.tar_file:
            self.tar_file.close()
            self.tar_file = None

    def open(self, mode: str = 'r', compresslevel: int | None = None, pax_headers = None) -> None:
        if compresslevel:
            self.tar_file = tarfile.TarFile.gzopen(self.file_path, mode=mode, compresslevel=compresslevel)
            return
        self.tar_file = tarfile.open(self.file_path, mode,
                                     encoding=self.encoding,
                                     pax_headers=pax_headers)

    def add(self, source_path: str, relative_path: str) -> None:
        if self.tar_file:
            self.tar_file.add(source_path, relative_path)
        else:
            raise RuntimeError('The archive must be open before adding.')

    def extract_all(self, path_to_extract: str) -> None:
        if self.tar_file:
            self.tar_file.extractall(path_to_extract)
        else:
            raise RuntimeError('The archive must be open before extracting.')

    def read(self, file_name: str) -> bytes:
        if not self.tar_file:
            raise RuntimeError('The archive must be open before reading.')
        file = self.tar_file.extractfile(file_name)
        if not file:
            raise RuntimeError(f'The file "{file_name}" is not found in "{self.file_path}".')
        return file.read()

    @staticmethod
    def can_open(file_name: str) -> bool:
        return tarfile.is_tarfile(file_name)


def is_package_file_extension(file_name: str) -> bool:
    return file_name.endswith(".zip") or file_name.endswith(".tar.gz")


def extract(file_path: str, output_dir_path: str):
    package_class = get_package_class_for_file(file_path)
    if not package_class:
        raise NotImplementedError(f"python does not support: '{file_path}'")

    package = package_class(file_path)
    package.open()
    package.extract_all(output_dir_path)


def create(source_dir_path: str, file_path: str):
    if file_path.endswith('.zip'):
        package = ZipPackageFile(file_path)
        package.open('w')
        package.add(source_dir_path, '.')
        package.close()
        return

    if file_path.endswith('.tar'):
        package = TarPackageFile(file_path)
        package.open('w')
        package.add(source_dir_path, '.')
        package.close()
        return

    if file_path.endswith('.tar.gz'):
        package = TarPackageFile(file_path)
        package.open('w', compresslevel=1)
        package.add(source_dir_path, '.')
        package.close()
        return

    raise NotImplementedError(f"python archiver create does not support: '{file_path}'")


def create_tar_with_pax_headers(source_dir_path: str, file_path: str):
    pax_headers = {'test_header': 'test_header_value'}
    if file_path.endswith('.tar'):
        package = TarPackageFile(file_path)
        package.open('w', pax_headers=pax_headers)
        package.add(source_dir_path, '.')
        package.close()
        return
    

def get_pax_headers(file_path: str) -> dict[str, str]:
    if file_path.endswith('.tar'):
        package = TarPackageFile(file_path)
        package.open()
        pax_headers = package.tar_file.pax_headers
        package.close()
        return pax_headers


from __future__ import annotations
from typing import Any

import os
from os.path import join, exists
import hashlib
from pathlib import Path
import json

from paramiko import SSHClient
from scp import SCPClient

from .exceptions import PathFormatError


def check_file_path(path: Any) -> Path:
    if not isinstance(path, Path):
        path = Path(path)
    if not exists(path):
        raise FileNotFoundError(f"{path} does not exists.")
    return path


class File:
    def __init__(self, path: Path | str):
        self.path = check_file_path(path)
        self.name = self.path.name
        self.format = self.path.suffix
        self.checksum = None
        self.hash_function = "md5"
        self.size = os.path.getsize(self.path)

    @classmethod
    def load_from_json(cls, path: Path):
        path = check_file_path(path)

        with open(path, "r") as handle:
            data = json.load(handle)

        instance = cls.__new__(cls)
        instance.path = Path(data['path'])
        instance.name = data['name']
        instance.format = data['format']
        instance.checksum = data['checksum']
        instance.hash_function = data['hash_function']
        instance.size = data['size']

        return instance

    def __eq__(self, file: File) -> bool:
        return self.checksum == file.checksum

    def calculate_file_checksum(self, chunk_size: int = 8192) -> str:
        """Calculate the hash of a file using the specified hash function."""
        hash_func = hashlib.new(self.hash_function)

        with open(self.path, "rb") as file:
            while chunk := file.read(chunk_size):
                hash_func.update(chunk)

        checksum = hash_func.hexdigest()
        self.checksum = checksum
        return checksum

    def compare_to_checksum(self, checksum: str) -> bool:
        return self.checksum == checksum

    def compare_to_checksum_file(self, metadata: Path) -> bool:
        check_file_path(metadata)
        with open(metadata, "r") as handle:
            checksum = json.load(handle)["checksum"]
        return self.checksum == checksum

    @property
    def metadata(self) -> dict:
        return self.__dict__

    def save_metadata(self) -> None:
        path = join(self.path.parent, f"{self.path.stem}.json")
        data = self.__dict__

        data["path"] = str(data["path"])
        with open(path, "w") as handle:
            json.dump(self.__dict__, handle)

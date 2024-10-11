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
    def __init__(self, path: Path):
        self.path = check_file_path(path)
        self.name = self.path.name
        self.format = self.path.suffix
        self.hash_val = None
        self.hash_file = None
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
        instance.hash_val = data.get('hash_val')
        instance.hash_file = Path(data.get('hash_file'))
        instance.hash_function = data.get('hash_function', 'md5')
        instance.size = data['size']

        return instance

    def __eq__(self, file: File) -> bool:
        return self.hash_val == file.hash_val

    def calculate_file_hash(self, chunk_size: int = 8192) -> str:
        """Calculate the hash of a file using the specified hash function."""
        hash_func = hashlib.new(self.hash_function)

        with open(self.path, "rb") as file:
            while chunk := file.read(chunk_size):
                hash_func.update(chunk)

        hash_val = hash_func.hexdigest()
        self.hash_val = hash_val
        return hash_val

    def save_hash_file(self) -> None:
        path = Path(join(self.path.parent, f"{self.path.stem}.hash"))

        with open(path, "w") as file:
            file.write(self.hash_val)

        self.hash_file = path

    def compare_to_hash(self, hash_val: str) -> bool:
        return self.hash_val == hash_val

    def compare_to_hash_file(self, hash_file: Path) -> bool:
        check_file_path(hash_file)
        with open(hash_file, "r") as handle:
            hash_val = handle.read()
        return self.hash_val == hash_val

    @property
    def metadata(self) -> dict:
        return self.__dict__

    def save_metadata(self) -> None:
        path = join(self.path.parent, f"{self.path.stem}.json")
        data = self.__dict__

        data["path"] = str(data["path"])
        data["hash_file"] = str(data["hash_file"])

        with open(path, "w") as handle:
            json.dump(self.__dict__, handle)

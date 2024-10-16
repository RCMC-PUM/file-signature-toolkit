from __future__ import annotations

import hashlib
import json
import os
from os.path import exists, join
from pathlib import Path
from typing import Any


def check_file_path(path: Any) -> Path:
    if not isinstance(path, Path):
        path = Path(path)
    if not exists(path):
        raise FileNotFoundError(f"{path} does not exists.")
    return path


class File:
    def __init__(self, path: Path | str, hash_function: str):
        self.path = check_file_path(path)
        self.name = self.path.name
        self.format = self.path.suffix
        self.checksum = None
        self.hash_function = hash_function
        self.size = os.path.getsize(self.path)

    @classmethod
    def load_from_json(cls, path: Path | str) -> File:
        path = check_file_path(path)

        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)

        instance = cls.__new__(cls)
        instance.path = ""
        instance.name = data["name"]
        instance.format = data["format"]
        instance.checksum = data["checksum"]
        instance.hash_function = data["hash_function"]
        instance.size = data["size"]

        return instance

    def __eq__(self, file: File) -> bool:
        return self.checksum == file.checksum

    def calculate_file_checksum(self, batch_size: int) -> str:
        """Calculate the hash of a file using the specified hash function."""
        hash_func = hashlib.new(self.hash_function)

        with open(self.path, "rb", encoding=None) as file:
            while chunk := file.read(batch_size):
                hash_func.update(chunk)

        checksum = hash_func.hexdigest()
        self.checksum = checksum
        return checksum

    def compare_to_checksum(self, checksum: str) -> bool:
        return self.checksum == checksum

    def compare_to_checksum_file(self, signature: Path) -> bool:
        check_file_path(signature)
        with open(signature, "r", encoding="utf-8") as handle:
            checksum = json.load(handle)["checksum"]
        return self.checksum == checksum

    @property
    def signature(self) -> dict:
        return self.__dict__

    def save_signature(self) -> None:
        path = join(self.path.parent, f"{self.path.name}.sign")
        data = {key: val for key, val in self.__dict__.items() if not key == "path"}

        with open(path, "w", encoding="utf-8") as handle:
            json.dump(data, handle)

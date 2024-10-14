import json
from os.path import join
from pathlib import Path

import pytest

from src.file import File

# Constants
TEST_DIR = Path("tests")
TEST_FILE_1 = Path("tests/file_1.txt")
TEST_FILE_2 = Path("tests/file_2.txt")
BATCH_SIZE = 4096
HASH_FUNCTION = "md5"


@pytest.fixture
def file_one():
    """Fixture to initialize File object for file_one.txt"""
    return File(TEST_FILE_1, HASH_FUNCTION)


@pytest.fixture
def file_two():
    """Fixture to initialize File object for file_two.txt"""
    return File(TEST_FILE_2, HASH_FUNCTION)


def test_calculate_file_checksum(file_one):
    """Test calculating the checksum of file_one.txt"""
    checksum = file_one.calculate_file_checksum(BATCH_SIZE)
    assert isinstance(checksum, str)
    assert len(checksum) > 0  # Ensure checksum is not empty


def test_save_and_load_signature(file_one):
    """Test saving a signature and loading it from the JSON file"""
    # Save the signature
    signature_path = Path(join(TEST_DIR, f"{file_one.name}.sign"))
    file_one.calculate_file_checksum(BATCH_SIZE)
    file_one.save_signature()

    # Load the signature and verify
    loaded_file = File.load_from_json(signature_path)
    assert loaded_file.name == file_one.name
    assert loaded_file.format == file_one.format
    assert loaded_file.size == file_one.size
    assert loaded_file.checksum == file_one.checksum


def test_compare_two_files(file_one, file_two):
    """Test comparing two files"""
    file_one_checksum = file_one.calculate_file_checksum(BATCH_SIZE)
    file_two_checksum = file_two.calculate_file_checksum(BATCH_SIZE)

    assert (
        file_one_checksum != file_two_checksum
    )  # File one and file two should have different checksums


def test_signature_validation(file_one):
    """Test validating a file against its signature"""
    # Save the signature
    signature_path = Path(join(TEST_DIR, f"{file_one.name}.sign"))
    file_one.calculate_file_checksum(BATCH_SIZE)
    file_one.save_signature()

    # Manually load the saved signature and validate
    with open(signature_path, "r", encoding="utf-8") as signature_file:
        metadata = json.load(signature_file)

    checksum_in_sign_file = metadata["checksum"]
    # Validate that checksum matches
    assert file_one.checksum == checksum_in_sign_file


def test_find_file_matching_signature(file_one):
    """Test finding a file that matches a pre-generated signature"""
    # Generate and save the signature for file_1
    file_one.calculate_file_checksum(BATCH_SIZE)
    file_one.save_signature()

    # Load the saved signature file
    signature_path = Path(join(TEST_DIR, f"{file_one.name}.sign"))
    signature = File.load_from_json(signature_path)

    # Calculate the checksum for file_1 again
    file_1_checksum = file_one.calculate_file_checksum(BATCH_SIZE)

    # Verify the file matches its own signature
    assert signature.checksum == file_1_checksum
    assert signature == file_one

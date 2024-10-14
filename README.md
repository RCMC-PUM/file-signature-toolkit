## File Signature Toolkit
![Static Badge](https://img.shields.io/badge/Python-3.10%7C3.11%7C3.12-blue)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)
![Static Badge](https://img.shields.io/badge/code_style-black-black)
![Static Badge](https://img.shields.io/badge/license-Apache_2.0-yellow)

### Overview
The File Signature Toolkit is a CLI-based tool that provides utilities for generating, validating, and comparing file signatures based on their cryptographic hash values. The tool is designed to ensure file integrity, detect modifications, and assist in file comparison using various hash algorithms.

The toolkit is built using Python and utilizes the click library for the CLI interface and hashlib for generating cryptographic hashes. Additionally, it supports batch processing of files and comparison of file integrity against pre-generated signature files.

### Features
- `Generate File Signature` - Create a cryptographic signature for files using different hash algorithms.
- `Validate File Signature` - Check if files match their previously generated signatures.
- `Compare Two Files` - Compare two files based on their cryptographic signatures.
- `Find Files Matching a Signature` - Search for files that match a given signature file.

### Installation

#### Requirements
- Python 3.10 or higher
- Poetry

#### Steps
   1. Clone the repository:

    ```
    git clone https://github.com/yourusername/file-signature-toolkit.git
    cd file-signature-toolkit
    ```

   2. Install dependencies using Poetry:

    ```
    poetry install
    ```
   
   3. Activate the virtual environment:

    ```
    poetry shell
    ```

### Usage
After installation, the file-signature-toolkit can be used through the command line interface (CLI).

#### Commands
##### Generate File Signature

   Generates a cryptographic signature for one or more files.

   ```
   python file-signature-toolkit.py generate-file-signature <files...> [OPTIONS]
   ```
   
   *Options:*

   - `--batch-size`, `-b`: Number of bytes to read in each batch. Helps avoid loading the entire file into memory.
   - `--hash-function`, `-f`: Hash algorithm to use (md5, sha1, sha224, sha256, sha384, sha512).

   *Example:*
 

   ```
   python file-signature-toolkit.py generate-file-signature data/*.fastq 
   ```

##### Validate File Signature

   Validates the integrity of one or more files by comparing them to their signature files.
   
   ```
   python file-signature-toolkit.py validate-file-signature <files...> [OPTIONS]
   ```
   
   *Options:*
   
   - `--batch-size`, `-b`: Number of bytes to read in each batch.
   
   *Example:*
   
   ```
   python file-signature-toolkit.py validate-file-signature data/*.fastq
   ```

##### Compare Two Files

   Compares two files based on their cryptographic hashes.
   
   ```
   python file-signature-toolkit.py compare-two-files --file-one <file_one> --file-two <file_two> [OPTIONS]
   ```
   
   *Options:*
   
   - `--batch-size`, `-b`: Number of bytes to read in each batch.
   - `--hash-function`, `-f`: Hash algorithm to use (md5, sha1, sha224, sha256, sha384, sha512).
   
   *Example:*
   
   ```
   python file-signature-toolkit.py compare-two-files --file-one file1.txt --file-two file2.txt
   ```

##### Find File Matching Signature

   Finds files that match a given signature file.
   
   ```
   python file-signature-toolkit.py find-file-matching-signature <files...> --signature-file <signature_file> [OPTIONS]
   ```
   
   *Options:*
   
   - `--batch-size`, `-b`: Number of bytes to read in each batch.
   
   *Example:*
   
   ```
   python file-signature-toolkit.py find-file-matching-signature data/*.fastq --signature-file example.fastq.sign
   ```

### Unit tests
To run unit tests.

```
pytest tests.py 
```

### License
This project is licensed under the Apache-2.0 license. See the LICENSE file for details.

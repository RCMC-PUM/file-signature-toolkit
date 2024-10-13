import json
from os.path import join
from pathlib import Path
from collections import defaultdict

import click
from tqdm import tqdm

from src.file import File


@click.group()
def cli():
    pass


@cli.command()
@click.argument(
    "files",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    nargs=-1,
)
@click.option(
    "--batch-size",
    "-b",
    default=8192,
    show_default=True,
    help="The number of bytes to read in single run. This allows to avoid loading whole file at once.",
)
@click.option(
    "--hash-function",
    "-t",
    type=click.Choice(
        ["md5", "sha1", "sha224", "sha256", "sha384", "sha512"], case_sensitive=False
    ),
    default="md5",
    show_default=True,
    help="Type of hash algorithm to use.",
)
def generate_file_signature(files: tuple[Path], batch_size: int, hash_function: str):
    files = [file for file in files if not file.suffix == ".sign"]

    for path in tqdm(files, desc="Creating file signature"):
        file = File(path, hash_function)
        file.calculate_file_checksum(batch_size)
        file.save_signature()

    click.echo(f"Created signature for {len(files)} files.")


@cli.command()
@click.argument(
    "files",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    nargs=-1,
)
@click.option(
    "--batch-size",
    "-b",
    default=8192,
    show_default=True,
    help="The number of bytes to read in single run. This allows to avoid loading whole file at once.",
)
def validate_file_signature(files: tuple[Path], batch_size):
    signatures = {Path(join(file.parent, f"{file.name}.sign")) for file in files if file.suffix != ".sign"}
    stats = defaultdict(int)

    for signature_file in signatures:
        with open(signature_file, "r") as handle:
            metadata = json.load(handle)
            hash_function = metadata["hash_function"]

            expected_file_path = join(signature_file.parent, metadata["name"])
            expected_file = File(expected_file_path, hash_function)

            checksum = expected_file.calculate_file_checksum(batch_size)
            validated = checksum == metadata["checksum"]

            if validated:
                stats["PASSED"] += 1
                click.echo(
                    click.style(
                        f"File {expected_file.name} integrity test PASSED", fg="green"
                    )
                )
            else:
                stats["FAILED"] += 1
                click.echo(
                    click.style(
                        f"File {expected_file.name} integrity test FAILED", fg="red"
                    )
                )

    click.echo(click.style("SUMMARY:", bold=True))
    click.echo(
        click.style(
            f"Files passing integrity test: {stats['PASSED']} / {len(signatures)}",
            bold=True,
        )
    )


@cli.command()
@click.option(
    "--file-one",
    "-fo",
    required=True,
    type=click.Path(exists=True, path_type=Path),
)
@click.option(
    "--file-two",
    "-ft",
    required=True,
    type=click.Path(exists=True, path_type=Path),
)
@click.option(
    "--batch-size",
    "-b",
    default=8192,
    show_default=True,
    help="The number of bytes to read in single run. This allows to avoid loading whole file at once.",
)
@click.option(
    "--hash-function",
    "-t",
    type=click.Choice(
        ["md5", "sha1", "sha224", "sha256", "sha384", "sha512"], case_sensitive=False
    ),
    default="md5",
    show_default=True,
    help="Type of hash algorithm to use.",
)
def compare_two_files(file_one, file_two, batch_size, hash_function):
    file_one = File(file_one, hash_function)
    file_one.calculate_file_checksum(batch_size)

    file_two = File(file_two, hash_function)
    file_two.calculate_file_checksum(batch_size)

    status = file_one == file_two

    if status:
        click.echo(click.style(f"File {file_one.path} == File {file_two.path}", fg="green"))
    else:
        click.echo(click.style(f"File {file_one.path} != File {file_two.path}", fg="red"))


@cli.command()
@click.argument(
    "files",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    nargs=-1,
)
@click.option(
    "--signature-file",
    "-s", required=True,
    type=click.Path(exists=True, path_type=Path)
)
@click.option(
    "--batch-size",
    "-b",
    default=8192,
    show_default=True,
    help="The number of bytes to read in single run. This allows to avoid loading whole file at once.",
)
def find_file_matching_signature(files, signature_file, batch_size):
    signature = File.load_from_json(signature_file)
    hash_function = signature.hash_function

    matched_files = []
    for file in tqdm(files, desc="Searching"):
        file = File(file, hash_function)
        checksum = file.calculate_file_checksum(batch_size)

        if signature.checksum == checksum:
            matched_files.append(file)

    for file in matched_files:
        click.echo(click.style(f"Signature of file {file.path} matches signature of provided file: {signature_file}", fg="green"))

    click.echo(click.style("DONE", bold=True))


if __name__ == "__main__":
    cli()

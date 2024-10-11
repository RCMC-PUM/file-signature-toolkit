from collections import defaultdict
from os.path import join, exists
from pathlib import Path
from glob import glob
import json

from tqdm import tqdm
import click

from src.file import File
from src.exceptions import FilesNotMatch


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "-sp",
    "--source-path",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    multiple=True,
    help="Source path(s) to download.",
)
@click.option(
    "-dp",
    "--destination-path",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="Destination path(s) to save.",
)
def download():
    click.echo("Downloading")


@cli.command()
@click.option(
    "-sp",
    "--source-path",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    multiple=True,
    help="Source path(s) to download.",
)
@click.option(
    "-dp",
    "--destination-path",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="Destination path(s) to save.",
)
def upload():
    click.echo("Uploading")


@cli.command()
@click.argument(
    "files",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    nargs=-1,
)
def generate_checksums(files: tuple[Path]):
    for path in tqdm(files, desc="Creating checksum for inputted files"):
        file = File(path)
        file.calculate_file_checksum()
        file.save_metadata()

    click.echo(f"Created checksum for {len(files)} files.")


@cli.command()
@click.argument(
    "files",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    nargs=-1,
)
def validate_checksums(files: tuple[Path]):
    metadata_files = {Path(join(file.parent, f"{file.stem}.json")) for file in files}
    stats = defaultdict(int)

    for file in metadata_files:
        with open(file, "r") as handle:
            metadata = json.load(handle)

            expected_file = join(file.parent, metadata["name"])
            expected_file = File(expected_file)

            checksum = expected_file.calculate_file_checksum()
            validated = checksum == metadata["checksum"]

            if validated:
                stats["PASSED"] += 1
                click.echo(click.style(f"File {expected_file.name} integrity test PASSED", fg="green"))
            else:
                stats["FAILED"] += 1
                click.echo(click.style(f"File {expected_file.name} integrity test FAILED", fg="red"))

    click.echo(click.style("SUMMARY:", bold=True))
    click.echo(click.style(f"Files passing integrity test: {stats['PASSED']} / {len(metadata_files)}", bold=True))


if __name__ == "__main__":
    cli()

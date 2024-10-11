import json
from collections import defaultdict
from os.path import join
from pathlib import Path

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
def generate_fingerprint(files: tuple[Path]):
    for path in tqdm(files, desc="Creating fingerprint"):
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
def validate_fingerprint(files: tuple[Path]):
    metadata_files = {Path(join(file.parent, f"{file.stem}.json")) for file in files}
    stats = defaultdict(int)

    for file in metadata_files:
        with open(file, "r") as handle:
            metadata = json.load(handle)

            expected_file = join(file.parent, metadata["name"])
            expected_file = File(expected_file)

            checksum = expected_file.calculate_file_checksum()
            filesize = expected_file.size

            validated = (checksum == metadata["checksum"]) and (
                filesize == metadata["size"]
            )

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
            f"Files passing integrity test: {stats['PASSED']} / {len(metadata_files)}",
            bold=True,
        )
    )


if __name__ == "__main__":
    cli()

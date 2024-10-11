import pathlib

import click


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "-sp",
    "--source-path",
    required=True,
    type=click.Path(exists=True, path_type=pathlib.Path),
    multiple=True,
    help="Source path(s) to download.",
)
@click.option(
    "-dp",
    "--destination-path",
    required=True,
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Destination path(s) to save.",
)
def download():
    click.echo("Downloading")


@cli.command()
@click.option(
    "-sp",
    "--source-path",
    required=True,
    type=click.Path(exists=True, path_type=pathlib.Path),
    multiple=True,
    help="Source path(s) to download.",
)
@click.option(
    "-dp",
    "--destination-path",
    required=True,
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Destination path(s) to save.",
)
def upload():
    click.echo("Uploading")


@cli.command()
@click.option(
    "-f",
    "--files",
    required=True,
    type=click.Path(exists=True, path_type=pathlib.Path),
    multiple=True,
    help="Path(s) to file(s) to validate integrity.",
)
def validate():
    click.echo("Validation")


if __name__ == "__main__":
    cli()

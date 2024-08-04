from pathlib import Path
import click

from mc_assets_extractor.extractor import extract_assets
from mc_assets_extractor.minecraft import MinecraftDir, get_minecraft_dir


@click.command()
@click.option(
    "--mcdir",
    help="The path to the .minecraft directory",
    type=click.Path(exists=True, file_okay=False),
    default=None,
    show_default=True,
    required=False,
)
@click.option(
    "--index",
    help="The index file to extract assets from",
    type=click.Path(exists=True, dir_okay=False),
    default=None,
    show_default=True,
    required=False,
)
@click.option(
    "--objects",
    help="The objects directory to extract assets from",
    type=click.Path(exists=True, file_okay=False),
    default=None,
    show_default=True,
    required=False,
)
@click.option(
    "--output",
    help="The output directory to store the extracted assets",
    type=click.Path(file_okay=False),
    default="output",
    show_default=True,
)
def main(
    mcdir: str | None,
    index: str | None,
    objects: str | None,
    output: str,
):
    mc_path = Path(mcdir) if mcdir else get_minecraft_dir()
    index_path = Path(index) if index else None
    objects_path = Path(objects) if objects else None
    output_path = Path(output)

    mc = MinecraftDir(mcdir=mc_path)
    index_path = index_path or mc.assets.get_latest_index()
    objects_path = objects_path or mc.assets.objects

    extract_assets(
        index_path,
        objects_path,
        output_path,
        print,
    )


if __name__ == "__main__":
    main()

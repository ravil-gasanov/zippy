

import typer

from zippy.core import compress, decompress

app = typer.Typer(help="Zippy CLI for compression and decompression")

@app.command()
def cli(
    compress_flag: bool = typer.Option(False, "-c", "--compress", help="Compress input", is_flag=True),
    decompress_flag: bool = typer.Option(False, "-d", "--decompress", help="Decompress input",  is_flag=True),
    read_path: str = typer.Option(..., "-r", "--read_path", help="Path to input file"),
    write_path: str | None = typer.Option(None, "-w", "--write_path", help="Optional output file"),
):
    """
    Zippy CLI — choose compression or decompression.
    """
    if compress_flag and decompress_flag:
        typer.echo("❌ Cannot use --compress and --decompress together", err=True)
        raise typer.Exit(code=1)

    if not compress_flag and not decompress_flag:
        typer.echo("❌ Must specify either --compress or --decompress", err=True)
        raise typer.Exit(code=1)

    if compress_flag:
        compress(read_path, write_path)
    elif decompress_flag:
        decompress(read_path, write_path)


def main():
    typer.run(cli)


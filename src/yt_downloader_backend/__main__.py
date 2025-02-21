import asyncio

import click
import hypercorn.asyncio

from yt_downloader_backend.app import create_app


@click.command()
@click.option("--host", default="127.0.0.1", help="Host to bind to")
@click.option("--port", default=8000, help="Port to bind to")
def main(host: str, port: int) -> None:
    config = hypercorn.asyncio.Config()
    config.bind = [f"{host}:{port}"]
    asyncio.run(hypercorn.asyncio.serve(create_app(), config))


if __name__ == "__main__":
    main()

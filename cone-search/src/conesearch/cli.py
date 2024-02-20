"""Administrative command-line interface."""

import json
import sys
from pathlib import Path

import click
import uvicorn
from fastapi.openapi.utils import get_openapi

from .main import app

__all__ = [
    "main",
    "openapi_schema",
    "run",
]


@click.group()
@click.version_option(message="%(version)s")
def main() -> None:
    """Administrative command-line interface for cone-search."""


@main.command()
@click.option(
    "--output",
    "-o",
    default=None,
    type=click.Path(path_type=Path),
    help="Output path (output to stdout if not given).",
)
def openapi_schema(*, output: Path | None) -> None:
    """Generate the OpenAPI schema."""
    schema = get_openapi(
        title=app.title,
        description=app.description,
        version=app.version,
        routes=app.routes,
    )
    if output:
        output.parent.mkdir(exist_ok=True)
        with output.open("w") as f:
            json.dump(schema, f, indent=2)
    else:
        json.dump(schema, sys.stdout, indent=2)


@main.command()
@click.option(
    "--port", default=8080, type=int, help="Port to run the application on."
)
def run(*, port: int) -> None:
    """Run the application."""
    uvicorn.run(
        "conesearch.main:app",
        port=port,
        reload=True,
        reload_dirs=["src"],
    )

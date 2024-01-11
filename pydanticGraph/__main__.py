import typer
from pydanticGraph import run, Config
from enum import Enum
import yaml  # type: ignore

from pathlib import Path
from typing import Optional
from typing_extensions import Annotated

"""
Allows to easily work with cli
Just write:
```bash
python pydanticGraph/
```
"""

app = typer.Typer()


class Example(str, Enum):
    simple = "simple"
    conv = "conv"
    lstm = "lstm"


# add options to load custom file
@app.command()
def start_server(
    config: Annotated[Optional[Path], typer.Option()] = None,
    network: Example = Example.simple,
):
    if config is None:
        print("Using default settings")
    elif config.is_file():
        text = config.read_text()
        print(f"Config file contents: {text}")
    elif config.is_dir():
        print("Config can not be a directory")
        raise typer.Abort()
    elif not config.exists():
        print("The config doesn't exist")
        raise typer.Abort()
    run()


if __name__ == "__main__":
    app()

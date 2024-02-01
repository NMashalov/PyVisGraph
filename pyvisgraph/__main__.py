import typer
from pyvisgraph import run, Config
from enum import Enum
import yaml  # type: ignore

import webbrowser

from pathlib import Path
from typing import Optional
from typing_extensions import Annotated
from .server import server

"""
Allows to easily work with cli
Just write:
```bash
python pydanticGraph/
```
"""

app = typer.Typer()


# add options to load custom file
@app.command()
def start(
    config: Annotated[Optional[Path], typer.Option()] = None,
):
    '''
    Provide to config
    '''
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
    webbrowser.open('http:/127.0.0.1', new=2)

if __name__ == "__main__":
    app()

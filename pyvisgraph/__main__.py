import typer
from .config import configs_app
from enum import Enum
import yaml  # type: ignore

import webbrowser
import uvicorn
from pyvisgraph.back import server


app = typer.Typer(help="Cli app for Graph Managment")
app.add_typer(configs_app, name="configs")


# add options to load custom file
@app.command()
def start():
    uvicorn.run(server)
    webbrowser.open("http:/127.0.0.1", new=2)


app()

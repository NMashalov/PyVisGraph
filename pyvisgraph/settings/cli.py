import typer 
from .utils import YamlPresetDir


app = typer.Typer()

@app.command('preset_folder')
def create_preset_folder():
    YamlPresetDir()

import typer
from pydanticGraph import (
    run,
    Config
)
import yaml  # type: ignore

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
def start_server(preset_path: str = 'preset_yaml'):
    # with open(f'../{preset_path}') as f:
    #     c = Config(yaml.safe_load(f.read()))
    run()


if __name__ == "__main__":
    app()

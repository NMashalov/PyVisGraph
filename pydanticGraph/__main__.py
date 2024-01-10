import typer
from pydanticGraph import run

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
def start_server():
    run()

if __name__ == "__main__":
    app()
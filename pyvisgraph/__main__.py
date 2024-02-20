from enum import Enum
import yaml  # type: ignore
import hydra

import webbrowser
import uvicorn
from pyvisgraph.backend import server


PRESET: Preset = Preset.from_configs()

@hydra.main(config_path='default.py-vis-graph-preset.yaml')
def start(cfg):
    if
            print("Creating preset")
        PRESET.print()
    uvicorn.run(server)
    webbrowser.open("http:/127.0.0.1", new=2)


app()

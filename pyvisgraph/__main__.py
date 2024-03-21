from pyvisgraph.settings.manager import PyVisGraphManager
import hydra
from pyvisgraph.settings.configs import Preset


@hydra.main(config_path="default.py-vis-graph-preset.yaml")
def start(cfg: Preset):
    PyVisGraphManager(cfg)

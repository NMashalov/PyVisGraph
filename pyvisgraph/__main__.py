from pyvisgraph.manager import PyVisGraphManager
import hydra
from configs import Preset


@hydra.main(config_path="default.py-vis-graph-preset.yaml")
def start(cfg: Preset):
    PyVisGraphManager(cfg)

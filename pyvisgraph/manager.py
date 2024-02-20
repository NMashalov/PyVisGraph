from pyvisgraph.configs import Preset, ConfigsManager
import hydra
from pyvisgraph.backend import OperatorMart


class PyVisGraphManager:
    def __init__(self,op_mart: OperatorMart, cfg_manager:  ConfigsManager):
        self.op_mart = op_mart
        self.config_manager = cfg_manager

@hydra.main(version_base=None, config_name="config")
def create_manger(cfg: Preset):

    return PyVisGraphManager(
        OperatorMart(
            export_models_name = cfg.format_input_settings.export_models_name,
            export_module_name =  cfg.format_input_settings.export_module_name,
            import_paths = cfg.import_paths,
            inputs_name: str,
            outputs_name: str
        ),
        ConfigsManager(
            cfg
        )

    )

  






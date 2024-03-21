import typing as tp
from pathlib import Path
from dataclasses import dataclass

from hydra.core.config_store import ConfigStore
from .manager import AbstractManager

from fastapi import APIRouter

"""
Import path parses all py file in directory 
and grabs all PydanticModels ans @registered nodes
"""


@dataclass
class ImportPath:
    relative_path: Path
    module_name: tp.Optional[str] = None


@dataclass
class Endpoints:
    """
    Opens API possibilities
    """
    endpoints: list[str]


@dataclass
class FormatInputSettings:
    export_models_name: str = "EXPORT_MODELS"
    export_module_name: str = "EXPORT_MODULE_NAME"
    inputs_name: str = "INPUTS"
    outputs_name: str = "OUTPUTS"


@dataclass
class FormatOutputSettings:
    format: tp.Literal["yaml", "json"]
    mode: tp.Literal["linear", "groups"]
    # naming
    dependency_name: str = "needs"
    properties_name: str = "arguments"
    default_dag_name: str = "pyvisgraph"
    default_group_name: str = "group"
    # info_fileds
    # properties of dag


@dataclass
class Preset:
    backend: tp.Literal["LiteGraph"] = "LiteGraph"
    import_paths: list[ImportPath] = []
    info_fields: tp.Optional[dict[str, str]] = None
    format_output_settings: FormatOutputSettings
    format_input_settings: FormatInputSettings


class WrongConfigs(ValueError):
    pass


class ConfigProvider:
    def __init__(self,  cfg: Preset):
        self.cfg = cfg

    def return_OperatorMartCfg(self):
        return OperatorMartCfg(
            export_models_name=self.preset.format_input_settings.export_models_name,
            export_module_name=self.preset.format_input_settings.export_module_name,
            import_paths=self.preset.import_paths,
            inputs_name=self.preset.format_input_settings.inputs_name,
            outputs_name=self.preset.format_input_settings.outputs_name,
        )
    



class ConfigsManager:
    """
    Responsible for changing configs from UI
    """

    def __init__(self, cfg: Preset):
        self.preset = cfg

    def provide_configs(self, manager : AbstractManager):   
        manager


    

    def router(self):
        configs_router = APIRouter(prefix="/settings", tags=["settings"])

        @configs_router.post("/output_format/{format}")
        def export():
            return
        

configs_manager = ConfigsManager()

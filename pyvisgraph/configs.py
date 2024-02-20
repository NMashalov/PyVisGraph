from pydantic import BaseModel, create_model
import typing as tp 
import typer
from pathlib import Path
import yaml
from dataclasses import dataclass

from hydra.core.config_store import ConfigStore

'''
Import path parses all py file in directory 
and grabs all PydanticModels ans @registered nodes
'''

@dataclass 
class ImportPath:
    relative_path: Path
    module_name: tp.Optional[str] = None

@dataclass 
class Endpoints:
    '''
    Opens API possibilities
    '''
    endpoints: list[str] 

@dataclass 
class FormatInputSettings:
    export_models_name: str = 'EXPORT_MODELS'
    export_module_name: str = 'EXPORT_MODULE_NAME'
    inputs_name: str = "INPUTS"
    outputs_name: str = "OUTPUTS"

@dataclass 
class FormatOutputSettings:
    format: tp.Literal['yaml','json']
    mode: tp.Literal['linear','groups']
    # naming
    dependency_name: str = 'needs'
    properties_name: str = 'arguments'
    default_dag_name: str = "pyvisgraph"
    default_group_name: str = "group"
    # info_fileds
    # properties of dag
    
@dataclass 
class Preset:
    backend: tp.Literal['LiteGraph'] = 'LiteGraph'
    import_paths: list[ImportPath] = []
    info_fields: tp.Optional[dict[str,str]] = None
    format_output_settings: FormatOutputSettings
    format_input_settings: FormatInputSettings



cs = ConfigStore.instance()
cs.store(name="config", node=Preset)


class WrongConfigs(ValueError):
    pass



class ConfigsManager:
    def __init__(self,cfg:Preset):
        self.preset = cfg

    def router(self):
        from fastapi import APIRouter
        from contextlib import asynccontextmanager
        from .manager import Manager


        @asynccontextmanager
        def lifespan():
            processor = ConfigsManager()
            yield
            del processor


        configs_router = APIRouter(prefix="/settings", lifespan=lifespan, tags=["settings"])


        @configs_router.post("/output_format/{format}")
        def export():
            return






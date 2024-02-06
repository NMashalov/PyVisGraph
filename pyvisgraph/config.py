from pydantic import BaseModel, create_model
import typing as tp 
import typer
from pathlib import Path
import yaml

app = typer.Typer()

LOCAL_PATH = Path(__file__).parent

'''
Import path parses all py file in directory 
and grabs all PydanticModels ans @registered nodes
'''

class ImportPath(BaseModel):
    relative_path: str
    module_name: tp.Optional[str] = None

class Endpoints(BaseModel):
    '''
    Opens API possibilities
    '''
    endpoints: list[str]    

class FormatOutputSettings(BaseModel):
    mode: tp.Literal['linear','groups']
    # naming
    dependency_name: str = 'needs'
    properties_name: str = 'arguments'
    default_dag_name: str = "pyvisgraph"
    default_group_name: str = "group"
    # info_fileds
    # properties of dag
    


class Preset(BaseModel):
    backend: tp.Literal['LiteGraph'] = 'LiteGraph'
    import_paths: list[ImportPath] = []
    info_fields: tp.Optional[dict[str,str]] = None
    format_output_settings: FormatOutputSettings

    @classmethod
    def from_configs(cls, preset_path: Path):
        if preset_path.exists():
            return cls(**yaml.safe_load(preset_path.read_text()))
        else:
            print("Path doesn't exist. Load default")
            load_default() 
    
    @classmethod
    def load_default(cls):
        file = LOCAL_PATH / 'default_configs.yaml'
        
    def dump(self, preset_path: Path):
        return preset_path.write_text()
    
    def to_yaml(self):
        return yaml.safe_dump(self.model_dump())

    @classmethod
    def load_local_preset(cls,preset_path: tp.Optional[Path] = None):  
        '''
        Awesome option from typer doc
        https://typer.tiangolo.com/tutorial/commands/callback/

        Allow option persistent option --preset_path for cli
        '''

        local_preset = Path.cwd() / '.py-vis-graph-preset.yaml'
        try:
            CONFIGS = cls.from_configs(local_preset)
        except Exception as e:
            print('Mistake in configs',e)

PRESET: Preset = Preset.from_configs()

configs_app = typer.Typer(
    help='Edit defualt configs of pyvisgraph'
)

@configs_app.command(help="")
def default():
    PRESET.print()


@configs_app.command()
def ():
    PRESET.print()


@configs_app.command()
def load():
    PRESET.print()


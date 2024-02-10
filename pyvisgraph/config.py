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
    format: tp.Literal['yaml','json']
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
            file = LOCAL_PATH / 'default_configs.yaml'

    def dump(self):
        local_preset = Path.cwd() / '.py-vis-graph-preset.yaml'
        try:
            local_preset.write_text(self.to_yaml())
        except Exception as e:
            print('Mistake in configs',e)

    def to_yaml(self):
        return yaml.safe_dump(self.model_dump())

    @classmethod
    def load_local_preset(cls,preset_path: tp.Optional[Path] = None):  
        '''
        Load preset from current path
        '''

        local_preset = Path.cwd() / '.py-vis-graph-preset.yaml'
        if local_preset.exists():
            try:
                CONFIGS = cls.from_configs(local_preset)
            except Exception as e:
                print('Mistake in configs',e)
        else:
            raise Exception 

PRESET: Preset = Preset.from_configs()

configs_app = typer.Typer(
    help='Edit defualt configs of pyvisgraph'
)

@configs_app.command(help="")
def start():
    if 
        print("Creating preset")
        PRESET.print()


@configs_app.command():
    


@configs_app.command()
def load():
    PRESET.print()


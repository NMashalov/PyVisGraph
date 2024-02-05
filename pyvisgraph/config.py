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

class OutputSettings(BaseModel):
    mode: tp.Literal['linear','groups']
    dependency_name: str
    properties_name: str


class DefaultGraphSettings(BaseModel):
    name: str = "actions"
    group_name: str = "group"
    properties: dict[str,str] = {}

class Preset(BaseModel):
    backend: tp.Literal['LiteGraph'] = 'LiteGraph'
    import_paths: list[ImportPath] = []
    default_graph_settings: DefaultGraphSettings
    output_settings: OutputSettings

    @classmethod
    def from_configs(cls, preset_path: Path):
        return cls(**yaml.safe_load(preset_path.read_text()))
    
    @classmethod
    def load_default(cls):
        file = LOCAL_PATH / 'default_configs.yaml'
        
    def save(self, preset_path: Path):
        return preset_path.write_text(yaml.safe_dump(self.model_dump()))
    
    def print(self):
        return yaml.safe_dump(self.model_dump())

    @classmethod
    def load_local_preset(preset_path: tp.Optional[Path] = None):  
        '''
        Awesome option from typer doc
        https://typer.tiangolo.com/tutorial/commands/callback/

        Allow option persistent option --preset_path for cli
        '''

        local_preset = Path.cwd() / '.py-vis-graph-preset.yaml'
        if local_preset.exists():
            try:
                CONFIGS = Preset.from_configs()
            except Exception as e:
                print('Mistake in configs')
        else:
            print("Create local preset with ")


PRESET: Preset = Preset.from_configs()


configs_app = typer.Typer(
    help='Edit defualt configs of pyvisgraph'
)


@configs_app.command()
def print():
    PRESET.print()


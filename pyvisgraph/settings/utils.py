from pathlib import Path
import yaml

def rmtree(root: Path):
    for p in root.iterdir():
        if p.is_dir():
            rmtree(p)
        else:
            p.unlink()
    root.rmdir()



class YamlPresetDir:
    '''
        Create directory for Hydra configuration
    '''
    def __init__(self,yaml_path:Path,preset_dir: Path):
        self.preset_dir = preset_dir
        self.read_preset_model(yaml_path)
        self.dag_dir = self.preset_dir / 'dag'
        self.action_dir = self.preset_dir / 'actions'

    def read_preset_model(self,yaml_path:Path):
        try:
            self.preset = Preset(**self.parse_yaml(yaml_path)['preset'])
        except Exception as e:
            raise ValueError(f'Check {yaml_path}') from e
    
    def init_dir(self):
        self.create_config_dir()
        self.create_actions()
        self.create_dag()
       
    def create_config_dir(self):
        if self.preset_dir.exists():
            rmtree(self.preset_dir)
        self.preset_dir.mkdir()
        self.dag_dir.mkdir()
        self.action_dir.mkdir()

    def create_actions(self):
        for group in self.preset.actions:
            print(group)
            group_name, group_actions = next(iter(group.items()))
            print(group_actions)
            group_file: Path = self.action_dir / f'{group_name}.yaml'
            group_file.write_text(yaml.safe_dump(group_actions))

    def create_dag(self):
        (self.dag_dir / 'base.yaml').write_text(yaml.safe_dump(self.preset.dag))
            

    @staticmethod
    def parse_yaml(yaml_path: Path):
        try:
            return yaml.safe_load(yaml_path.read_text())
        except:
            raise Exception(f'Wrong File! {yaml_path}')
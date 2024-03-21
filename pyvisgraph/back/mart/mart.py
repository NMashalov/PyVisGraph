from .operator import Operator
import uuid
from pyvisgraph.settings.configs import WrongConfigs
from dataclasses import dataclass
import typing as tp
import inspect

import importlib
from pathlib import Path


@dataclass
class FileOperatorProcessorCfg:
    '''
     Reads export model and module
        Arguments:
            export_models_name - name of dictionary. If not specified read all models from file
            export_module_name - name of module. If not specified takes ordinary name
            inputs_name -
            outputs_name -
    '''
    export_models_name: str = 'EXPORT_MODELS'
    export_module_name: str = 'EXPORT_MODULE_NAME'
    inputs_name: str = 'INPUTS'
    outputs_name: str = 'OUTPUTS'
    groups_name: str = 'GROUP'

class FileOperatorProcessor:
    """
    Explores module
    """

    def __init__(
        self,
        cfg: FileOperatorProcessorCfg
    ):
        """
        Processes file with models for U
        Example:    
            ```main.py
            class Cat:
                INPUTS: ('Toys', '.csv')
                OUTPUTS: ('Meow_model', '.pkl')

            EXPORT_MODELS_NAME = {
                'cat': Cat
            }
            EXPORT_MODULE_NAME = 'Cats'
            ```
        """
        self.cfg = cfg

    def process_paths(self, module_paths: list[Path]):
        operators_groups: dict[str, Operator] = {}
        operators_atlas: dict[uuid.UUID, Operator] = {}
        for path in module_paths:
            try:
                name, ops = self(path)
                operators_atlas.update(ops)
                operators_groups[name] = ops
            except Exception as e:
                print(e)
        return operators_groups, operators_atlas

    def format_operator(self, cls: object):
        op = Operator.from_class(cls, self.cfg.inputs_name, self.cfg.outputs_name)
        return op.id, op

    def __call__(self, module_path: Path):
        """
        Loads nodes from defined Path.
        Checks if it's right file
        """
        if not module_path.exists():
            raise ValueError(f"invalid path or file: {module_path}")

        module_name = str(module_path)

        module_spec: tp.ModuleType = importlib.util.spec_from_file_location(
            module_name, module_path
        )

        name = getattr(module_spec, self.cfg.export_module_name, module_name)

        # process with self.export_models_name
        if hasattr(module_spec, self.cfg.export_models_name):
            models_names = getattr(module_spec, self.cfg.export_module_name)
            try:
                output_dict = dict(
                    self.format_operator(model_name) for model_name in models_names
                )
            except AttributeError as e:
                raise WrongConfigs("Wrong import path") from e
            
            return name, output_dict
        else:
            raise ValueError(f'No {self.cfg.export_models_name} in module {module_path}')
            # def _check_class(x):
            #     return inspect.isclass(x) and x.__module__ == module_name

            # output_dict = dict(
            #     self.format_operator(cls)
            #     for cls in inspect.getmembers(module_spec, _check_class)
            # )

            # return name, output_dict


@dataclass
class OperatorMartCfg:
    file_processor_cfg: FileOperatorProcessorCfg
    import_paths: list[Path]


class OperatorMart:
    """
    Manages collection of
    operators and it's interaction with
    """

    def __init__(
        self,
        cfg: OperatorMartCfg
    ):
        self.cfg = cfg
        self.load_local(cfg.import_paths)
        
    def add_file_processor(self,file_processor_cfg: FileOperatorProcessorCfg):
        self.file_processor = FileOperatorProcessor(
            file_processor_cfg
        )

    def load_local(self, import_paths: list[Path]):
        self.operator_atlas: dict[uuid.UUID, Operator] = {}
        self.operators_groups, self.operator_atlas = self.file_processor.process_paths(
            import_paths
        )

    def to_groups(self):
        return self.operators_groups
    

operator_mart = OperatorMart()

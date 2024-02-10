from .operator import Operator
import uuid
from .format import GraphProcessor
from pydantic import BaseModel
import typing as tp
from types import ModuleType
import inspect
from pyvisgraph.config import Preset, PRESET


class OperatorProcessor:
    def __init__(self,preset):
        self.preset = preset

    def load_nodes_from_module(self,module: ModuleType, module_name: str):
        def _check_defined_pydantic(x):
            return (
                inspect.isclass(x)
                and issubclass(x, BaseModel)
                and x.__module__ == module_name
            )

        new_nodes = []
        for cls in inspect.getmembers(module, _check_defined_pydantic):
            new_node = Operator(*cls)
            new_nodes.append(new_node)
        return {"nodes": new_nodes, "module_name": module_name}
    
    def register(
        self, inputs: list[tuple] = [], outputs: list[tuple] = [], module_name: str = ""
    ):
        """
        Register any object
        INPUTS and OUTPUTS defined explicitly in decorator params
        Widgets yield from function signature
        """

        def decorator(func_to_node: tp.Callable):
            node = Operator.from_callable(
                func=func_to_node, inputs=inputs, outputs=outputs
            )

            self.operators[node.id] = node
            return func_to_node

        return decorator




class OperatorMart:
    '''
    Manages collection of
    operators and it's interaction with
    '''
    def __init__(self, processor: GraphProcessor, preset: Preset = PRESET, ):
        self.operators: dict[uuid.UUID, Operator] = {}
        self.backend = preset.backend
        self.processor = processor



    @classmethod
    def from_preset(cls):
        import_paths = PRESET.import_paths
        for import_path in import_paths:
            cls.load_nodes_from_module(import_path)
            cls.operators: dict[str, Operator] = {}


    def from_configs():
        pass

    def from_text(self, text: str, name: str):
        # creates new module
        module = ModuleType(name)
        # populate the module with code
        exec(contents, module.__dict__)
        return self.load_nodes_from_module(module, name)

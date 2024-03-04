from pydantic import BaseModel
from ..operator.operator import Operator
import typing as tp
import inspect


class CallableMixin:
    def register(
        self,  module_name: str = ""
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


class PydanticMixin:
    def load_pydantic_module(self, module: tp.ModuleType, module_name: str):
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

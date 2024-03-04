from typing import TypeVar, Type, ClassVar
from pydantic_core._pydantic_core import PydanticUndefinedType
from pydantic import BaseModel, Field
from .operator import IO


PydanticModels = TypeVar("PydanticModels", bound=BaseModel)



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



class PydanticLinkMixin:
    default_properties = {}

    @classmethod
    def from_pydantic(cls, model: PydanticModels):
        replace_with_None = (
            lambda x: None if isinstance(x, PydanticUndefinedType) else x
        )
        return {
            field_name: cls(
                description=str(field_info.description or ""),
                type=str(field_info.annotation),
                default_value=str(replace_with_None(field_info.default) or ""),
            )
            for field_name, field_info in model.model_fields.items()
        } | cls.default_properties


class PydanticOperatorMixin:
    @classmethod
    def from_pydantic(cls, name: str, model: PydanticModels):
        """
        Reads arbitary pydantic models to operator

        """

        doc = model.__doc__
        if doc:
            doc = doc.strip()

        return cls(
            name=name,
            io=IO.from_object(model),
            # model.model_fields don't contain fields of ClassVar
            properties=PydanticLinkMixin.from_pydantic(model),
            # put docstring to helper
            helper=doc,
        )

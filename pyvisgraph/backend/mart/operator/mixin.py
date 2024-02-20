from typing import TypeVar, Type, ClassVar
from pydantic_core._pydantic_core import PydanticUndefinedType
from pydantic import BaseModel, Field


PydanticModels = TypeVar("PydanticModels", bound=BaseModel)


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


class PydanticOperatorkMixin:
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

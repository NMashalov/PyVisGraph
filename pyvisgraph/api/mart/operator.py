from abc import abstractmethod
import typing as tp

import inspect
from functools import wraps
import uuid
from dataclasses import dataclass, field
from .mart import OperatorMart

@dataclass
class Link:
    name: str
    type: str

@dataclass
class IO:
    input: tp.Optional[list[Link]] = None
    output: tp.Optional[list[Link]] = None

    @staticmethod
    def get_attribute_items(model: object, attribute_name: str):
        return [Link(*item) for item in getattr(model, attribute_name, [])]

    @classmethod
    def from_object(cls, model: object):
        """
        Grab list of inputs Model should have
        Inputs a
        """


        return cls(
            input=cls.get_attribute_items(model, OperatorMart.cfg.file_processor_cfg.inputs_name),
            output=cls.get_attribute_items(model, OperatorMart.cfg.file_processor_cfg.outputs_name),
        )

    @classmethod
    def from_tuples(
        cls, inputs: list[tuple[str, ...]] = [], outputs: list[tuple[str, ...]] = []
    ):
        """
        Read tuples
        """
        get_links = lambda x, name: [Link(name=item[0], type=name) for item in x]
        return cls(input=get_links())


@dataclass
class Property:
    type: str
    default_value: tp.Optional[str] = None
    description: tp.Optional[str] = None

    @classmethod
    def parse_signature(cls, sign: inspect.Signature):
        """
        Read fields of function
        """
        replace_with_None = lambda x: None if x is inspect._empty else x
        return {
            field_name: cls(
                type=str(field_info.annotation),
                default_value=str(replace_with_None(field_info.default) or ""),
            )
            for field_name, field_info in sign.parameters.items()
        }


@dataclass
class Operator:
    name: str
    type: str
    id: str = field(default_factory=uuid.uuid1)
    io: IO
    properties: dict[str, Property]
    helper: tp.Optional[str] = None

    @classmethod
    def from_callable(
        cls, func: tp.Callable, inputs: list[tuple] = [], outputs: list[tuple] = []
    ):
        sign = inspect.signature(func)

        return cls(
            name=func.__name__,
            io=IO.from_tuples(inputs, outputs),
            # model.model_fields don't contain fields of ClassVar
            properties=Property.parse_signature(sign),
            # put docstring to helper
            helper=func.__doc__,
        )

    @classmethod
    def from_class(cls, input_cls: object):
        func = input_cls.__init__
        sign = inspect.signature(func)
        return cls(
            name=func.__name__,
            id=uuid.uuid1(),
            io=IO.from_object(input_cls),
            # model.model_fields don't contain fields of ClassVar
            properties=Property.parse_signature(sign),
            # put docstring to helper
            helper=func.__doc__,
        )

@dataclass
class OperatorGroup:
    name: str
    operators: list[Operator]

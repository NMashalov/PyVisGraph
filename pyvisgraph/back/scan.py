from pydantic import BaseModel, Field
from abc import abstractmethod
from typing import Optional, Callable
from pydantic_core._pydantic_core import PydanticUndefinedType
import inspect
from functools import wraps
import uuid 
from dataclasses import dataclass
from typing import TypeVar, Type, ClassVar




# generics
T = TypeVar("T")
PydanticModels = TypeVar("PydanticModels",bound=BaseModel)

class Link(BaseModel):
    name: str
    type: str

class IO(BaseModel):
    input: Optional[list[Link]] = None
    output: Optional[list[Link]] = None
    
    @staticmethod
    def get_attribute_items(model,attribute_name):
        return [
                Link(*item) 
                for item in getattr(model,attribute_name,[])
        ] 

    @classmethod
    def from_object(cls,model: object):
        '''
        Grab list of inputs Model should have
        '''
         
        return cls(
            input = cls.get_attribute_items('INPUTS'),
            output= cls.get_attribute_items('OUTPUTS')
        )

    @classmethod
    def from_tuples(cls,inputs: list[tuple[str,...]] = [], outputs: list[tuple[str,...]] = []):
        '''
        Read tuples 
        '''    
        get_links = lambda x, name: [Link(name=item[0], type=name) for item in x]
        return cls(
            input = get_links()
        )
        

class Property(BaseModel):
    type: str
    default_value: Optional[str] = None
    description: Optional[str] = None

    @property
    def default_properties(cls):
        return {}
   
    @classmethod
    def from_pydantic(cls,model: PydanticModels):
        """
        Note than fields of different types can not be connected!
        Example:
        ---
        from pydantic import BaseModel
        from typing import ClassVar
        class MyNode(Base):
            INPUTS : ClassVar = [
                Link(
                    name = 'Data',
                    type= 'csv'
                ),
                Link(
                    name = 'Model',
                    type= 'csv'
                ),
            ]
            OUTPUT : ClassVar = [
                Link(
                    name = 'Scores',
                    type= 'csv'
                ),
            ]
        """
        replace_with_None = lambda x: None if isinstance(x, PydanticUndefinedType) else x
        return {
                field_name: cls(
                    description=str(field_info.description or ""),
                    type=str(field_info.annotation),
                    default_value=str(replace_with_None(field_info.default) or ""),
                )
                for field_name, field_info in model.model_fields.items()
            } | cls.default_properties
        
    @classmethod
    def from_signature(cls,sign: inspect.Signature):
        '''
        Read fields of function
        '''
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
    id: str = Field(default_factory=uuid.uuid1)
    io: IO
    properties: dict[str, Property]
    helper: Optional[str] = None

    @classmethod
    def from_pydantic(cls, name: str, model: PydanticModels):
        '''
        Reads arbitary pydantic models to operator
        
        '''
        
        doc = model.__doc__
        if doc:
            doc = doc.strip()

        return cls(
            name=name,
            id=uuid.uuid1(),
            io = IO.from_object(model),
            # model.model_fields don't contain fields of ClassVar
            properties= Property.from_pydantic(model),
            # put docstring to helper
            helper=doc
        )
        
    @classmethod
    def from_callable(cls,func: Callable, inputs: list[tuple] = [], outputs: list[tuple] = []):
        sign = inspect.signature(func)
        
        return cls(
            name=func.__name__,
            id=uuid.uuid1(),
            io = IO.from_tuples(inputs,outputs),
            # model.model_fields don't contain fields of ClassVar
            properties=Property.from_signature(sign),
            # put docstring to helper
            helper=func.__doc__,
        ) 

    
    def validate_node():
        pass






# you may add default properties to node



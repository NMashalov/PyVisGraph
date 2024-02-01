from pydantic import BaseModel, Field
from abc import abstractmethod
from typing import Optional, Callable
from pydantic_core._pydantic_core import PydanticUndefinedType
import inspect
from functools import wraps
import uuid 
from typing import TypeVar, Type, ClassVar
from types import ModuleType



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


class Operator(BaseModel):
    name: str
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


class OperatorMart:
    def __init__(self):
        self.operators: dict[str,Operator] = {}
        

    def register(self,inputs: list[tuple] = [], outputs: list[tuple] = [], module_name: str = ''):
        """
        Register any object
        INPUTS and OUTPUTS defined explicitly in decorator params
        Widgets yield from function signature
        """

        def decorator(func_to_node: Callable):
            node = Operator.from_callable(func=func_to_node, inputs=inputs, outputs=outputs)

            self.operators[node.id] = node
            return func_to_node

        return decorator
    
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
            self.operators[new_node.hash] = cls[1]
        return {"nodes": new_nodes, "module_name": module_name}

    def validate_graph(self, g):
        if g.nodes:
            for node in g.nodes:
                props = node.properties
                hash_key = props.pop("hash")
                if props:
                    _NODE_MODELS[hash_key](**props)  # type: ignore

    def from_configs():
        pass


    def from_text(text: str, name: str):
        # creates new module
        module = ModuleType(name)
        # populate the module with code
        exec(contents, module.__dict__)
        return load_nodes_from_module(module, name)




# you may add default properties to node



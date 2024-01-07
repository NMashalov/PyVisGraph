from pydantic import (
    BaseModel,
    Field
)
from typing import ClassVar
from pathlib import Path

from pydanticGraph import load_custom_node,NODES

class Link(BaseModel):
    name: str 
    type: str 

class Car(BaseModel):
    engine: str = Field(description="Describes how much wheel")
    wheels: int = Field(description="Describes how much wheel")
    INPUTS : ClassVar = [
        Link(
            name = 'Data',
            type= 'csv' 
        )
    ]
#print(NODES)
    
path = Path(__file__).parent
load_custom_node(path / 'nodes.py')
#print(NODES)
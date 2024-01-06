from pydantic import BaseModel, Field
from typing import ClassVar
from pydanticGraph import Link

class Scoring(BaseModel):
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
    treshold: int = Field(description='How sharp will be nails')

class Dog(BaseModel):
    bark: int = Field(description="Will dog bark?")

    OUTPUT : ClassVar = [
        Link(
            name = 'Bones',
            type= '' 
        ),
    ]

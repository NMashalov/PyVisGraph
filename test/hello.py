from pydantic import (
    BaseModel,
    Field
)
from typing import ClassVar
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

for i,j in Car.model_fields.items():
    print(i,str(j.annotation))

print(Car.INPUTS)
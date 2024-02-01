from pydantic import BaseModel
from typing import ClassVar



class Animal(BaseModel):
    nose: int
    claws: int

    DEFAULT_PARAMETERS: ClassVar = [Animal(nose=1,claws=3)]

    def __new__(cls):
        instance = super().__new__(cls)
        instance.DEFAULT_PARAMETERS = [cls(nose=1,claws=3)]
        return instance


print(Animal.DEFAULT_PARAMETERS)
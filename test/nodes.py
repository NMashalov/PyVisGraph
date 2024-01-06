from pydantic import BaseModel, Field

class Cat(BaseModel):
    claws: int = Field(description='How sharp will be nails')

class Dog(BaseModel):
    bark: int = Field(description="Will dog bark?")

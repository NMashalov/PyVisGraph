from pydantic import BaseModel, Field
from abc import abstractmethod

class BaseNode(BaseModel):
    name: str
    inputs: dict[str,type]
    outputs: dict[str,type]
    needs: list[str]

def NodeFactory(
    Model
) -> :
    class ModelNode(BaseNode):
        widget: Model # type: ignore

    return ModelNode





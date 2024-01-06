from .node import NodeFactory
from pydantic import BaseModel

class Graph(BaseModel):
    name: str
    nodes: list[Node]
from pydantic import create_model, BaseModel
from pydanticGraph import SETTINGS
from typing import Optional


"""
Parse Graph to unified interior format


"""


class Input(BaseModel):
    link: Optional[int] = None
    type: str


class Node(BaseModel):
    id: int
    type: str
    inputs: list[Input] = []
    title: Optional[str] = None
    properties: dict[str, str] = {}


class Graph(BaseModel):
    nodes: Optional[list[Node]] = None
    links: Optional[list[list]] = None



# dag settigs model is created in runtime from user configs
DagInfo: type[BaseModel] = create_model(
    "DagInfo", ** {name: (str, item) for name, item in SETTINGS.dag_settings.items()} 
) # type: ignore


class Dag(BaseModel):
    graph: Graph
    dag_settings: DagInfo # type: ignore


class WrongGraphException(Exception):
    pass



    

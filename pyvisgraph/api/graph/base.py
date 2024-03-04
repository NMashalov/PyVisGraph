import typing as tp
import networkx as nx  # type: ignore
import collections
import typing as tp
from dataclasses import dataclass
import abc
from pydantic import BaseModel, create_model
from .processor import GraphProcessor

"""
Parse Graph to unified interior format
"""

# dag settigs model is created in runtime from user configs



class WrongGraphException(Exception):
    pass


@dataclass
class Node:
    id: int
    title: tp.Optional[str]
    type: str
    properties: dict[str, str]
    dependencies: tp.Optional[list[int]] = None


@dataclass
class Group:
    title: tp.Optional[str] = None
    nodes: list[Node]


class Graph:
    def __init__(self,atlas: nx.DiGraph):
        self.atlas = atlas


class GraphCreator:
    @abc.abstractmethod
    def to_graph(self):
        pass

class GraphManager:

    DagInfo: type[BaseModel] = create_model(
        "DagInfo", **{name: (str, item) for name, item in PRESET.info_fields.items()}
    )  # type: ignore

    

    def __init__(self):
        self.processor =  GraphProcessor()

    



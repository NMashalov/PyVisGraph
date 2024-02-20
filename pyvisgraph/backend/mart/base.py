import typing as tp
import networkx as nx  # type: ignore
import collections
from pyvisgraph import PRESET
import typing as tp
from dataclasses import dataclass
import abc
from pydantic import BaseModel, create_model

"""
Parse Graph to unified interior format
"""

# dag settigs model is created in runtime from user configs
DagInfo: type[BaseModel] = create_model(
    "DagInfo", **{name: (str, item) for name, item in PRESET.info_fields.items()}
)  # type: ignore


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


@dataclass
class Graph:
    """
    List of nodes ordered in topological order
    """

    atlas: nx.DiGraph


class GraphCreator:
    @abc.abstractmethod
    def to_graph(self):
        pass

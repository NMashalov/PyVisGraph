import typing as tp
import networkx as nx  # type: ignore
import collections
import typing as tp
from dataclasses import dataclass
import abc
from pydantic import BaseModel, create_model
from .formatter import GraphFormatter
from pyvisgraph.settings import AbstractManager,AbstractSettings

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


class Graph:
    '''
    Defines interface for work with nx.DiGraph
    '''
    def __init__(self,atlas: nx.DiGraph):
        self.atlas = atlas
    def dag_settings(self):
        return self.atlas['dag_settings']

@dataclass
class DagSettings:
    name: str
    timetable: str

@dataclass
class GraphManagerCfg:
    dependency_name:str
    group_name: str


class GraphManager(AbstractManager):
    def __init__(self,cfg:GraphManagerCfg):
        self.graph_state = Graph()
        self.formatter =  GraphFormatter()
        self.cfg = cfg
    def dag_settings(self):



graph_manager = GraphManager()


    



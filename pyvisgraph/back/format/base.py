import typing as tp
from pydantic import BaseModel, Field
import networkx as nx  # type: ignore
import collections

import yaml

from pydantic import create_model, BaseModel
from pyvisgraph import Preset, PRESET
import typing as tp

import abc

"""
Parse Graph to unified interior format
"""
class WrongGraphException(Exception):
    pass

class Link(BaseModel):
    name: str 
    type: str


class Node(BaseModel):
    title: str
    type: str
    properties: dict[str,str]
    dependencies: tp.Optional[list[Link]]

class Group(BaseModel):
    title:str
    nodes: list[Node]

class Graph(BaseModel):
    nodes: list[Node]

class GroupedGraph(BaseModel):
    groups: list[Group]


class BackendGraph(BaseModel):
    @abc.abstractmethod
    def to_graph():
        pass

    @abc.abstractmethod
    def to_groupped_graph():
        pass


class Namer:
    def __init__(self, preset: Preset):
        self.default_name_counter = collections.defaultdict(lambda: 0)
        self.group_name = preset.default_graph_settings.group_name

    def name(self, obj: Node | Group):
        if obj.title:
            return  obj.title
        
        if isinstance(obj, Node):
            suggestion = obj.type
        elif isinstance(obj, Node):
            suggestion = self.group_name
        self.default_name_counter[suggestion] +=1
        return f"{suggestion}_{self.default_name_counter[suggestion]}"
    

    def __call__(self, obj: Node | Group | Graph | GroupedGraph):
        '''
        Name structure in recursive way 
        '''
        if isinstance(obj, Node):
            title = self.name(obj)
            return {
                title: {
                    "properties": self.properties,
                    "dependencies":  self.dependencies
                } 
            }
    
        elif isinstance(obj, Group):
            title = self.name(obj)
            return {
                title: self(node) for node in self.nodes
            }
        elif isinstance(obj, Graph):
            return [self(node) for node in self.nodes]
        elif isinstance(obj, GroupedGraph):
            return  [self(group) for group in obj.groups]












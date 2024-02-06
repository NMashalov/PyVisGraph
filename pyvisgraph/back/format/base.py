import typing as tp
import networkx as nx  # type: ignore
import collections
from pyvisgraph import PRESET
import typing as tp
from dataclasses import dataclass
import abc
import functools


"""
Parse Graph to unified interior format
"""
class WrongGraphException(Exception):
    pass

@dataclass
class Node:
    title: tp.Optional[str]
    type: str
    properties: dict[str,str]
    dependencies: tp.Optional[list['Node']] = None

    def update_dependencies(self,node: 'Node'):
        if self.dependencies:
            self.dependencies.append(node)
        else:
            self.dependencies = [node]


class NetworkXMixin:
    def __init__(self,linkage:list[list[int]]):
        self.nx_graph =  nx.DiGraph(linkage)
    
    @functools.cached_property
    def sorted_dag(self):       
        return list(nx.topological_sort(self.nx_graph))
    
    @property
    def check_dag(self):
        return nx.is_directed_acyclic_graph(self.nx_graph)

    @functools.cached_property
    def generations(self):
        return nx.topological_generations(self.nx_graph)
    


@dataclass
class Group:
    title:str
    nodes: list[Node]

@dataclass
class Graph:
    '''
    List of nodes ordered in topological order
    '''
    nodes: list[Node]
    
@dataclass
class GroupedGraph:
    '''
    List of nodes ordered in topological generation
    '''
    groups: list[Group]

class GraphCreator:
    @abc.abstractmethod
    def to_graph(self):
        pass

    @abc.abstractmethod
    def to_groupped_graph(self):
        pass


class GraphBuilder(NetworkXMixin):
    def __init__(self,linkage: list[list[int]]):
        '''
        Graph
        '''
        super().__init__(linkage=linkage)
        if not self.check_dag:
            raise Exception('Should be DAG')
        for node_id in self.sorted_dag:
            pass
       
    def from_generator(cls,node_generator: tp.Iterator[Node]):

        self.graph = 

    def to_graph(self):
        return

    def to_grouped_graph(self):
        return GroupedGraph(self.base_groups)

















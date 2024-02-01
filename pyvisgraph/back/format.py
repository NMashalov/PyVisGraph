import typing as tp
from pydantic import BaseModel, Field
import networkx as nx  # type: ignore
import collections

import yaml

_NODE_MODELS: dict[str, BaseModel] = {}


from pydantic import create_model, BaseModel
from pyvisgraph import Preset, PRESET
from typing import Optional
import functools

"""
Parse Graph to unified interior format
"""
class WrongGraphException(Exception):
    pass

class Node(BaseModel):
    id: int
    type: str
    title: Optional[str] = None
    properties: dict[str, str] = {}
    dependencies: Optional[list[str]] = Field(default_factory=list)


class Group(BaseModel):
    bounding: list[int]
    title: str

class LiteGraphProcessor(BaseModel):
    nodes: list[Node]
    links: list[list[int]]

class Graph:
    def __init__(self,nodes: dict[int,Node],linkage: dict[int,int]):
        self.nodes = nodes
        self.linkage = linkage

    @classmethod
    def from_litegraph(cls, model:LiteGraphProcessor):
        nodes = {node.id: node for node in model.nodes}
        linkage = {(link[1],link[3]) for link in model.links}

        # add dependecies to node
        for link in linkage:
            nodes[link[0]].dependencies.append(link[1])
        cls()
    
    @functools.cached_property
    def ordered_groups(self):
        '''
        Topological sort of graph
        
        linked list
        [: []]
        '''
        DG = nx.DiGraph(self.linkage)
        return [
            sorted(generation) for generation in nx.topological_generations(DG)
        ]

class FormatProcessor:
    def __init__(self, preset: Preset, g: Graph):
        self.process_preset(preset)
        self.default_name_counter = collections.defaultdict(lambda: 0)
        self.name_mapping = {node.id: self.name_node(node.title) for node in nodes}

    @classmethod
    def process_graph(cls, g: Graph):
        cls(PRESET,g)

    def process_preset(self, preset: Preset):
        self.dependency_name = preset.output_settings.dependency_name
        self.properties_name = preset.output_settings.properties_name
        self.group_name = preset.default_graph_settings.group_name
        self.task_name = preset.default_graph_settings.task_name

    def default_name(self,suggestion:str):
        return f"{suggestion}_{self.default_name_counter[suggestion]}"

    def name_node(self, node: Node):
        '''
        Give node default name by it's type if not defined
        '''
        return  node.title if node.title else self.default_name(node.type)
         
    def node_info(self,node):
        '''
        Node should contain information about
        properties and it's linkage with other nodes
        ''' 
    
        dependencies =  [self.name_node() for input in node.inputs if input.link] 

        node.update_dependencies()

    def format_graph(self, g: Graph):
        groups = g.ordered_groups()

        id_to_name = self.name_mapping(g.nodes)
    
        connections = g.edges_connections()
        
        for con in connections:

    
            return [
                {
                    _name_group(group): {
                        name_mappping[node_id]: node_map[node_id] for node_id in group
                    }
                }
                for group in grouped_dag
            ]


    @classmethod
    def from_configs(cls):
        return cls(PRESET)


# dag settigs model is created in runtime from user configs
DagInfo: type[BaseModel] = create_model(
    "DagInfo", **{name: (str, item) for name, item in SETTINGS.dag_settings.items()}
)  # type: ignore







class Dag(BaseModel):
    graph: Graph
    dag_settings: DagInfo  # type: ignore
        
    def to_groups_yaml(self):
        yaml.safe_dump(
        {
            SETTINGS.template_settings.dag_info_name: g.dag_settings.dict(),  # type: ignore
            SETTINGS.template_settings.graph_name: _format_to_groups(g.graph),
        }




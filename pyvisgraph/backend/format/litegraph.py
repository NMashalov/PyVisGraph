from pydantic import BaseModel, create_model, Field
from ..mart.base import Node, Graph, Group, DagInfo
import typing as tp
import collections
import networkx as nx  # type: ignore
from pyvisgraph import PRESET


"""
Read input graph and 
"""

class Size(BaseModel):
    x: int  = Field(validation_alias='0')
    y: int  = Field(validation_alias='1')

class LiteGraphNode(BaseModel):
    id: int
    type: str
    title: tp.Optional[str] = None
    properties: dict[str, str] = {}
    pos: list[int]
    size: Size

    def to_base_node(self, predecessors: list[Node]):
        return Node(
            title=self.title,
            properties=self.properties,
            type=self.type,
            dependencies=predecessors
        )

class LiteGraphGroup(BaseModel):
    bounding: list[int]
    title: str

    def to_corner_xy(self):
        """
        Group Bounding in YoLo format:
        bounding[0] - x center
        bounding[1] - y center
        bounding[2] - width
        bounding[3] - height
        """
        x, y, w, h = self.bounding
        x_min, x_max = x - w / 2, x + w / 2
        y_min, y_max = y - h / 2, y + h / 2
        return x_min, y_min, x_max, y_max

    def nodes_in_group(self, nodes: list[LiteGraphNode]):
        """
        Node center
        pos[0] -x , pos[1] -y
        """
        x_min, y_min, x_max, y_max = self.to_corner_xy()

        included_nodes: list[LiteGraphNode] = []

        for node in nodes:
            pos = node.pos
            if (x_min <= pos[0] <= x_max) and (y_min <= pos[1] <= y_max):
                included_nodes.append(node)
        return included_nodes

    def to_base_group(
        self, linkage: dict[int, set[LiteGraphNode]], nodes: list[LiteGraphNode]
    ):
        return Group(
            title=self.title,
            nodes=[node.to_base_node() for node in self.nodes_in_group(nodes)],
        )


class LiteGraph(BaseModel):
    nodes: list[LiteGraphNode]
    groups: list[LiteGraphGroup]
    links: list[list[int]]

    def __init__(self,nodes: list[LiteGraphNode],  groups: list[LiteGraphGroup],links: list[list[int]]):
        super().__init__(nodes=nodes,groups=groups,links=links) 
        self.add_graph()
        self.add_base_nodes()

    def add_graph(self):
        """
        Link example
            [
                3,
                2,
                0,
                5,
                0,
                ".csv"
            ],
        0 - link id
        1 position - source node
        3 poistion - target node
        We'll form linkage in form of necessities of node
        """
        self._nx_graph = nx.DiGraph()

        for node in self.nodes: 
            self._nx_graph.add_node(node.id, node=node)

        self._nx_graph.add_edges_from((link[1],link[3]) for link in self.links)

        if not nx.is_directed_acyclic_graph(self._nx_graph):   
            raise NotImplementedError('Only DAG-s are supported')
        
    def get_predecessors(self,id:int):  
        return [self[predecessors_id]['base_node'] for predecessors_id in self._nx_graph.predecessors(id)] 
    
    def __getitem__(self,id: int):
        '''
            Returns base node representation
        '''
        return self._nx_graph.nodes[id]
    

    def add_base_nodes(self):       
        for node_id in nx.topological_sort(self._nx_graph):
            node:  LiteGraphNode = self[node_id]['node']
            predecessors = self.get_predecessors(node_id)
            base_node = node.to_base_node(predecessors) 
            self[node_id]['base_node'] = base_node
        
    def return_graph(self):
        return Graph(atlas = self._nx_graph )

    
    def __del__(self):
        '''
            Clear node info from atlas
        '''
        for (d,g) in self._nx_graph.nodes(data=True):
            del g['node']


class LiteGraphOutput(BaseModel):
    graph: LiteGraph
    dag_settings: DagInfo  # type: ignore


class BadLiteGraphOutput(Exception):
    pass
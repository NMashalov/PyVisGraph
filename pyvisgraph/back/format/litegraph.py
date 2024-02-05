from pydantic import BaseModel, create_model
from .base import Node, Graph,Group,GroupedGraph,BackendGraph
import typing as tp
import functools
import networkx as nx  # type: ignore
from collections import defaultdict

'''
Read input graph and 
'''


class LiteGraphNode(BaseModel):
    id: int
    type: str
    title: tp.Optional[str] = None
    properties: dict[str, str] = {}
    pos: list[int]

    def to_base_node(self,linkage: dict[int,set[Node]]):
        return Node(
                title=self.title,
                properties=self.properties,
                dependencies=linkage.get(self.id,None)
            )


class LiteGraphGroup(BaseModel):
    bounding: list[int]
    title: tp.Optional[str] = None 

    def to_corener_xy(self):
        ''' 
        Group Bounding in YoLo format:
        bounding[0] - x center
        bounding[1] - y center 
        bounding[2] - width
        bounding[3] - height
        '''
        x,y,w,h = self.bounding
        x_min, x_max = x-w/2, x+w/2
        y_min, y_max = y-h/2, y+h/2
        return x_min, y_min, x_max, y_max
    
    @functools.cached_property
    def nodes_in_group(self,nodes:list[LiteGraphNode]):
        '''
        Node center
        pos[0] -x , pos[1] -y 
        '''
        x_min, y_min, x_max, y_max = self.to_corener_xy()

        included_nodes = []

        for node in nodes:
            pos = node.pos
            if  (x_min <= pos[0] <= x_max) and (y_min <= pos[1] <= y_max):
                included_nodes.append(nodes)
        return included_nodes
    
    def to_base_group(self,linkage: dict[int,set[Node]]):
        return Group(
            title=self.title,
            nodes=[node.to_base_node(linkage) for node in self.nodes_in_group]
        )



class LiteGraph(BackendGraph,BaseModel):
    nodes : list[LiteGraphNode]
    groups: list[LiteGraphGroup]
    links : list[list[int]]

    @functools.cached_property
    def linkage(self): 
        '''
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
        '''
        linkage = defaultdict(set)
        for link in self.links:
            linkage[link[1]].add(link[3])
        return linkage
    

    @functools.cached_property
    def base_nodes(self):
        linkage = self.linkage
        return [node.to_base_node(linkage) for node in self.nodes]


    @functools.cached_property
    def base_groups(self):
        linkage = self.linkage
        return GroupedGraph(groups=[group.to_base_group(linkage)for group in self.groups])
         

    @functools.cached_property
    def order_groups(self):
        '''
        Topological sort of graph
        
        linked list
        [group: []]
        '''
        DG = nx.DiGraph(self.linkage)

        return [
            sorted(generation) for generation in nx.topological_generations(DG)
        ]

    def to_graph(self):
        return Graph(
            self.base_nodes
        )

    def to_groupped_graph(self):
        self.linkage(self)
        nodes = {node.id: node for node in self.nodes}
        linkage: set = []

        for group in self.groups:
            for node in nodes:
                for link in node.links: 
                    linkage.add((link[0]))
                    for link in linkage:
                        nodes[link[0]].dependencies.append(link[1])

        return GroupedGraph(nodes=nodes,)

 # dag settigs model is created in runtime from user configs
DagInfo: type[BaseModel] = create_model(
    "DagInfo", **{name: (str, item) for name, item in SETTINGS.dag_settings.items()}
)  # type: ignore   


class LiteGraphDag(BaseModel):
    graph: Graph
    dag_settings: DagInfo  # type: ignore


        

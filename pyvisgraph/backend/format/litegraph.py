from pydantic import BaseModel, create_model
from .base import Node, Graph, Group, GroupedGraph, BackendGraph
import typing as tp
import functools
import collections
import networkx as nx  # type: ignore
from collections import defaultdict
from pyvisgraph import PRESET

"""
Read input graph and 
"""


class LiteGraphNode(BaseModel):
    id: int
    type: str
    title: tp.Optional[str] = None
    properties: dict[str, str] = {}
    pos: list[int]

    def to_base_node(self):
        return Node(
            title=self.title,
            properties=self.properties,
            type=self.type,
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

    @functools.cached_property
    def linkage(self):
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
        linkage = collections.defaultdict(list)
        for link in self.links:
            linkage[link[1]].append(link[3])
        return linkage

    def base_nodes_generator(self):
        return (node.to_base_node(self.linkage) for node in self.nodes)

    def base_groups_generator(self):
        return (group.to_base_group(self.linkage) for group in self.groups)


# dag settigs model is created in runtime from user configs
DagInfo: type[BaseModel] = create_model(
    "DagInfo", **{name: (str, item) for name, item in PRESET.info_fields.items()}
)  # type: ignore


class LiteGraphDag(BaseModel):
    graph: Graph
    dag_settings: DagInfo  # type: ignore

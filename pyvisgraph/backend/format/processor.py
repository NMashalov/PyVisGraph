import typing as tp
from pydantic import BaseModel, Field

from pyvisgraph import Preset, PRESET
from .base import Link, Graph, Group, Node, GroupedGraph
from .litegraph import LiteGraphDag
import collections


class DependenciesOutput(BaseModel):
    name: str

    @classmethod
    def from_base_link(cls, link: Link):
        return cls()


class NodeOutput(BaseModel):
    properties: DependenciesOutput
    dependencies: dict[str, str] = Field(alias=PRESET.output_settings.dependency_name)

    @classmethod
    def from_base_node(cls, node: Node):
        return cls(properties=node.properties, dependencies=node.dependencies)


class GroupOutput(BaseModel):
    nodes: dict[str, NodeOutput]

    @classmethod
    def from_base_node_generator(cls, gen: tp.Iterator[str, Node]):
        return cls(nodes={title: node for title, node in gen})


class GroupedGraphOutput(BaseModel):
    groups: list[dict[str, GroupOutput]]


class GraphOutput(BaseModel):
    nodes: dict[str, NodeOutput]


class Namer:
    def __init__(self, preset: Preset):
        self.default_name_counter: collections.defaultdict[
            str, int
        ] = collections.defaultdict(lambda: 0)
        self.group_name = preset.default_graph_settings.group_name

    def name(self, obj: Node | Group):
        if obj.title:
            return obj.title
        if isinstance(obj, Node):
            suggestion = obj.type
        elif isinstance(obj, Group):
            suggestion = self.group_name
        self.default_name_counter[suggestion] += 1
        return f"{suggestion}_{self.default_name_counter[suggestion]}"

    def __call__(self, obj: Node | Group | Graph | GroupedGraph):
        """
        Name structure in recursive way
        """
        if isinstance(obj, Node):
            title = self.name(obj)
            return {title: NodeOutput.from_base_node(obj)}

        elif isinstance(obj, Group):
            title = self.name(obj)
            return {
                title: GroupOutput.from_base_node_generator(
                    self(node) for node in obj.nodes
                )
            }
        elif isinstance(obj, Graph):
            return GraphOutput
        elif isinstance(obj, GroupedGraph):
            return [self(group) for group in obj.groups]


class GraphProcessor:
    """
    Processess graph to output file
    """

    def __init__(self, preset: Preset, namer: Namer):
        super().__init__()
        self.from_preset(preset)
        self.namer = namer

    def process_graph(self, graph: dict):
        """
        Input arbitrary graph
        """
        if self.backend == "LiteGraph":
            dag = LiteGraphDag(**graph)
            if self.mode == "linear":
                graph = GraphOutput()
            elif self.mode == "groups":
                graph = GroupedGraphOutput(**dag.graph.to_graph())
            else:
                raise NotImplemented(
                    f"Invalid backend parameter {self.backend}. Only Litegraph backend is available"
                )

            return self.namer(graph)

        else:
            raise NotImplemented(
                f"Invalid backend parameter {self.backend}. Only Litegraph backend is available"
            )

    def from_preset(self, preset: Preset):
        self.mode = preset.output_settings.mode
        self.backend = preset.backend

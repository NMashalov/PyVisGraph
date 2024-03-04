import typing as tp
from pydantic import BaseModel, Field

from pyvisgraph import Preset, PRESET
from pyvisgraph.mart import Graph, Group, Node, DagInfo
from ..backend.format.litegraph import LiteGraphOutput, BadLiteGraphOutput
import collections
import networkx as nx
import yaml


class DependenciesOutput(BaseModel):
    name: str
    type: str


class NodeOutput(BaseModel):
    properties: dict[str, str]
    dependencies: list[str] = Field(alias=PRESET.format_output_settings.dependency_name)


class GroupOutput(BaseModel):
    nodes: dict[str, NodeOutput]

    @classmethod
    def from_group(cls, gen: tp.Iterator[str, Node]):
        return cls(nodes={title: node for title, node in gen})


class GroupedGraphOutput(BaseModel):
    groups: list[dict[str, GroupOutput]]


class GraphOutput(BaseModel):
    nodes: dict[str, NodeOutput]


class Output(BaseModel):
    graph: GroupedGraphOutput | GraphOutput
    dag_info: DagInfo = Field(alias=PRESET.format_output_settings.dependency_name)


class Namer:
    """
    Deduplicate names in graph
    """

    def __init__(self, atlas: nx.DiGraph):
        self.name_counter: collections.defaultdict[str, int] = collections.defaultdict(
            lambda: 0
        )
        self.atlas = atlas
        self.process_preset(PRESET)

    def __del__(self):
        for _, state in self.atlas.nodes(data=True):
            del state["name"]

    def process_preset(self, preset: Preset):
        self.group_name = preset.format_output_settings.mode

    def suggest(self, obj: Node | Group):
        if getattr(obj, "title", False):
            return obj.title
        elif isinstance(obj, Node):
            return obj.type
        elif isinstance(obj, Group):
            return self.group_name
        else:
            raise NotImplemented(f"Unsupported type {type(obj)}")

    def name_group(self, group_ids: list[int]):
        pass
        Group(title="group", nodes=[self(id) for id in group_ids])

    def name_node(self, id: int):
        if id not in self.atlas.nodes:
            suggestion = self.suggest(self.atlas.nodes[id]["base_node"])
            self.name_counter[suggestion] += 1

            title = (
                suggestion
                if self.name_counter > 1
                else f"{suggestion}_{self.name_counter[suggestion]}"
            )
            self.atlas.nodes[id]["title"] = title

        d: Node = self.atlas.nodes[id]["BaseNode"]

        deps_name = [self(node_id) for node_id in d["dependencies"]]

        return title, NodeOutput(dependencies=deps_name, properties=d.properties)

    def __call__(self, id: int):
        """
        Remember node title from id
        """
        return self.atlas.nodes[id]["title"]


class BadFormatException(Exception):
    pass


class GraphProcessor:
    """
    Processess graph to output file
    """

    def __init__(self, mode: str, backend: str, format: str):
        super().__init__()

        self.mode = mode
        self.backend = backend
        self.format = format

    def output_graph(self, atlas: nx.DiGraph):
        """
        Depending on mode ouputs graph
        in linear or group represenation
        """
        graph_output = {}
        namer = Namer(atlas)
        if self.mode == "linear":
            for node_id in nx.topological_sort(atlas):
                title, node = namer.name_node(node_id)
                graph_output[title] = node
            return GraphOutput(nodes=graph_output)
        elif self.mode == "groups":
            for group_ids in nx.topological_generations(atlas):
                title, node = namer.name_group(group_ids)
                graph_output[title] = title
            return GroupedGraphOutput(groups=graph_output)
        else:
            raise (f"Not implemented mode {self.mode}")

    def format_output(self, output: Output):
        if self.format == "yaml":
            return yaml.safe_dump(output.model_dump())
        elif self.format == "json":
            return output.model_dump_json()
        else:
            raise (f"Unsupported mode {self.format}. Should be in yaml, json")

    def __call__(self, graph: dict):
        """
        Input arbitrary graph
        """
        if self.backend == "LiteGraph":
            try:
                dag = LiteGraphOutput(**graph)
            except Exception as e:
                raise BadLiteGraphOutput from e
            try:
                graph = self.output_graph(dag.graph.return_graph().atlas)
            except Exception as e:
                raise BadFormatException from e
            return Output(dag_info=dag.dag_settings, graph=graph)
        else:
            raise NotImplemented(
                f"Invalid backend parameter {self.backend}. Only Litegraph backend is available"
            )

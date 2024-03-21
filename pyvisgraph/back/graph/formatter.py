import typing as tp
from pydantic import BaseModel, Field
from .base import Graph,graph_manager
from .utils import Namer
import networkx as nx
import yaml

class DependenciesOutput(BaseModel):
    name: str
    type: str

class NodeOutput(BaseModel):
    properties: dict[str, str]
    dependencies: list[str] = Field(alias=graph_manager.cfg.dependency_name)

class GroupOutput(BaseModel):
    nodes: dict[str, NodeOutput]

    @classmethod
    def from_group(cls, gen: tp.Iterator[str, NodeOutput]):
        return cls(nodes={title: node for title, node in gen})

class GroupedGraphOutput(BaseModel):
    groups: list[dict[str, GroupOutput]]

class DagOutput(BaseModel):
    graph: GroupedGraphOutput
    dag_info: dict[str,str]

class BadFormatException(Exception):
    pass

class GraphFormatter:
    """
    Processess graph to output file
    """

    def __init__(self, format: str):
        super().__init__()
        self.format = format

    def return_graph_preset(self, atlas: nx.DiGraph):
        graph_output = {}
        namer = Namer(atlas)
        for group_ids in nx.topological_generations(atlas):
            title, node = namer.name_group(group_ids)
            graph_output[title] = title
        return GroupedGraphOutput(groups=graph_output)

    def format_output(self, output: DagOutput):
        if self.format == "yaml":
            return yaml.safe_dump(output.model_dump())
        elif self.format == "json":
            return output.model_dump_json()
        else:
            raise (f"Unsupported mode {self.format}. Should be in yaml, json")

    def __call__(self, graph: Graph):
        """
        Input arbitrary graph
        """
        try:
            graph = self.output_graph(graph.return_graph().atlas)
        except Exception as e:
            raise BadFormatException from e

        return DagOutput(dag_info=graphs.dag_settings, graph=graph)


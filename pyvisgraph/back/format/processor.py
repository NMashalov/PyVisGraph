import typing as tp
from pydantic import BaseModel, Field

import collections
from pyvisgraph import Preset,PRESET
from .base import Graph, Node,GroupedGraph, Namer
from .litegraph import LiteGraphDag

class NodeOutput(BaseModel):
    properties: dict[str,str] 
    dependencies: dict[str,str] = Field(alias =  PRESET.output_settings.dependency_name)

class GroupOutput(BaseModel):
    nodes: dict[str, NodeOutput]

class GroupedGraphOutput(BaseModel):
    groups: list[dict[str,GroupOutput]]

class GraphOutput(BaseModel):
    nodes: dict[str,NodeOutput]


class GraphProcessor:
    '''
    Processess graph to output file
    '''
    def __init__(self, preset: Preset, namer: Namer):
        super().__init__()
        self.from_preset(preset) 

    def process_graph(self,graph: dict):
        '''
        Input arbitrary graph 
        '''
        if self.backend == 'LiteGraph':
            dag = LiteGraphDag(**graph)
            if self.mode == 'linear':
                graph = GraphOutput(**dag.graph.to_graph())
            elif self.mode == 'groups':
                graph = GroupedGraphOutput(**dag.graph.to_graph())
            else:
                raise NotImplemented(f'Invalid backend parameter {self.backend}. Only Litegraph backend is available')

            return Graph


        else:
            raise NotImplemented(f'Invalid backend parameter {self.backend}. Only Litegraph backend is available')


    def from_preset(self, preset: Preset):
        self.mode = preset.output_settings.mode
        self.backend = preset.backend



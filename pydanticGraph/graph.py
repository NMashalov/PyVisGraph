from pydantic import (
    create_model,
    BaseModel
)
from typing import Optional
import networkx as nx  # type: ignore

"""
Parse Graph to unified interior format


"""
class Outputs(BaseModel):
    links: Optional[list[int]] = None
    type: str

class Node(BaseModel):
    id: int
    type: str
    outputs: Optional[list[Outputs]] = None
    title: Optional[str] = None
    properties: dict[str, str] = {}

class Graph(BaseModel):
    nodes: Optional[list[Node]] = None
    links: Optional[list[list]] = None

class DagInfo(BaseModel):
    name: str
    schedule: str

def _overrideDagInfo():
    global SettingsClass
    SettingsClass = create_model(
        'DynamicFoobarModel', timetable = (str,...)
    )

class Dag(BaseModel):
    graph: Graph
    dag_info: DagInfo

class WrongGraphException(Exception):
    pass

def sequential_groups(model: dict):
    """
    Validate and format in sequential parallel group for parallel DAG execution
    using nx.topological_generations(DG)
    """
    g = Graph(**model)
    links = g.links
    nodes = g.nodes

    if nodes and links:
        take_ids = lambda x: (links[x - 1][1], links[x - 1][3])
        linkage = [
            take_ids(link)
            for node in nodes
            if node.outputs is not None
            for output in node.outputs
            if output.links is not None
            for link in output.links
        ]

        DG = nx.DiGraph(linkage)
        groupped_dag = [sorted(generation) for generation in nx.topological_generations(DG)]

        return groupped_dag, g
    else:
        raise WrongGraphException('Graph should have edges')
    


    

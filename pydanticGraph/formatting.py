# Formating
from pydantic import BaseModel
from pydanticGraph import Graph, Dag, WrongGraphException, SETTINGS
import yaml  # type: ignore
import networkx as nx  # type: ignore
from itertools import chain


class IncrementalName:
    def __init__(self, defualt_name):
        self.default_name = defualt_name
        self.default_counter = 0

    def __call__(self, task):
        if getattr(task, "title", None):
            return task.name
        else:
            self.default_counter += 1
            return f"{self.default_name}_{self.default_counter}"


def _format_to_groups(
    g: Graph
):
    print
    links = g.links
    nodes = g.nodes

    if nodes is None or links is None:
        raise WrongGraphException("Graph should have nodes and links")
    else:
        # link has format [1,1,0,2,1,'.csv']
        # link[0] - id of link (order of bringing links to folder)
        # link[1] - id of source node
        # link[3] - id of target node
        # node.outputs contain use link id
        # that's why we need link_map
        # you can have better understanding looking at graph.json in test folder

        link_map = {link[0]: link for link in links}
        take_ids = lambda x: (link_map[x][1], link_map[x][3],)
        linkage = {
            input.link: take_ids(input.link)
            for node in nodes
            if node.inputs is not None
            for input in node.inputs
            if input.link is not None
        }

        DG = nx.DiGraph(linkage.values())
        grouped_dag = [
            sorted(generation) for generation in nx.topological_generations(DG)
        ]
        _name_task = IncrementalName(SETTINGS.template_settings.default_task_name)

        name_mappping = {node.id: node.title for node in nodes}
        name_mappping = {node_id: _name_task(name_mappping[node_id]) for node_id in chain.from_iterable(grouped_dag) }

        node_map = {
            node.id: {
                SETTINGS.template_settings.properties_name: node.properties,
                SETTINGS.template_settings.requested_nodes_name: [
                    name_mappping[linkage[input.link][0]]
                    for input in node.inputs if input.link 
                ] or None,
            }
            for node in nodes
   
        }

        output: list[dict] = []

        _name_group = IncrementalName(SETTINGS.template_settings.default_group_name)

        return [
            {
                _name_group(group): {
                    name_mappping[node_id] : node_map[node_id] for node_id in group
                }     
            }
            for group in grouped_dag
        ]




def format_dag_to_groups(
   g: Dag
):
    return yaml.safe_dump(
        {
        SETTINGS.template_settings.dag_info_name: g.dag_settings.dict(), # type: ignore
        SETTINGS.template_settings.graph_name: _format_to_groups(g.graph),
        })

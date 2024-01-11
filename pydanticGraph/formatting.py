# Formating
from pydantic import BaseModel
from .graph import Graph
import yaml # type: ignore

class Config(BaseModel):
    default_group_name: str = "group"
    default_task_name: str = "task"

CONFIG = Config()


def _format_graph(g: Graph):
    if g.nodes:
        return {
            node.id: {
                "properties": node.properties,
                "title": node.title,
            }
            for node in g.nodes
        }


class IncrementalName:
    def __init__(self, defualt_name):
        self.default_name = defualt_name
        self.default_counter = 0

    def __call__(self, task):
        if getattr(task, "name", None):
            return task.name
        else:
            self.default_counter += 1
            return f"{self.default_name}_{self.default_counter}"

def _format_to_groups(
    grouped_dag: list[list[int]],
    g: Graph,
):
    graph = _format_graph(g)

    _name_group = IncrementalName(CONFIG.default_group_name)
    _name_task = IncrementalName(CONFIG.default_task_name)

    def _node_info(node_id: int):
        node = graph[node_id]
        return (_name_task(node["title"]), node["properties"])

    return [{_name_group(group): dict(map(_node_info, group))} for group in grouped_dag]


class YamlStruct(BaseModel):
    dag_info: dict[str, str]
    groupped_dag: dict[str, dict[str, str]]


def format_to_yaml_groups(
    grouped_dag: list[list[int]],
    g: Graph):
    return yaml.safe_dump(_format_to_groups(grouped_dag,g))
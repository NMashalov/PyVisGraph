from pydantic import BaseModel, create_model
from typing import Optional


class Path(BaseModel):
    relative_path: str
    module_name: Optional[str] = None


class Template_config(BaseModel):
    default_group_name: str = "group"
    default_task_name: str = "task"
    requested_nodes_name: str = "needs"
    properties_name: str = "properties"
    graph_name: str = "actions"
    dag_info_name: str = "dag"



class Config(BaseModel):
    paths: list[Path] = []
    dag_settings: dict[str, str]
    template_settings: Template_config


SETTINGS = Config(
    paths=[Path(relative_path="test/nodes.py", module_name="basic")],
    dag_settings={
        "dag_name": "MyDag",
        "flavor": "cpu",
        "schedule": "0 * * * *",
    },
    template_settings=Template_config(),
)

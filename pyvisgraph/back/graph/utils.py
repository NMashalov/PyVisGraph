import networkx as nx
import collections
from .base import Node, Group, graph_manager

class Namer:
    """
    Deduplicate names in graph
    """

    def __init__(self, atlas: nx.DiGraph):
        self.name_counter: collections.defaultdict[str, int] = collections.defaultdict(
            lambda: 0
        )
        self.atlas = atlas

        self.group_name = graph_manager.cfg.group_name


    def __del__(self):
        for _, state in self.atlas.nodes(data=True):
            del state["name"]


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
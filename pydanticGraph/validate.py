from .scan import _NODE_MODELS
from .graph import (
    Graph,
)


def validate_graph(g: Graph):
    if g.nodes:
        for node in g.nodes:
            props = node.properties
            hash_key = props.pop("hash")
            if props:
                _NODE_MODELS[hash_key](**props)  # type: ignore

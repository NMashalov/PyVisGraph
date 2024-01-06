import importlib
import sys 
import os 
import inspect
from .node import model_to_node, Node
from typing import Optional
NODES: set[Optional[Node]] = set()

def load_custom_node(module_path, ignore=set()):
    """
    Load custom nodes to NODES VAR

    """
    module_name = os.path.basename(module_path)
    try: 
        if os.path.isfile(module_path):
            sp = os.path.splitext(module_path)
            module_name = sp[0]
            module_spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(module)

            global NODES
            # add nodes to scope
            NODES |= {
                model_to_node(cls) for cls in inspect.getmembers(module, inspect.isclass)
            }
    except Exception as e:
        print(f"Cannot import {module_path} module for custom nodes:", e)


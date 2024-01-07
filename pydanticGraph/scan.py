import importlib
import sys 
import os 
import inspect
from .node import model_to_node, Node
from typing import Optional
from pydantic import BaseModel
from pathlib import Path

NODES: list[Optional[Node]] = []

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
            def _check_defined_pydantic(x):
                return inspect.isclass(x) and issubclass(x, BaseModel) and x.__module__ == module_name
                
            NEW_NODES = [
                model_to_node(*cls) for cls in inspect.getmembers(module, _check_defined_pydantic) 
            ]

            NODES.extend(NEW_NODES)
            return NEW_NODES
    except Exception as e:
        print(f"Cannot import {module_path} module for custom nodes:", e)


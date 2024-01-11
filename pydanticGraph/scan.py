import importlib
import sys
import os
import inspect
from .node import model_to_node, Node
from typing import Optional
from pydantic import BaseModel
from pathlib import Path
from types import ModuleType
from fastapi import UploadFile

_NODE_MODELS: dict[str, BaseModel] = {}


def load_nodes_from_module(module: ModuleType, module_name: str):
    # add nodes to scope
    global _NODE_MODELS

    def _check_defined_pydantic(x):
        return (
            inspect.isclass(x)
            and issubclass(x, BaseModel)
            and x.__module__ == module_name
        )

    new_nodes = []
    for cls in inspect.getmembers(module, _check_defined_pydantic):
        new_node = model_to_node(*cls)
        new_nodes.append(new_node)
        _NODE_MODELS[new_node.hash] = cls[1]
    return {"nodes": new_nodes, "module_name": module_name}


async def load_nodes_from_file(file: UploadFile):
    contents = file.file.read().decode("UTF-8")
    name = file.filename or ""
    # creates new module
    module = ModuleType(name)
    # populate the module with code
    exec(contents, module.__dict__)
    return load_nodes_from_module(module, name)


def load_nodes_from_local(module_path: Path, module_name: Optional[str] = None):
    """
    Load custom nodes to NODES VAR
    """
    try:
        if os.path.isfile(module_path):
            sp = os.path.splitext(module_path)
            module_name = module_name or sp[0]
            module_spec = importlib.util.spec_from_file_location(
                module_name, module_path
            )
            if module_spec and module_spec.loader:
                module = importlib.util.module_from_spec(module_spec)
                module_spec.loader.exec_module(module)
                return load_nodes_from_module(module, module_name)
    except Exception as e:
        print(f"Cannot import {module_path} module for custom nodes:", e)

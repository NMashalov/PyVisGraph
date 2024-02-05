# Formating
from pydantic import BaseModel
from pyvisgraph import Graph, Dag, WrongGraphException, SETTINGS
import yaml  # type: ignore

from itertools import chain



links_ref = """
Node can have multiple inputs and outputs.

Output of node can be used in multiple other nodes. One-to-Many
Input, conversely, only handle one connection. Many-to-one

Serialize pydantic model to JSON
and sends to frontend to
Output consist of:
- inputs
    - name
    - type
- outputs
    - name
    - type

should have modifiable
"""






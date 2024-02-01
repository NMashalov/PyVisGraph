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

"""
Note than fields of different types can not be connected!
Example:
---
from pydantic import BaseModel
from typing import ClassVar
class MyNode(Base):
    INPUTS : ClassVar = [
        Link(
            name = 'Data',
            type= 'csv'
        ),
        Link(
            name = 'Model',
            type= 'csv'
        ),
    ]
    OUTPUT : ClassVar = [
        Link(
            name = 'Scores',
            type= 'csv'
        ),
    ]
"""




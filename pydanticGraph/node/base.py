from pydantic import BaseModel, Field
from pydantic._internal._model_construction import ModelMetaclass
from abc import abstractmethod
from typing import Optional
import logging

links_ref = """
Node can have multiple inputs and outputs.

Output of node can be used in multiple other nodes. One-to-Many
Input, conversely, only handle one connection. Many-to-one
"""

class Link(BaseModel):
    name: str 
    type: str 

class Property(BaseModel):
    type: str
    default_value: Optional[str] = None
 
class Node(BaseModel):
    name: str
    input: Optional[list[Link]] = None
    output: Optional[list[Link]] = None
    helper: Optional[str] = None
    properties: Optional[dict[str,Property]] = None


def model_to_node(name: str,model: BaseModel):
    """
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

    print(model)

    return Node(
        name = name,
        input = getattr(model,'INPUTS',None),
        output = getattr(model,'OUTPUTS',None),
         # model.model_fields don't contain fields of ClassVar
        properties={
            field_name: Property(
                
                type = str(field_info.annotation),
                default_value=str(field_info.default or 0)
            )
            for field_name,field_info in model.model_fields.items()
        },
        # put docstring to helper
        helper=model.__doc__
    )















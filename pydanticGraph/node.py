from pydantic import BaseModel, Field
from abc import abstractmethod
from typing import Optional
import logging
from pydantic_core._pydantic_core import PydanticUndefinedType

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
    description: Optional[str] = None


class Node(BaseModel):
    name: str
    hash: str
    properties: dict[str, Property]
    input: Optional[list[Link]] = None
    output: Optional[list[Link]] = None
    helper: Optional[str] = None


# you may add default properties to node
DEFAULT_PROPERTIES: dict[str, Property] = {
    # 'NAME': Property(
    #     type=str(str),
    #     default_value='Enter Name',
    # )
}


def model_to_node(name: str, model: BaseModel):
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

    get_links = lambda model, attribute_name: [
        Link(name=item[0], type=item[1]) for item in getattr(model, attribute_name, [])
    ]

    # unfortunately without default value
    # pydantic will return internal type PydanticUndefinedType
    # instead of null. I write small func to overcome this
    replace_with_None = lambda x: None if isinstance(x, PydanticUndefinedType) else x

    doc = model.__doc__
    if doc:
        doc = doc.strip()

    return Node(
        name=name,
        hash=str(hash(model)),
        input=get_links(model, "INPUTS"),
        output=get_links(model, "OUTPUTS"),
        # model.model_fields don't contain fields of ClassVar
        properties={
            field_name: Property(
                description=str(field_info.description or ""),
                type=str(field_info.annotation),
                default_value=str(replace_with_None(field_info.default) or ""),
            )
            for field_name, field_info in model.model_fields.items()
        }
        | DEFAULT_PROPERTIES,
        # put docstring to helper
        helper=doc,
    )

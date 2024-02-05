from pydantic import create_model, BaseModel, Field

from typing import ClassVar
from annotated_types import Gt



class UploadCsv(BaseModel):
    OUTPUTS: ClassVar = [
        (
            "Data",
            ".csv",
        )
    ]
    source_name: str = "S3"


class Scoring(BaseModel):
    """
    Node for scoring
    """

    INPUTS: ClassVar = [
        ("Data", ".csv"),
        ("Model", ".pkl"),
    ]
    OUTPUTS: ClassVar = [
        (
            "Score",
            ".csv",
        )
    ]
    threshold: int = Field(description="Score cut off. Below no credit :(")


from pydantic import validate_call
import inspect

class Myop:
    @validate_call
    def __init__(self,
                 m: int| None,
                 c: str = '100'):
        print('Good' if isinstance(m,int) else 'bad')

sign = inspect.signature(Myop)

from pathlib import Path

file = Path(__file__).parent / 't.py'


contents = file.read_text()
from pyvisgraph.graph.scan import _NODE_MODELS
exec(contents, {})
print(_NODE_MODELS)
        

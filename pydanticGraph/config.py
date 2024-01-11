from pydantic import BaseModel
from typing import Optional

class Path(BaseModel):
    relative_path: str
    module_name: Optional[str] = None

class Config(BaseModel):
    paths: list[Path] = []

SETTING = Config(
    paths=[
        Path(
            relative_path = 'test/nodes.py',
            module_name = 'basic'
        )
    ]
)
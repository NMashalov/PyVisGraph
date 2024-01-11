from pydantic import (
    create_model,
    BaseModel,
    Field
)

from typing import ClassVar
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

{UploadCsv,Scoring}
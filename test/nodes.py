from pydantic import BaseModel, Field
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


class LoadModel(BaseModel):
    OUTPUTS: ClassVar = [
        ("Model", ".pkl"),
    ]
    sink_name: str = "S3"
    bucket: str = "risk_model"


class UploadScoreToDB(BaseModel):
    INPUTS: ClassVar = [
        ("Score", ".csv"),
    ]
    db: str = "Postgres"
    table: str = Field(
        default="scores.credit_card_scores",
        description="!Table should be written with previous schema SCHEMA.TABLE",
    )

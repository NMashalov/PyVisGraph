from pydantic import create_model, BaseModel, Field

from typing import ClassVar


class UploadCsv(BaseModel):
    GROUP = 'Upload'
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
    GROUP = 'Inference'

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


EXPORT_MODELS = {
    'CsvUploader': UploadCsv,
    'Score': Scoring
}

EXPORT_MODULE_NAME = 'BASE_NODES'

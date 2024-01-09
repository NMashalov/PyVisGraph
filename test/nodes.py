from pydantic import BaseModel, Field
from typing import ClassVar
from pydanticGraph import Link

class UploadCsv(BaseModel):
    OUTPUTS : ClassVar = [
        Link(
            name = 'Data',
            type= 'csv' 
        ),
    ]
    source_name:str = 'S3'


class Scoring(BaseModel):
    INPUTS : ClassVar = [
        Link(
            name = 'Data',
            type= 'csv' 
        ),
        Link(
            name = 'Model',
            type= 'pkl' 
        ),
    ]

    OUTPUTS : ClassVar = [
        Link(
            name = 'Scores',
            type= 'csv' 
        ),
    ]
    threshold: int = 0

class UploadScoresDB(BaseModel):
    INPUTS : ClassVar = [
        Link(
            name = 'Scores',
            type= 'csv' 
        ),
    ]
    schema_name:str = 'Client_accepts'

class UploadModel(BaseModel):
    OUTPUTS : ClassVar = [
        Link(
            name = 'Model',
            type= 'pkl' 
        ),
    ]
    sink_name:str = 'S3'
    bucket: str = 'models'
    model_name: str = 'Credit_Cards'


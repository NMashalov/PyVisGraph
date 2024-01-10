from pydantic import BaseModel, Field
from typing import ClassVar

class ReadKafka(BaseModel):
    OUTPUTS:  ClassVar =  [
        ('Message','Avro') 
    ]


class FilterByHeader(BaseModel):
    INPUTS : ClassVar = [
        ('Message','Avro')
    ]
    OUTPUTS : ClassVar = [
        ('Message','Avro')
    ]
    header: str

class FormCSVByTimeout(BaseModel):
    INPUTS : ClassVar = [
        ('Message','Avro')
    ]
    OUTPUTS : ClassVar = [
        ('Score','.csv',)
    ]
    header: str

class CPDToDB(BaseModel):
    INPUTS : ClassVar = [
        ('Message','Avro')
    ]
    table_name: str
    header: str



from pydantic import BaseModel, Field
from typing import ClassVar
from pydantic_core._pydantic_core import PydanticUndefinedType


class UploadCsv(BaseModel):
    OUTPUTS: ClassVar = [
        (
            "Data",
            ".csv",
        )
    ]
    source_name: str


replace_with_None = lambda x: None if isinstance(x, PydanticUndefinedType) else x
print(
    [
        (
            str(field_info.description or ""),
            str(field_info.annotation or ""),
            str(replace_with_None(field_info.default) or ""),
        )
        for field_name, field_info in UploadCsv.model_fields.items()
    ]
)

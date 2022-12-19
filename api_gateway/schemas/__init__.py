from typing import Any

import pydantic
from pydantic import BaseModel, validator
from pydantic.errors import AnyStrMinLengthError


class NoBlankStrBaseModel(BaseModel):
    @validator("*", pre=True)
    def forbid_blank_str(cls, value: Any, values: dict[str, Any]) -> Any:
        if isinstance(value, str) and value == "":
            raise AnyStrMinLengthError(limit_value=1)
        return value


pydantic.BaseModel = NoBlankStrBaseModel

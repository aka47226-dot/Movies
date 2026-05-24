from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator, ValidationError


class RolesEnum(str, Enum):
    user = "USER"
    admin = "ADMIN"
    superadmin = "SUPERADMIN"

class User(BaseModel):
    email: str
    fullName: str
    password: str = Field (..., min_length=8)
    passwordRepeat: str = Field (..., min_length=8)
    roles: RolesEnum
    banned: Optional[bool] = None
    verified: Optional[bool] = None

    @field_validator("email")
    @classmethod
    def check_email(cls, value: str) -> str:
        if "@" in value:
            return value
        else:
            raise ValueError("Invalid email address")
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Literal
from uuid import UUID
import re
class CredenciaisLogin(BaseModel):
    email: EmailStr
    senha: str

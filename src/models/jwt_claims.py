from enum import StrEnum

from more_itertools.recipes import is_prime
from pydantic import BaseModel, field_validator, model_validator, Field


class Role(StrEnum):
    Admin = "Admin"
    Member = "Member"
    External = "External"


class JWTClaims(BaseModel):
    role: Role
    seed: str
    name: str = Field(max_length=256)

    @model_validator(mode="before")
    def check_claims(cls, values):
        if len(values) != 3:
            raise ValueError(f"Only 3 claims are allowed, {len(values)} were submitted")
        return values

    @field_validator("name")
    def check_name(cls, value):
        if any(char.isdigit() for char in value):
            raise ValueError(f"Name cannot {value} contain numeric characters")
        return value

    @field_validator("seed")
    def check_seed(cls, value):
        if not is_prime(int(value)):
            raise ValueError(f"Seed {value} must be a prime number")
        return value

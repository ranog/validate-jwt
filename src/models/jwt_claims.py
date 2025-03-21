from enum import StrEnum
from more_itertools.recipes import is_prime
from pydantic import BaseModel, Field, field_validator, model_validator


class Role(StrEnum):
    Admin = "Admin"
    Member = "Member"
    External = "External"


class JWTClaims(BaseModel):
    role: Role
    seed: str
    name: str = Field(max_length=256)

    @model_validator(mode="before")
    def validate_exactly_three_claims(cls, values: dict) -> dict:
        if len(values) != 3:
            raise ValueError(f"Only 3 claims are allowed, {len(values)} were submitted")
        return values

    @field_validator("name")
    def validate_name_does_not_contain_digits(cls, value: str) -> str:
        if any(char.isdigit() for char in value):
            raise ValueError(f"Name cannot {value} contain numeric characters")
        return value

    @field_validator("seed")
    def validate_seed_is_prime_number(cls, value: str) -> str:
        if not is_prime(int(value)):
            raise ValueError(f"Seed {value} must be a prime number")
        return value

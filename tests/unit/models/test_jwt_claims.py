import pytest
from pydantic import ValidationError

from src.models.jwt_claims import JWTClaims


def test_should_return_jwt_claims_object():
    claims = {
        "role": "Admin",
        "seed": "7841",
        "name": "Toninho Araujo",
    }

    jwt_claims = JWTClaims(**claims)

    assert jwt_claims.role == claims["role"]
    assert jwt_claims.seed == claims["seed"]
    assert jwt_claims.name == claims["name"]


def test_should_only_contain_3_claims():
    claims = {
        "role": "Admin",
        "seed": "7841",
        "name": "Toninho Araujo",
        "extra": "extra",
    }

    with pytest.raises(ValidationError) as error:
        JWTClaims(**claims)
    assert "Only 3 claims are allowed, 4 were submitted" in str(error.value)


@pytest.mark.parametrize("claim", ["role", "seed", "name"])
def test_should_raise_exception_when_any_claim_field_is_not_sent(claim):
    claims = {
        "role": "Admin",
        "seed": "72341",
        "name": "Maria Olivia",
    }
    claims.pop(claim)

    with pytest.raises(ValidationError) as error:
        JWTClaims(**claims)
    assert "Only 3 claims are allowed, 2 were submitted" in str(error.value)


def test_should_raise_exception_when_the_claim_is_not_allowed():
    claims = {
        "role": "Admin",
        "mcc": "7841",
        "name": "Toninho Araujo",
    }

    with pytest.raises(ValidationError) as error:
        JWTClaims(**claims)
    assert (
        "1 validation error for JWTClaims\n"
        "seed\n"
        "  Field required [type=missing, input_value={'role': 'Admin', 'mcc': "
        "...name': 'Toninho Araujo'}, input_type=dict]\n"
    ) in str(error.value)


@pytest.mark.parametrize(
    "name",
    [
        "M4ria Olivia",
        "Toninho Arauj0",
        "Valdir Aran7a",
    ],
)
def test_should_raise_exception_when_claim_name_contains_numeric_characters(name):
    claims = {
        "role": "External",
        "seed": "72341",
        "name": name,
    }

    with pytest.raises(ValidationError) as error:
        JWTClaims(**claims)
    assert f"Name cannot {name} contain numeric characters" in str(error.value)


@pytest.mark.parametrize("role", ["Admin", "Member", "External"])
def test_should_accept_valid_role_values(role):
    claims = {
        "role": role,
        "seed": "72341",
        "name": "Maria Olivia",
    }

    jwt_claims = JWTClaims(**claims)

    assert jwt_claims.role == role


def test_should_raise_exception_for_invalid_role_value():
    claims = {
        "role": "Superuser",
        "seed": "72341",
        "name": "Maria Olivia",
    }

    with pytest.raises(ValidationError) as error:
        JWTClaims(**claims)
    assert (
        "1 validation error for JWTClaims\n"
        "role\n"
        "  Input should be 'Admin', 'Member' or 'External' [type=enum, "
        "input_value='Superuser', input_type=str]\n"
    ) in str(error.value)


@pytest.mark.parametrize(
    "seed",
    [
        "2",
        "3",
        "5",
        "7",
        "72341",
        "72353",
    ],
)
def test_should_allow_only_prime_numbers_for_claim_seed(seed):
    claims = {
        "role": "Admin",
        "seed": seed,
        "name": "Maria Olivia",
    }

    jwt_claims = JWTClaims(**claims)

    assert jwt_claims.seed == seed


@pytest.mark.parametrize(
    "seed",
    [
        "1",
        "4",
        "6",
        "72342",
        "72343",
        "72344",
    ],
)
def test_should_raise_exception_when_claim_seed_is_not_prime(seed):
    claims = {
        "role": "Admin",
        "seed": seed,
        "name": "Maria Olivia",
    }

    with pytest.raises(ValidationError) as error:
        JWTClaims(**claims)
    assert f"Seed {seed} must be a prime number" in str(error.value)


def test_should_accept_maximum_of_256_characters_for__claim_name():
    claims = {
        "role": "Admin",
        "seed": "72341",
        "name": "A" * 256,
    }

    jwt_claims = JWTClaims(**claims)

    assert jwt_claims.name == claims["name"]


def test_should_raise_exception_when_claim_name_exceeds_256_characters():
    claims = {
        "role": "Admin",
        "seed": "72341",
        "name": "A" * 257,
    }

    with pytest.raises(ValidationError) as error:
        JWTClaims(**claims)
    assert (
        "1 validation error for JWTClaims\n"
        "name\n"
        "  String should have at most 256 characters [type=string_too_long, "
        "input_value='AAAAAAAAAAAAAAAAAAAAAAAA...AAAAAAAAAAAAAAAAAAAAAAA', "
        "input_type=str]\n"
    ) in str(error.value)


@pytest.mark.parametrize(
    "seed",
    [
        "abc",
        "12a34",
        "!@#456",
        "72 341",
    ],
)
def test_should_raise_exception_when_claim_seed_is_not_numeric(seed):
    claims = {
        "role": "Admin",
        "seed": seed,
        "name": "Maria Olivia",
    }

    with pytest.raises(ValidationError) as error:
        JWTClaims(**claims)
    assert (
        "1 validation error for JWTClaims\n"
        "seed\n"
        f"  Value error, invalid literal for int() with base 10: '{seed}' "
        f"[type=value_error, input_value='{seed}', input_type=str]\n"
    ) in str(error.value)

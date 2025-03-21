import pytest
from pydantic import ValidationError
from src.models.jwt_claims import JWTClaims

VALID_CLAIMS = {
    "role": "Admin",
    "seed": "7841",
    "name": "Toninho Araujo",
}


def test_should_create_jwt_claims_with_valid_data():
    jwt_claims = JWTClaims(**VALID_CLAIMS)

    assert jwt_claims.role == VALID_CLAIMS["role"]
    assert jwt_claims.seed == VALID_CLAIMS["seed"]
    assert jwt_claims.name == VALID_CLAIMS["name"]


def test_should_raise_when_extra_claim_is_provided():
    claims = {**VALID_CLAIMS, "extra": "not_allowed"}

    with pytest.raises(ValidationError) as error:
        JWTClaims(**claims)
    assert "Only 3 claims are allowed, 4 were submitted" in str(error.value)


@pytest.mark.parametrize("missing_field", ["role", "seed", "name"])
def test_should_raise_when_required_field_is_missing(missing_field):
    claims = {**VALID_CLAIMS}
    claims.pop(missing_field)

    with pytest.raises(ValidationError) as error:
        JWTClaims(**claims)
    assert "Only 3 claims are allowed, 2 were submitted" in str(error.value)


def test_should_raise_when_unexpected_field_is_provided():
    claims = {
        "role": "Admin",
        "mcc": "7841",
        "name": "Toninho Araujo",
    }

    with pytest.raises(ValidationError) as error:
        JWTClaims(**claims)
    assert "Field required" in str(error.value)
    assert "seed" in str(error.value)


@pytest.mark.parametrize("invalid_name", ["M4ria Olivia", "Toninho Arauj0", "Valdir Aran7a"])
def test_should_raise_when_name_contains_digits(invalid_name):
    claims = {**VALID_CLAIMS, "name": invalid_name}

    with pytest.raises(ValidationError) as error:
        JWTClaims(**claims)
    assert f"Name cannot {invalid_name} contain numeric characters" in str(error.value)


@pytest.mark.parametrize("valid_role", ["Admin", "Member", "External"])
def test_should_accept_valid_roles(valid_role):
    claims = {**VALID_CLAIMS, "role": valid_role}

    jwt_claims = JWTClaims(**claims)

    assert jwt_claims.role == valid_role


def test_should_raise_when_invalid_role_is_provided():
    claims = {**VALID_CLAIMS, "role": "Superuser"}

    with pytest.raises(ValidationError) as error:
        JWTClaims(**claims)
    assert "Input should be 'Admin', 'Member' or 'External'" in str(error.value)


@pytest.mark.parametrize("valid_prime_seed", ["2", "3", "5", "7", "72341", "72353"])
def test_should_accept_only_prime_numbers_for_seed(valid_prime_seed):
    claims = {**VALID_CLAIMS, "seed": valid_prime_seed}

    jwt_claims = JWTClaims(**claims)

    assert jwt_claims.seed == valid_prime_seed


@pytest.mark.parametrize("non_prime_seed", ["1", "4", "6", "72342", "72343", "72344"])
def test_should_raise_when_seed_is_not_prime(non_prime_seed):
    claims = {**VALID_CLAIMS, "seed": non_prime_seed}

    with pytest.raises(ValidationError) as error:
        JWTClaims(**claims)
    assert f"Seed {non_prime_seed} must be a prime number" in str(error.value)


def test_should_accept_name_with_max_256_characters():
    claims = {**VALID_CLAIMS, "name": "A" * 256}

    jwt_claims = JWTClaims(**claims)

    assert jwt_claims.name == "A" * 256


def test_should_raise_when_name_exceeds_256_characters():
    claims = {**VALID_CLAIMS, "name": "A" * 257}

    with pytest.raises(ValidationError) as error:
        JWTClaims(**claims)
    assert "String should have at most 256 characters" in str(error.value)


@pytest.mark.parametrize("non_numeric_seed", ["abc", "12a34", "!@#456", "72 341"])
def test_should_raise_when_seed_is_not_numeric(non_numeric_seed):
    claims = {**VALID_CLAIMS, "seed": non_numeric_seed}

    with pytest.raises(ValidationError) as error:
        JWTClaims(**claims)
    assert f"invalid literal for int() with base 10: '{non_numeric_seed}'" in str(error.value)

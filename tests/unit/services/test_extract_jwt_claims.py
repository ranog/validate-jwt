import json

import pytest
import base64

from src.services.extract_jwt_claims import extract_jwt_claims


@pytest.mark.parametrize(
    "jwt, expected_result",
    [
        (
            "eyJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiQWRtaW4iLCJTZWVkIjoiNzg0MSIsIk5hbWUiOiJUb25pbmhvIEFyYXVqbyJ9.QY05sIjtrcJnP533kQNk8QXcaleJ1Q01jWY_ZzIZuAg",
            {"role": "Admin", "seed": "7841", "name": "Toninho Araujo"},
        ),
        (
            "eyJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiRXh0ZXJuYWwiLCJTZWVkIjoiODgwMzciLCJOYW1lIjoiTTRyaWEgT2xpdmlhIn0.6YD73XWZYQSSMDf6H0i3-kylz1-TY_Yt6h1cV2Ku-Qs",
            {"role": "External", "seed": "88037", "name": "M4ria Olivia"},
        ),
        (
            "eyJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiTWVtYmVyIiwiT3JnIjoiQlIiLCJTZWVkIjoiMTQ2MjciLCJOYW1lIjoiVmFsZGlyIEFyYW5oYSJ9.cmrXV_Flm5mfdpfNUVopY_I2zeJUy4EZ4i3Fea98zvY",
            {"role": "Member", "org": "BR", "seed": "14627", "name": "Valdir Aranha"},
        ),
    ],
)
def test_should_extract_content_of_jwt(jwt, expected_result):
    result = extract_jwt_claims(jwt)

    assert result == expected_result


def test_should_not_extract_content_of_jwt_claims():
    with pytest.raises(ValueError) as error:
        extract_jwt_claims(
            "eyJhbGciOiJzI1NiJ9.dfsdfsfryJSr2xrIjoiQWRtaW4iLCJTZrkIjoiNzg0MSIsIk5hbrUiOiJUb25pbmhvIEFyYXVqbyJ9.QY05fsdfsIjtrcJnP533kQNk8QXcaleJ1Q01jWY_ZzIZuAg"
        )
    assert str(error.value) == "'utf-8' codec can't decode byte 0xfb in position 1: invalid start byte"


def test_should_raise_when_jwt_does_not_have_three_parts():
    with pytest.raises(ValueError) as error:
        extract_jwt_claims("only_one_part")
    assert "not enough values to unpack" in str(error.value)


def test_should_raise_when_payload_is_not_valid_json():
    invalid_json = base64.urlsafe_b64encode(b"just some text").decode().rstrip("=")
    jwt = f"aaa.{invalid_json}.bbb"

    with pytest.raises(json.JSONDecodeError):
        extract_jwt_claims(jwt)


def test_should_return_empty_dict_when_payload_has_no_claims():
    empty_payload = base64.urlsafe_b64encode(b"{}").decode().rstrip("=")
    jwt = f"aaa.{empty_payload}.bbb"

    result = extract_jwt_claims(jwt)

    assert result == {}

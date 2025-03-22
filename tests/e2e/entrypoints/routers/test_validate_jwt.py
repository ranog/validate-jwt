import pytest

import logging


@pytest.mark.asyncio
async def test_should_return_true_when_passed_valid_jwt(test_client):
    response = test_client.post(
        "/validate-jwt",
        json={
            "jwt": "eyJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiQWRtaW4iLCJTZWVkIjoiNzg0MSIsIk5hbWUiOiJUb25pbmhvIEFyYXVqbyJ9.QY05sIjtrcJnP533kQNk8QXcaleJ1Q01jWY_ZzIZuAg"
        },
    )

    assert response.status_code == 200
    assert response.json() == {"valid": True}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "jwt",
    [
        "eyJhbGciOiJzI1NiJ9.dfsdfsfryJSr2xrIjoiQWRtaW4iLCJTZrkIjoiNzg0MSIsIk5hbrUiOiJUb25pbmhvIEFyYXVqbyJ9.QY05fsdfsIjtrcJnP533kQNk8QXcaleJ1Q01jWY_ZzIZuAg",
        "eyJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiRXh0ZXJuYWwiLCJTZWVkIjoiODgwMzciLCJOYW1lIjoiTTRyaWEgT2xpdmlhIn0.6YD73XWZYQSSMDf6H0i3-kylz1-TY_Yt6h1cV2Ku-Qs",
        "eyJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiTWVtYmVyIiwiT3JnIjoiQlIiLCJTZWVkIjoiMTQ2MjciLCJOYW1lIjoiVmFsZGlyIEFyYW5oYSJ9.cmrXV_Flm5mfdpfNUVopY_I2zeJUy4EZ4i3Fea98zvY",
    ],
)
async def test_should_return_false_when_passed_invalid_jwt(test_client, jwt):
    response = test_client.post("/validate-jwt", json={"jwt": jwt})

    assert response.status_code == 200
    assert response.json() == {"valid": False}


@pytest.mark.asyncio
async def test_should_return_false_when_jwt_is_not_provided(test_client):
    response = test_client.post("/validate-jwt", json={})

    assert response.status_code == 200
    assert response.json() == {"valid": False, "error": "JWT not provided"}


@pytest.mark.asyncio
async def test_should_return_log_message_when_jwt_is_not_provided(test_client, caplog):
    caplog.set_level(logging.WARNING)

    test_client.post("/validate-jwt", json={})

    assert "JWT not provided" in caplog.text


@pytest.mark.asyncio
async def test_should_return_log_message_when_invalid_jwt_is_provided(test_client, caplog):
    caplog.set_level(logging.WARNING)

    test_client.post("/validate-jwt", json={"jwt": "invalid_jwt"})

    assert "Invalid JWT" in caplog.text


@pytest.mark.asyncio
async def test_should_return_log_message_when_jwt_is_provided(test_client, caplog):
    caplog.set_level(logging.INFO)

    test_client.post(
        "/validate-jwt",
        json={
            "jwt": "eyJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiQWRtaW4iLCJTZWVkIjoiNzg0MSIsIk5hbWUiOiJUb25pbmhvIEFyYXVqbyJ9.QY05sIjtrcJnP533kQNk8QXcaleJ1Q01jWY_ZzIZuAg"
        },
    )

    assert (
        "Validating JWT: eyJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiQWRtaW4iLCJTZWVkIjoiNzg0MSIsIk5hbWUiOiJUb25pbmhvIEFyYXVqbyJ9.QY05sIjtrcJnP533kQNk8QXcaleJ1Q01jWY_ZzIZuAg"
        in caplog.text
    )

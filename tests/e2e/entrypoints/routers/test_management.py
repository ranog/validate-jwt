import logging

import pytest

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_should_return_ok_status_when_calling_health_check_endpoint(test_client):
    response = test_client.get("/_health_check")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_should_return_log_message_from_health_check_endpoint(test_client, caplog):
    caplog.set_level(logging.INFO)

    test_client.get("/_health_check")

    assert "Starting Health Check with log_text" in caplog.text

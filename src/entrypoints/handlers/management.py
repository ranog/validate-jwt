import logging

from fastapi import status
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


async def health_check():
    logger.info("Starting Health Check with log_text")
    return JSONResponse(content={"status": "ok"}, status_code=status.HTTP_200_OK)

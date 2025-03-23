import logging
from fastapi import status
from fastapi.responses import JSONResponse

from src.models.jwt_claims import JWTClaims
from src.services.extract_jwt_claims import extract_jwt_claims
from pydantic import ValidationError, BaseModel

logger = logging.getLogger(__name__)


class ValidateJWTRequest(BaseModel):
    jwt: str


async def validate_jwt_handler(validate_jwt_request: ValidateJWTRequest):
    try:
        if not validate_jwt_request.jwt:
            logger.warning("JWT not provided")
            return JSONResponse(content={"valid": False, "error": "JWT not provided"}, status_code=status.HTTP_200_OK)

        logger.info(f"Validating JWT: {validate_jwt_request.jwt}")

        jwt_claims_dict = extract_jwt_claims(validate_jwt_request.jwt)
        JWTClaims(**jwt_claims_dict)

        return JSONResponse(content={"valid": True}, status_code=status.HTTP_200_OK)

    except (ValueError, ValidationError, KeyError) as e:
        logger.warning(f"Invalid JWT: {str(e)}")
        return JSONResponse(content={"valid": False}, status_code=status.HTTP_200_OK)

from fastapi import APIRouter

from src.entrypoints.handlers.validade_jwt import validate_jwt_handler

validate_jwt_router = APIRouter()

validate_jwt_router.add_api_route(
    "/validate-jwt",
    validate_jwt_handler,
    methods=["POST"],
)

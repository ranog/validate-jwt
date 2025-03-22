from fastapi import APIRouter

from src.entrypoints.handlers.management import health_check

management_router = APIRouter()

management_router.add_api_route(
    "/_health_check",
    health_check,
    methods=["GET"],
)

from fastapi import APIRouter

from src.entrypoints.handlers.management import health_check

management_router = APIRouter()

management_router.add_api_route(
    "/health",
    health_check,
    methods=["GET"],
    summary="Health Check",
    description="Verifica se o serviço está online.",
)

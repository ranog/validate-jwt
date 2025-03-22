from src.entrypoints.routers.management import management_router
from src.entrypoints.routers.validade_jwt import validate_jwt_router


def add_routes(app):
    app.include_router(management_router)
    app.include_router(validate_jwt_router)

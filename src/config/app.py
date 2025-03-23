from fastapi import FastAPI

from src.entrypoints import router


def create_app():
    app = FastAPI(
        title="API de Validação de JWT",
        description="Esta API permite validar tokens JWT e monitorar a saúde do serviço.",
        version="1.0.0",
    )

    router.add_routes(app)
    return app

from src.config.app import create_app
from src.entrypoints import router

app = create_app()

router.add_routes(app)

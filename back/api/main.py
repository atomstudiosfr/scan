from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from api import admin
from core.config import SETTINGS
from core.db import ASYNC_ENGINE
from api.views import user_view


def create_app():
    description = """SCAN 🚀"""
    tags_metadata = [
        {
            "name": "User",
            "description": "User ",
        },
    ]
    app = FastAPI(
        title=SETTINGS.PROJECT_NAME,
        version="0.0.1",
        docs_url="/",
        description=description,
        contact={"name": "Larry", "email": "larry@atomstudios.fr"},
        swagger_ui_init_oauth={
            "usePkceWithAuthorizationCodeGrant": True,
        },
        openapi_tags=tags_metadata,
        middleware=[
            Middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
                expose_headers=["*"],
            ),
        ],
    )
    app.include_router(user_view.router)

    admin.add(app, ASYNC_ENGINE)

    Instrumentator(
        should_ignore_untemplated=True,
        should_group_status_codes=False,
        excluded_handlers=["/metrics", "/readiness"],
    ).instrument(app).expose(app)
    return app


if __name__ == "__main__":
    from uvicorn import run

    run("api.main:create_app", host='0.0.0.0', port=5002, reload=True, factory=True)

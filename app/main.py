from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import (
    ai_routes,
    auth_routes,
    habit_routes,
    health,
    payment_routes,
    task_routes,
    user_routes,
    workspace_routes,
)


def create_app() -> FastAPI:
    app = FastAPI(title="HabX", description="HabX API", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth_routes.router)
    app.include_router(ai_routes.router)
    app.include_router(user_routes.router)
    app.include_router(habit_routes.router)
    app.include_router(task_routes.router)
    app.include_router(health.router)
    app.include_router(payment_routes.router)
    app.include_router(workspace_routes.router)
    return app


app = create_app()

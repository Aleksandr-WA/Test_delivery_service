import uvicorn
from api import router as api_router
from core.config import settings
from create_fastapi_app import create_app
from errors.errors import (
    validation_exception_handler,
    http_exception_handler,
    general_exception_handler,
)
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
import sentry_sdk
from prometheus_fastapi_instrumentator import Instrumentator


sentry_sdk.init(
    dsn="https://2b7331da13ca3efa3872e0ff831b4e04@o4507944730361856.ingest.de.sentry.io/4507944744910928",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

main_app = create_app(
    create_custom_static_urls=True,
)

main_app.add_exception_handler(RequestValidationError, validation_exception_handler)
main_app.add_exception_handler(HTTPException, http_exception_handler)
main_app.add_exception_handler(Exception, general_exception_handler)

main_app.include_router(
    api_router,
)

Instrumentator().instrument(main_app).expose(main_app)

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )

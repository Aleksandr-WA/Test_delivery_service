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

main_app = create_app(
    create_custom_static_urls=True,
)

main_app.add_exception_handler(RequestValidationError, validation_exception_handler)
main_app.add_exception_handler(HTTPException, http_exception_handler)
main_app.add_exception_handler(Exception, general_exception_handler)

main_app.include_router(
    api_router,
)

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )

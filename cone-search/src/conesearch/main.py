"""The main application factory for the cone-search service.

Notes
-----
Be aware that, following the normal pattern for FastAPI services, the app is
constructed when this module is loaded and is not deferred until a function is
called.
"""

from importlib.metadata import metadata, version

from fastapi import FastAPI

from .handlers import router

__all__ = ["app", "config"]


app = FastAPI(
    title="cone-search",
    description=metadata("cone-search")["Summary"],
    version=version("cone-search"),
    openapi_url="/cone-search/openapi.json",
    docs_url="/cone-search/docs",
    redoc_url="/cone-search/redoc",
)
"""The main FastAPI application for cone-search."""

# Attach the routers.
app.include_router(router, prefix="/cone-search")

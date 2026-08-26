import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from aws import get_secret
from av_client import AVClient
from config import create_route_map, settings
from gateway import handle_api_gateway_proxy
from http_clients import (
    close_clients,
    create_downstream_clients,
    create_http_client,
)
from logging_config import get_logger, get_transaction_logger


logger = get_logger()


# ------------------------------------------------------------
# Parse ROUTES ONCE.
#
# Same source is used for:
#   1. FastAPI route registration
#   2. Downstream URL object
# ------------------------------------------------------------
ROUTE_MAP = create_route_map(
    routes=settings.routes,
    environment=settings.environment,
    downstream_url_template=settings.downstream_url_template,
)

logger.info(
    "Downstream route map created: %d mappings",
    len(ROUTE_MAP),
)

for route, downstream_url in ROUTE_MAP.items():
    logger.info(
        "DOWNSTREAM MAP | %s -> %s",
        route,
        downstream_url,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup started")

    # --------------------------------------------------------
    # AWS secret before readiness.
    # --------------------------------------------------------
    logger.info(
        "Loading AWS secret: %s",
        settings.aws_secret_name,
    )

    secret = await get_secret(
        secret_name=settings.aws_secret_name,
        region=settings.aws_region,
    )

    client_id = secret["clientId"]
    client_secret = secret["clientSecret"]

    # --------------------------------------------------------
    # Separate AV pools.
    # --------------------------------------------------------
    app.state.av = AVClient(
        auth_client=create_http_client(),
        scan_client=create_http_client(),
        client_id=client_id,
        client_secret=client_secret,
        auth_url=settings.av_auth_url,
        scan_url=settings.av_scan_url,
    )

    # --------------------------------------------------------
    # One downstream pool per origin.
    # --------------------------------------------------------
    app.state.downstream_clients = (
        create_downstream_clients(ROUTE_MAP)
    )

    app.state.route_map = ROUTE_MAP
    app.state.environment = settings.environment
    app.state.s3_bucket = settings.s3_bucket
    app.state.aws_region = settings.aws_region
    app.state.ready = True

    logger.info(
        "FastAPI route count: %d",
        len(ROUTE_MAP),
    )

    logger.info(
        "Downstream HTTPX pool count: %d",
        len(app.state.downstream_clients),
    )

    logger.info("Application startup completed")

    try:
        yield
    finally:
        app.state.ready = False

        logger.info("Application shutdown started")

        await app.state.av.close()

        await close_clients(
            app.state.downstream_clients
        )

        logger.info("Application shutdown completed")


app = FastAPI(
    title="AV Scan Service",
    lifespan=lifespan,
)


# ------------------------------------------------------------
# Dynamic FastAPI route registration.
# ------------------------------------------------------------
for route in ROUTE_MAP:
    app.add_api_route(
        route,
        handle_api_gateway_proxy,
        methods=["POST"],
    )

    logger.info(
        "FASTAPI ROUTE REGISTERED | POST %s",
        route,
    )


logger.info(
    "Total FastAPI routes registered: %d",
    len(ROUTE_MAP),
)


# ------------------------------------------------------------
# Health
# ------------------------------------------------------------
@app.get("/health/live")
async def liveness():
    return {"status": "UP"}


@app.get("/health/ready")
async def readiness(request: Request):
    if not getattr(
        request.app.state,
        "ready",
        False,
    ):
        return JSONResponse(
            status_code=503,
            content={"status": "NOT_READY"},
        )

    return {"status": "READY"}


# ------------------------------------------------------------
# Global unexpected exception handler.
# ------------------------------------------------------------
@app.exception_handler(Exception)
async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
):
    transaction_id = request.headers.get(
        "x-tps-value-id"
    )

    request_logger = get_transaction_logger(
        transaction_id
    )

    request_logger.exception(
        "Unhandled exception | method=%s path=%s",
        request.method,
        request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={
            "status": "ERROR",
            "message": "Internal server error",
            "transaction_id": transaction_id,
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )

import time
from pathlib import Path
from urllib.parse import urlsplit

import httpx
from fastapi import File, HTTPException, Request, UploadFile

from aws import upload_s3
from http_clients import get_origin
from logging_config import get_transaction_logger


HOP_BY_HOP_HEADERS = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailer",
    "transfer-encoding",
    "upgrade",
    "host",
    "content-length",
    "content-type",
}


async def handle_api_gateway_proxy(
    request: Request,
    file: UploadFile = File(...),
):
    transaction_id = request.headers.get(
        "x-tps-value-id"
    )

    logger = get_transaction_logger(transaction_id)

    request_start = time.perf_counter()
    path = request.url.path

    logger.info(
        "Request received: %s %s",
        request.method,
        path,
    )

    # Exact incoming-path lookup.
    downstream_url = request.app.state.route_map.get(path)

    if not downstream_url:
        logger.error("Route not configured")
        raise HTTPException(
            status_code=404,
            detail="Route not configured",
        )

    if not transaction_id:
        logger.error("Missing x-tps-value-id")
        raise HTTPException(
            status_code=400,
            detail="x-tps-value-id is required",
        )

    filename = Path(
        file.filename or "upload"
    ).name

    # NGINX enforces the 9 MB limit.
    # We keep the application simple and read the accepted file once.
    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(
            status_code=400,
            detail="Empty file",
        )

    # --------------------------------------------------------
    # S3
    # --------------------------------------------------------
    s3_start = time.perf_counter()

    app_type = path.strip("/").split("/", 1)[0]

    s3_key = (
        f"{request.app.state.environment}/"
        f"{app_type}/"
        f"{transaction_id}/"
        f"{filename}"
    )

    try:
        await upload_s3(
            bucket=request.app.state.s3_bucket,
            key=s3_key,
            file_bytes=file_bytes,
            region=request.app.state.aws_region,
        )
    except Exception:
        logger.exception("S3 upload failed")
        raise HTTPException(
            status_code=502,
            detail="S3 upload failed",
        )

    s3_ms = (
        time.perf_counter() - s3_start
    ) * 1000

    logger.info(
        "S3 upload completed: %.2f ms",
        s3_ms,
    )

    # --------------------------------------------------------
    # AV
    # --------------------------------------------------------
    av_start = time.perf_counter()

    try:
        scan_result, scan_headers = (
            await request.app.state.av.scan(
                filename=filename,
                file_bytes=file_bytes,
                transaction_id=transaction_id,
            )
        )
    except httpx.TimeoutException:
        logger.exception("AV timeout")
        raise HTTPException(
            status_code=504,
            detail="AV service timeout",
        )
    except httpx.ConnectError:
        logger.exception("AV connection failed")
        raise HTTPException(
            status_code=502,
            detail="Unable to connect to AV service",
        )
    except httpx.HTTPStatusError as exc:
        logger.exception(
            "AV returned HTTP %s",
            exc.response.status_code,
        )
        raise HTTPException(
            status_code=502,
            detail="AV service error",
        )
    except Exception:
        logger.exception("AV scan failed")
        raise HTTPException(
            status_code=502,
            detail="AV scan failed",
        )

    av_ms = (
        time.perf_counter() - av_start
    ) * 1000

    logger.info(
        "AV scan completed: %.2f ms",
        av_ms,
    )

    # Adapt this to the exact Symantec AV response contract.
    if scan_result.get("status") != "clean":
        logger.info("File rejected by AV")

        return {
            "status": "REJECTED",
            "transaction_id": transaction_id,
            "scan": scan_result,
        }

    # --------------------------------------------------------
    # Downstream HTTPX pool
    # --------------------------------------------------------
    origin = get_origin(downstream_url)

    client = (
        request.app.state.downstream_clients.get(origin)
    )

    if client is None:
        logger.error(
            "No HTTPX client for downstream origin: %s",
            origin,
        )
        raise HTTPException(
            status_code=500,
            detail="Downstream HTTP client not configured",
        )

    parsed = urlsplit(downstream_url)

    downstream_path = parsed.path

    if parsed.query:
        downstream_path += f"?{parsed.query}"

    logger.info(
        "Downstream selected: %s",
        downstream_url,
    )

    # --------------------------------------------------------
    # Headers
    # --------------------------------------------------------
    headers: dict[str, str] = {}

    for key, value in request.headers.items():
        if key.lower() not in HOP_BY_HOP_HEADERS:
            headers[key] = value

    # Always preserve transaction ID.
    headers["x-tps-value-id"] = transaction_id

    # Forward relevant AV response headers.
    for key, value in scan_headers.items():
        if key.lower() not in HOP_BY_HOP_HEADERS:
            headers[key] = value

    # --------------------------------------------------------
    # Other multipart form fields
    # --------------------------------------------------------
    form = await request.form()

    data = {
        key: value
        for key, value in form.multi_items()
        if not isinstance(value, UploadFile)
    }

    # --------------------------------------------------------
    # Downstream request
    # --------------------------------------------------------
    downstream_start = time.perf_counter()

    try:
        response = await client.post(
            downstream_path,
            headers=headers,
            files={
                "file": (
                    filename,
                    file_bytes,
                    file.content_type
                    or "application/octet-stream",
                )
            },
            data=data,
        )

        response.raise_for_status()

    except httpx.TimeoutException:
        logger.exception("Downstream timeout")
        raise HTTPException(
            status_code=504,
            detail="Downstream service timeout",
        )

    except httpx.ConnectError:
        logger.exception("Downstream connection failed")
        raise HTTPException(
            status_code=502,
            detail="Unable to connect to downstream service",
        )

    except httpx.HTTPStatusError as exc:
        logger.exception(
            "Downstream returned HTTP %s",
            exc.response.status_code,
        )
        raise HTTPException(
            status_code=502,
            detail="Downstream service error",
        )

    except Exception:
        logger.exception("Downstream request failed")
        raise HTTPException(
            status_code=502,
            detail="Downstream request failed",
        )

    downstream_ms = (
        time.perf_counter() - downstream_start
    ) * 1000

    total_ms = (
        time.perf_counter() - request_start
    ) * 1000

    logger.info(
        "Request completed: downstream_status=%s "
        "s3_ms=%.2f av_ms=%.2f downstream_ms=%.2f total_ms=%.2f",
        response.status_code,
        s3_ms,
        av_ms,
        downstream_ms,
        total_ms,
    )

    return response.json()

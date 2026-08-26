from urllib.parse import urlsplit

import httpx

from config import settings


def get_origin(url: str) -> str:
    parsed = urlsplit(url)
    return f"{parsed.scheme}://{parsed.netloc}"


def create_http_client(
    base_url: str | None = None,
) -> httpx.AsyncClient:
    return httpx.AsyncClient(
        base_url=base_url,
        timeout=httpx.Timeout(
            connect=settings.http_connect_timeout,
            read=settings.http_read_timeout,
            write=settings.http_write_timeout,
            pool=settings.http_pool_timeout,
        ),
        limits=httpx.Limits(
            max_connections=settings.max_connections,
            max_keepalive_connections=settings.max_keepalive_connections,
            keepalive_expiry=settings.keepalive_expiry,
        ),
        follow_redirects=False,
    )


def create_downstream_clients(
    route_map: dict[str, str],
) -> dict[str, httpx.AsyncClient]:
    """
    One AsyncClient/pool per downstream origin.

    Multiple APIs belonging to the same service reuse one pool.
    """
    clients: dict[str, httpx.AsyncClient] = {}

    for downstream_url in route_map.values():
        origin = get_origin(downstream_url)

        if origin not in clients:
            clients[origin] = create_http_client(origin)

    return clients


async def close_clients(
    clients: dict[str, httpx.AsyncClient],
) -> None:
    for client in clients.values():
        await client.aclose()

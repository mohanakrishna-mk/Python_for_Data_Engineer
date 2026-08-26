from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    environment: str

    aws_region: str
    aws_secret_name: str
    s3_bucket: str

    av_auth_url: str
    av_scan_url: str

    # Comma-separated PUBLIC gateway paths only.
    routes: str

    # Derived downstream URL convention.
    downstream_url_template: str = (
        "http://{service}.namespace-{env}.local:8080{path}"
    )

    http_connect_timeout: float = 5
    http_read_timeout: float = 60
    http_write_timeout: float = 60
    http_pool_timeout: float = 5

    max_connections: int = 50
    max_keepalive_connections: int = 20
    keepalive_expiry: float = 10

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()


def create_route_map(
    routes: str,
    environment: str,
    downstream_url_template: str,
) -> dict[str, str]:
    """
    ROUTES is the single source for:
      1. FastAPI route registration
      2. Downstream URL creation

    Example:
      /secure-messages-svc/secure-message/members/messages/attachments

    becomes:
      http://secure-messages-svc.namespace-prod.local:8080/
      secure-message/members/messages/attachments
    """
    route_map: dict[str, str] = {}

    for raw_route in routes.split(","):
        route = raw_route.strip()

        if not route:
            continue

        if not route.startswith("/"):
            raise ValueError(
                f"Invalid route '{route}': must start with '/'"
            )

        parts = route.strip("/").split("/", 1)

        service = parts[0]

        if not service:
            raise ValueError(
                f"Invalid route '{route}'"
            )

        downstream_path = (
            f"/{parts[1]}"
            if len(parts) == 2
            else "/"
        )

        downstream_url = downstream_url_template.format(
            service=service,
            env=environment,
            path=downstream_path,
        )

        route_map[route] = downstream_url

    return route_map

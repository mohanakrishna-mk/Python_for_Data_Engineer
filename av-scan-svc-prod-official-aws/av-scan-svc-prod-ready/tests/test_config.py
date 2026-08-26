import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from config import create_route_map


def test_route_map():
    routes = (
        "/secure-messages-svc/secure-message/members/messages/attachments,"
        "/user-management-svc/users/upload/rolematrix"
    )

    result = create_route_map(
        routes=routes,
        environment="prod",
        downstream_url_template=(
            "http://{service}.namespace-{env}.local:8080{path}"
        ),
    )

    assert result[
        "/secure-messages-svc/secure-message/members/messages/attachments"
    ] == (
        "http://secure-messages-svc.namespace-prod.local:8080"
        "/secure-message/members/messages/attachments"
    )

    assert result[
        "/user-management-svc/users/upload/rolematrix"
    ] == (
        "http://user-management-svc.namespace-prod.local:8080"
        "/users/upload/rolematrix"
    )

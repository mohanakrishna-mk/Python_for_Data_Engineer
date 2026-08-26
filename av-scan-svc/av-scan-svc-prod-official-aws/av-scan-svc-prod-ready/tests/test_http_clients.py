import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from http_clients import get_origin


def test_get_origin():
    assert get_origin(
        "http://secure-messages-svc.namespace-prod.local:8080/a/b"
    ) == "http://secure-messages-svc.namespace-prod.local:8080"

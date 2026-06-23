import pytest
from starlette.testclient import TestClient

from main import app


@pytest.fixture(autouse=True)
def isolated_connections():
    """Each relay test starts with a clean connection set."""
    from main import connected
    connected.clear()
    yield
    connected.clear()


def test_sender_receives_own_submission():
    with TestClient(app) as client:
        with client.websocket_connect("/ws") as ws:
            payload = {"name": "Alice", "language": "python", "code": "print(1)"}
            ws.send_json(payload)
            assert ws.receive_json() == payload


def test_submission_broadcast_to_all_connected_clients():
    with TestClient(app) as client:
        with (
            client.websocket_connect("/ws") as ws1,
            client.websocket_connect("/ws") as ws2,
        ):
            payload = {"name": "Bob", "language": "java", "code": "System.out.println(42);"}
            ws1.send_json(payload)
            assert ws1.receive_json() == payload
            assert ws2.receive_json() == payload


def test_null_name_relayed_intact():
    with TestClient(app) as client:
        with client.websocket_connect("/ws") as ws:
            payload = {"name": None, "language": "c", "code": "int main() { return 0; }"}
            ws.send_json(payload)
            assert ws.receive_json() == payload


def test_multiple_submissions_relayed_in_order():
    with TestClient(app) as client:
        with (
            client.websocket_connect("/ws") as ws1,
            client.websocket_connect("/ws") as ws2,
        ):
            for i in range(3):
                payload = {"name": "Carol", "language": "rust", "code": f"let x = {i};"}
                ws1.send_json(payload)
                assert ws1.receive_json() == payload
                assert ws2.receive_json() == payload


def test_server_remains_functional_after_client_disconnect():
    with TestClient(app) as client:
        with client.websocket_connect("/ws") as ws1:
            pass  # ws1 disconnects on exit
        with client.websocket_connect("/ws") as ws2:
            payload = {"name": None, "language": "haskell", "code": "main = putStrLn \"hi\""}
            ws2.send_json(payload)
            assert ws2.receive_json() == payload


def test_each_sender_gets_own_broadcast_only_once():
    with TestClient(app) as client:
        with (
            client.websocket_connect("/ws") as ws1,
            client.websocket_connect("/ws") as ws2,
        ):
            payload = {"name": "Dave", "language": "typescript", "code": "const x: number = 1;"}
            ws2.send_json(payload)
            assert ws1.receive_json() == payload
            assert ws2.receive_json() == payload

from __future__ import annotations


def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"BankAI" in response.data


def test_health_route(client):
    response = client.get("/health/")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "ok"

from pathlib import Path

from fastapi.testclient import TestClient

from apps.api.main import app


ROOT = Path(__file__).resolve().parents[2]
client = TestClient(app)


def _read_fixture(name: str) -> str:
    return (ROOT / "tests" / name).read_text(encoding="utf-8")


def test_health_check_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analyze_happy_path_returns_success():
    response = client.post(
        "/analyze",
        json={"source_code": _read_fixture("algorithm_darwin.php")},
    )
    body = response.json()

    assert response.status_code == 200
    assert body["status"] == "success"
    assert len(body["tokens"]) > 0


def test_analyze_semantic_error_fixture():
    response = client.post(
        "/analyze",
        json={"source_code": _read_fixture("algorithm_gabriel.php")},
    )
    body = response.json()

    assert response.status_code == 200
    assert body["status"] == "semantic_error"
    assert any(error["code"] == "SEM_INCOMPATIBLE_ARITHMETIC_TYPES" for error in body["semantic_errors"])


def test_analyze_malformed_syntax_returns_syntax_error():
    malformed = """<?php
if ($edad >= 18 {
    echo "Mayor";
}
?>"""
    response = client.post("/analyze", json={"source_code": malformed})
    body = response.json()

    assert response.status_code == 200
    assert body["status"] == "syntax_error"
    assert len(body["syntactic_errors"]) > 0
    assert body["semantic_skipped"] is True


def test_analyze_without_tokens_returns_empty_tokens():
    response = client.post(
        "/analyze",
        json={
            "source_code": "<?php $x = 10; ?>",
            "include_tokens": False,
        },
    )
    body = response.json()

    assert response.status_code == 200
    assert body["tokens"] == []


def test_analyze_without_tokens_keeps_lexical_errors():
    response = client.post(
        "/analyze",
        json={
            "source_code": "<?php $x = @; ?>",
            "include_tokens": False,
        },
    )
    body = response.json()

    assert response.status_code == 200
    assert body["tokens"] == []
    assert any(error["phase"] == "lexical" for error in body["syntactic_errors"])


def test_analyze_oversized_payload_rejected():
    oversized = "a" * 262145
    response = client.post("/analyze", json={"source_code": oversized})

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert any("supera el límite" in item["msg"] for item in detail)


def test_cors_preflight_allows_configured_origin():
    response = client.options(
        "/analyze",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
        },
    )
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:5173"


def test_cors_preflight_blocks_unknown_origin():
    response = client.options(
        "/analyze",
        headers={
            "Origin": "https://evil.example.com",
            "Access-Control-Request-Method": "POST",
        },
    )
    assert response.status_code == 400
    assert response.headers.get("access-control-allow-origin") is None

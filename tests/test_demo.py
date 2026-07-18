from types import SimpleNamespace

import pytest

from hydra_mlx_context.demo import DemoContextStore, discover_chat_model


def test_demo_store_round_trip() -> None:
    store = DemoContextStore()
    store.persist("Prefer concise answers", source_id="preference")
    recalled = store.recall("How should I answer?")
    assert recalled[0].text == "Prefer concise answers"
    assert store.write_attempts == 1


def test_model_discovery_rejects_non_loopback_before_request() -> None:
    with pytest.raises(ValueError, match="loopback"):
        discover_chat_model("https://api.example.com/v1")


def test_model_discovery_ignores_embedding_models(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "hydra_mlx_context.demo.httpx.get",
        lambda *_, **__: SimpleNamespace(
            raise_for_status=lambda: None,
            json=lambda: {"data": [{"id": "embed-model"}, {"id": "mlx-chat"}]},
        ),
    )
    assert discover_chat_model("http://127.0.0.1:1234/v1") == "mlx-chat"

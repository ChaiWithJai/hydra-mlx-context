from types import SimpleNamespace

import pytest

from hydra_mlx_context.benchmark import score_troubleshooting_context
from hydra_mlx_context.demo import (
    COMPATIBILITY_RUNBOOK,
    DEVICE_PROFILE,
    FAILURE_SIGNAL,
    DemoBackend,
    DemoContextStore,
    discover_chat_model,
    run_demo,
)
from hydra_mlx_context.models import ContextKind


def test_demo_store_round_trip() -> None:
    store = DemoContextStore()
    store.ingest(
        "Prefer concise answers",
        kind=ContextKind.MEMORY,
        source_id="preference",
        infer=False,
    )
    recalled = store.recall("How should I answer?")
    assert recalled[0].text == "Prefer concise answers"
    assert store.write_attempts == 1


def test_fresh_session_recovers_complete_troubleshooting_context() -> None:
    backend = DemoBackend()
    first_session = DemoContextStore(backend)
    first_session.ingest(DEVICE_PROFILE, kind=ContextKind.MEMORY, source_id="device", infer=False)
    first_session.ingest(
        COMPATIBILITY_RUNBOOK,
        kind=ContextKind.KNOWLEDGE,
        source_id="runbook",
        infer=False,
    )
    first_session.ingest(FAILURE_SIGNAL, kind=ContextKind.MEMORY, source_id="failure", infer=True)

    second_session = DemoContextStore(backend)
    result = score_troubleshooting_context(second_session.recall("new process"))

    assert result.score == result.total == 3


def test_denied_content_cannot_be_ingested() -> None:
    store = DemoContextStore()
    with pytest.raises(ValueError, match="Denied"):
        store.ingest("secret", kind=ContextKind.DENY, source_id="bad", infer=False)
    assert store.write_attempts == 0


def test_model_discovery_rejects_non_loopback_before_request() -> None:
    with pytest.raises(ValueError, match="loopback"):
        discover_chat_model("https://api.example.com/v1")


def test_live_mode_requires_key_without_falling_back() -> None:
    with pytest.raises(RuntimeError, match="never fall back"):
        run_demo(base_url="http://127.0.0.1:1234/v1", mode="live", token="")


def test_model_discovery_ignores_embedding_models(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "hydra_mlx_context.demo.httpx.get",
        lambda *_, **__: SimpleNamespace(
            raise_for_status=lambda: None,
            json=lambda: {"data": [{"id": "embed-model"}, {"id": "mlx-chat"}]},
        ),
    )
    assert discover_chat_model("http://127.0.0.1:1234/v1") == "mlx-chat"

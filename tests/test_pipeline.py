from dataclasses import dataclass, field

import pytest

from hydra_mlx_context.models import ContextChunk, ContextKind
from hydra_mlx_context.pipeline import ingest_approved


@dataclass
class SpyStore:
    writes: list[dict[str, object]] = field(default_factory=list)

    def ingest(self, text: str, *, kind: ContextKind, source_id: str, infer: bool) -> object:
        self.writes.append({"text": text, "kind": kind, "source_id": source_id, "infer": infer})
        return object()

    def recall(self, query: str) -> list[ContextChunk]:
        del query
        return []


def test_ingest_approved_classifies_before_calling_store() -> None:
    store = SpyStore()
    decision = ingest_approved(
        "Project README documentation",
        store=store,
        source_id="readme",
    )
    assert decision.kind is ContextKind.KNOWLEDGE
    assert store.writes == [
        {
            "text": "Project README documentation",
            "kind": ContextKind.KNOWLEDGE,
            "source_id": "readme",
            "infer": False,
        }
    ]


def test_ingest_approved_never_calls_store_for_secret() -> None:
    store = SpyStore()
    with pytest.raises(PermissionError, match="credential"):
        ingest_approved("api_key=do-not-send", store=store, source_id="secret")
    assert store.writes == []

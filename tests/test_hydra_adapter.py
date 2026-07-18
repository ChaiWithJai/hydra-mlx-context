import json
from types import SimpleNamespace

from hydra_mlx_context.hydra import HydraV2Store
from hydra_mlx_context.models import ContextKind


def test_recall_maps_v2_chunk_fields() -> None:
    store = object.__new__(HydraV2Store)
    store.database = "db"
    store.collection = "user"
    store.client = SimpleNamespace(
        query=lambda **_: SimpleNamespace(
            data=SimpleNamespace(
                chunks=[
                    SimpleNamespace(
                        chunk_content="Remember this",
                        id="source-1",
                        chunk_uuid="chunk-1",
                        source_title="Preference",
                    )
                ]
            )
        )
    )

    assert store.recall("what?")[0].text == "Remember this"
    assert store.recall("what?")[0].source_id == "source-1"
    assert store.recall("what?")[0].title == "Preference"


def test_memory_ingest_uses_v2_unified_context_contract() -> None:
    calls = []
    store = object.__new__(HydraV2Store)
    store.database = "db"
    store.collection = "user"
    store.client = SimpleNamespace(
        context=SimpleNamespace(ingest=lambda **kwargs: calls.append(kwargs))
    )
    store.ingest(
        "Interaction log: 27B failed",
        kind=ContextKind.MEMORY,
        source_id="failure",
        infer=True,
    )
    assert calls[0]["type"] == "memory"
    assert json.loads(calls[0]["memories"]) == [
        {"id": "failure", "text": "Interaction log: 27B failed", "infer": True}
    ]


def test_knowledge_ingest_uses_v2_unified_context_contract() -> None:
    calls = []
    store = object.__new__(HydraV2Store)
    store.database = "db"
    store.collection = "user"
    store.client = SimpleNamespace(
        context=SimpleNamespace(ingest=lambda **kwargs: calls.append(kwargs))
    )
    store.ingest(
        "MLX sizing documentation",
        kind=ContextKind.KNOWLEDGE,
        source_id="runbook",
        infer=False,
    )
    payload = json.loads(calls[0]["app_knowledge"])[0]
    assert calls[0]["type"] == "knowledge"
    assert payload["id"] == "runbook"
    assert payload["content"] == {"text": "MLX sizing documentation"}


def test_ensure_database_uses_v2_readiness_fields() -> None:
    creates = []
    store = object.__new__(HydraV2Store)
    store.database = "db"
    store.client = SimpleNamespace(
        databases=SimpleNamespace(
            list=lambda: SimpleNamespace(data=SimpleNamespace(databases=["db"])),
            create=lambda **kwargs: creates.append(kwargs),
            status=lambda **_: SimpleNamespace(
                data=SimpleNamespace(
                    infra=SimpleNamespace(
                        scheduler_status=True,
                        graph_status=True,
                        vectorstore_status=SimpleNamespace(knowledge=True, memories=True),
                    )
                )
            ),
        )
    )
    store.ensure_database(timeout_seconds=1)
    assert creates == []


def test_ensure_database_creates_missing_database() -> None:
    creates = []
    store = object.__new__(HydraV2Store)
    store.database = "new-db"
    store.client = SimpleNamespace(
        databases=SimpleNamespace(
            list=lambda: SimpleNamespace(data=SimpleNamespace(databases=[])),
            create=lambda **kwargs: creates.append(kwargs),
            status=lambda **_: SimpleNamespace(
                data=SimpleNamespace(
                    infra=SimpleNamespace(
                        scheduler_status=True,
                        graph_status=True,
                        vectorstore_status=SimpleNamespace(knowledge=True, memories=True),
                    )
                )
            ),
        )
    )
    store.ensure_database(timeout_seconds=1)
    assert creates == [{"database": "new-db"}]


def test_source_statuses_maps_v2_processing_fields() -> None:
    store = object.__new__(HydraV2Store)
    store.database = "db"
    store.collection = "user"
    store.client = SimpleNamespace(
        context=SimpleNamespace(
            status=lambda **_: SimpleNamespace(
                data=SimpleNamespace(
                    statuses=[
                        SimpleNamespace(id="device", indexing_status="completed"),
                        SimpleNamespace(id="runbook", indexing_status="graph_creation"),
                    ]
                )
            )
        )
    )
    assert store.source_statuses(["device", "runbook"]) == {
        "device": "completed",
        "runbook": "graph_creation",
    }

from types import SimpleNamespace

from hydra_mlx_context.hydra import HydraV2Store


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

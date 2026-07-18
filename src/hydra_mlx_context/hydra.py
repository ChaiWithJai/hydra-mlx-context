from __future__ import annotations

import json
import time
from collections.abc import Sequence
from typing import Any

from .models import ContextChunk, ContextKind


class HydraV2Store:
    """Thin adapter over the canonical HydraDB v2 Python SDK surface."""

    def __init__(self, *, token: str, database: str, collection: str) -> None:
        from hydra_db import HydraDB

        self.client = HydraDB(token=token)
        self.database = database
        self.collection = collection

    def ingest(self, text: str, *, kind: ContextKind, source_id: str, infer: bool) -> Any:
        if kind is ContextKind.DENY:
            raise ValueError("Denied content cannot be ingested.")
        if kind is ContextKind.MEMORY:
            return self.client.context.ingest(
                type="memory",
                database=self.database,
                collection=self.collection,
                memories=json.dumps(
                    [{"id": source_id, "text": text, "infer": infer}]
                ),
            )
        return self.client.context.ingest(
            type="knowledge",
            database=self.database,
            collection=self.collection,
            app_knowledge=json.dumps(
                [
                    {
                        "id": source_id,
                        "database": self.database,
                        "collection": self.collection,
                        "title": source_id,
                        "type": "custom",
                        "content": {"text": text},
                    }
                ]
            ),
        )

    def ensure_database(self, *, timeout_seconds: int = 180) -> None:
        listed = self.client.databases.list()
        databases = getattr(listed.data, "databases", None) or []
        if self.database not in databases:
            self.client.databases.create(database=self.database)

        deadline = time.monotonic() + timeout_seconds
        while time.monotonic() < deadline:
            status = self.client.databases.status(database=self.database)
            infra = status.data.infra
            vectors = infra.vectorstore_status
            if (
                infra.scheduler_status
                and infra.graph_status
                and vectors.knowledge
                and vectors.memories
            ):
                return
            time.sleep(3)
        raise TimeoutError(f"Database {self.database!r} was not ready within {timeout_seconds}s")

    def recall(self, query: str) -> Sequence[ContextChunk]:
        response = self.client.query(
            database=self.database,
            collection=self.collection,
            query=query,
            type="all",
            query_by="hybrid",
            mode="thinking",
            max_results=6,
            graph_context=True,
        )
        raw_chunks = getattr(response.data, "chunks", None) or []
        chunks: list[ContextChunk] = []
        for raw in raw_chunks:
            chunks.append(
                ContextChunk(
                    text=_field(raw, "chunk_content", default=""),
                    source_id=_field(raw, "id", "chunk_uuid", default="unknown"),
                    title=_field(raw, "source_title", default="Untitled"),
                )
            )
        return chunks


def _field(value: Any, *names: str, default: str) -> str:
    for name in names:
        if isinstance(value, dict) and value.get(name) is not None:
            return str(value[name])
        candidate = getattr(value, name, None)
        if candidate is not None:
            return str(candidate)
    return default

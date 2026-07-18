from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol, Sequence


class ContextKind(StrEnum):
    MEMORY = "memory"
    KNOWLEDGE = "knowledge"
    DENY = "deny"


@dataclass(frozen=True)
class Classification:
    kind: ContextKind
    reason: str
    infer: bool = False


@dataclass(frozen=True)
class ContextChunk:
    text: str
    source_id: str = "unknown"
    title: str = "Untitled"


class ContextStore(Protocol):
    def recall(self, query: str) -> Sequence[ContextChunk]: ...


class WritableContextStore(ContextStore, Protocol):
    def ingest(self, text: str, *, kind: ContextKind, source_id: str, infer: bool) -> object: ...


class LocalModel(Protocol):
    def complete(self, *, system: str, user: str) -> str: ...

from __future__ import annotations

from .models import (
    Classification,
    ContextChunk,
    ContextKind,
    ContextStore,
    LocalModel,
    WritableContextStore,
)
from .policy import classify
from .prompting import SYSTEM_PROMPT, build_user_prompt


def answer(question: str, *, store: ContextStore, model: LocalModel) -> str:
    chunks = store.recall(question)
    return answer_from_chunks(question, chunks=chunks, model=model)


def answer_from_chunks(question: str, *, chunks: list[ContextChunk], model: LocalModel) -> str:
    return model.complete(system=SYSTEM_PROMPT, user=build_user_prompt(question, chunks))


def ingest_approved(
    text: str,
    *,
    store: WritableContextStore,
    source_id: str,
    requested: ContextKind | None = None,
) -> Classification:
    """Classify first and make denied writes unrepresentable at the adapter boundary."""
    decision = classify(text, requested=requested)
    if decision.kind is ContextKind.DENY:
        raise PermissionError(decision.reason)
    store.ingest(
        text,
        kind=decision.kind,
        source_id=source_id,
        infer=decision.infer,
    )
    return decision

from __future__ import annotations

from .models import ContextStore, LocalModel
from .prompting import SYSTEM_PROMPT, build_user_prompt


def answer(question: str, *, store: ContextStore, model: LocalModel) -> str:
    chunks = store.recall(question)
    return model.complete(system=SYSTEM_PROMPT, user=build_user_prompt(question, chunks))

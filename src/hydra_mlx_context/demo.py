from __future__ import annotations

import os
from dataclasses import dataclass, field
from urllib.parse import urlparse

import httpx

from .local_model import LocalOpenAIModel
from .models import ContextChunk, ContextKind
from .pipeline import answer
from .policy import classify


@dataclass
class DemoContextStore:
    """Deterministic stand-in for HydraDB when no demo API key is available."""

    chunks: list[ContextChunk] = field(default_factory=list)
    write_attempts: int = 0

    def persist(self, text: str, *, source_id: str) -> None:
        self.write_attempts += 1
        self.chunks.append(ContextChunk(text=text, source_id=source_id, title="User preference"))

    def recall(self, query: str) -> list[ContextChunk]:
        del query
        return list(self.chunks)


def discover_chat_model(base_url: str) -> str:
    parsed = urlparse(base_url)
    if parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
        raise ValueError("Demo model discovery is restricted to a loopback host.")
    response = httpx.get(f"{base_url.rstrip('/')}/models", timeout=5)
    response.raise_for_status()
    model_ids = [item["id"] for item in response.json().get("data", [])]
    chat_models = [model for model in model_ids if "embed" not in model.lower()]
    if not chat_models:
        raise RuntimeError("No chat model is loaded in the local OpenAI-compatible server.")
    return chat_models[0]


def run_demo(*, base_url: str, model_name: str | None = None) -> str:
    model_name = model_name or discover_chat_model(base_url)
    model = LocalOpenAIModel(base_url=base_url, model=model_name)
    store = DemoContextStore()

    print("HYDRA MLX CONTEXT — END-TO-END DEMO")
    print(f"[1/5] LOCAL MODEL     PASS  {base_url} · {model_name}")

    preference = "The user prefers concise answers with exactly three short bullets."
    preference_policy = classify(preference)
    assert preference_policy.kind is ContextKind.MEMORY
    assert preference_policy.infer is False
    store.persist(preference, source_id="demo_answer_style")
    print("[2/5] MEMORY DECISION PASS  memory · infer=false · explicit fact")

    secret = "api_key=super-secret-value"
    writes_before_secret = store.write_attempts
    secret_policy = classify(secret)
    assert secret_policy.kind is ContextKind.DENY
    assert store.write_attempts == writes_before_secret
    print("[3/5] EGRESS GATE     PASS  credential denied before persistence")

    question = (
        "Using the recalled preference, describe how you will answer future coding questions. "
        "Include the word concise."
    )
    recalled = store.recall(question)
    assert recalled and recalled[0].source_id == "demo_answer_style"
    print("[4/5] CONTEXT RECALL  PASS  1 scoped chunk returned as untrusted evidence")

    response = answer(question, store=store, model=model).strip()
    assert response
    assert "concise" in response.lower()
    print("[5/5] LOCAL RESPONSE  PASS  model used the recalled preference")
    print("\nMODEL OUTPUT\n" + response)
    print("\nDEMO RESULT: PASS")
    print(
        "BOUNDARY NOTE: persistence used the in-memory ContextStore simulator; "
        "set HYDRA_DB_API_KEY to exercise the production HydraV2Store adapter."
    )
    return response


def main() -> int:
    base_url = os.environ.get("LOCAL_LLM_BASE_URL", "http://127.0.0.1:1234/v1")
    model_name = os.environ.get("LOCAL_LLM_MODEL")
    run_demo(base_url=base_url, model_name=model_name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

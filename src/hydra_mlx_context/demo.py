from __future__ import annotations

import argparse
import os
import time
import uuid
from dataclasses import dataclass, field
from typing import Literal
from urllib.parse import urlparse

import httpx
from dotenv import load_dotenv

from .benchmark import BenchmarkResult, score_troubleshooting_context
from .hydra import HydraV2Store
from .local_model import LocalOpenAIModel
from .models import ContextChunk, ContextKind
from .pipeline import answer_from_chunks, ingest_approved

DemoMode = Literal["simulated", "live"]

DEVICE_PROFILE = (
    "This Mac is an Apple M4 Pro with 24 GB of unified memory and uses the LM Studio MLX "
    "backend for local inference."
)
COMPATIBILITY_RUNBOOK = (
    "LM Studio MLX-VLM compatibility runbook documentation: the batched vision path does not "
    "support KV cache quantization. Disable KV cache quantization before retrying, or use a "
    "compatible non-batched path."
)
FAILURE_SIGNAL = (
    "Interaction log from July 14: an MLX-VLM model failed to load twice on this Mac because "
    "the batched vision path does not support KV cache quantization yet."
)
DEMO_QUERY = (
    "An MLX-VLM model failed to load with KV cache quantization. Should I retry the same "
    "configuration? Use the device profile, compatibility runbook, and prior failure. Cite "
    "the exact M4 Pro, 24 GB, and KV cache facts from recalled context."
)


@dataclass
class DemoBackend:
    chunks: list[ContextChunk] = field(default_factory=list)
    write_attempts: int = 0


@dataclass
class DemoContextStore:
    """Deterministic persistence simulator shared across fresh demo sessions."""

    backend: DemoBackend = field(default_factory=DemoBackend)

    @property
    def write_attempts(self) -> int:
        return self.backend.write_attempts

    def ingest(self, text: str, *, kind: ContextKind, source_id: str, infer: bool) -> ContextChunk:
        if kind is ContextKind.DENY:
            raise ValueError("Denied content cannot be ingested.")
        self.backend.write_attempts += 1
        title = "Memory" if kind is ContextKind.MEMORY else "Knowledge"
        chunk = ContextChunk(
            text=text,
            source_id=source_id,
            title=f"{title} · infer={str(infer).lower()}",
        )
        self.backend.chunks.append(chunk)
        return chunk

    def recall(self, query: str) -> list[ContextChunk]:
        del query
        return list(self.backend.chunks)


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


def _hydra_store(*, token: str, database: str, collection: str) -> HydraV2Store:
    return HydraV2Store(token=token, database=database, collection=collection)


def _recall_until_complete(
    store: DemoContextStore | HydraV2Store,
    *,
    timeout_seconds: int,
) -> tuple[list[ContextChunk], BenchmarkResult]:
    deadline = time.monotonic() + timeout_seconds
    latest_chunks: list[ContextChunk] = []
    latest_result = score_troubleshooting_context([])
    while True:
        latest_chunks = list(store.recall(DEMO_QUERY))
        latest_result = score_troubleshooting_context(latest_chunks)
        if latest_result.score == latest_result.total:
            return latest_chunks, latest_result
        if time.monotonic() >= deadline:
            missing = ", ".join(latest_result.missing)
            raise TimeoutError(f"Context indexing did not expose required facts: {missing}")
        time.sleep(3)


def run_demo(
    *,
    base_url: str,
    model_name: str | None = None,
    mode: DemoMode = "simulated",
    token: str = "",
    database: str = "hydra_mlx_context",
    collection: str = "local_mlx_troubleshooting",
) -> str:
    if mode == "live" and not token:
        raise RuntimeError(
            "Live mode requires HYDRA_DB_API_KEY. It will never fall back to the simulator."
        )

    model_name = model_name or discover_chat_model(base_url)
    model = LocalOpenAIModel(base_url=base_url, model=model_name)
    run_id = uuid.uuid4().hex[:10]
    run_collection = f"{collection}_{run_id}"

    if mode == "live":
        first_session: DemoContextStore | HydraV2Store = _hydra_store(
            token=token, database=database, collection=run_collection
        )
        first_session.ensure_database()
        backend = None
    else:
        backend = DemoBackend()
        first_session = DemoContextStore(backend)

    cold_result = score_troubleshooting_context(first_session.recall(DEMO_QUERY))
    if cold_result.score:
        raise AssertionError("Isolated demo collection was not cold before ingestion")

    print("HYDRA MLX TROUBLESHOOTER — COLD VS LEARNED DEMO")
    print(f"MODE: {mode.upper()}{' · NO FALLBACK' if mode == 'live' else ' · LAB SIMULATOR'}")
    print(f"[1/7] LOCAL MODEL      PASS  {base_url} · {model_name}")
    print(
        f"[2/7] COLD BASELINE    {cold_result.score}/{cold_result.total}  required facts available"
    )

    cases = (
        (DEVICE_PROFILE, ContextKind.MEMORY, False, "device_profile"),
        (COMPATIBILITY_RUNBOOK, ContextKind.KNOWLEDGE, False, "mlx_vlm_runbook"),
        (FAILURE_SIGNAL, ContextKind.MEMORY, True, "load_failure_outcome"),
    )
    for text, expected_kind, expected_infer, label in cases:
        decision = ingest_approved(
            text,
            store=first_session,
            source_id=f"{label}_{run_id}",
            requested=expected_kind,
        )
        assert decision.kind is expected_kind
        assert decision.infer is expected_infer
    print("[3/7] CONTEXT LEARNING PASS  device + runbook + inferred load failure")

    secret = "api_key=super-secret-value"
    writes_before_secret = backend.write_attempts if backend else len(cases)
    try:
        ingest_approved(
            secret,
            store=first_session,
            source_id=f"should_never_write_{run_id}",
        )
    except PermissionError:
        pass
    else:
        raise AssertionError("Credential-shaped content reached the persistence adapter")
    writes_after_secret = backend.write_attempts if backend else len(cases)
    assert writes_after_secret == writes_before_secret
    print("[4/7] EGRESS GATE      PASS  credential denied before persistence")

    if mode == "live":
        second_session: DemoContextStore | HydraV2Store = _hydra_store(
            token=token, database=database, collection=run_collection
        )
        recall_timeout = 150
    else:
        assert backend is not None
        second_session = DemoContextStore(backend)
        recall_timeout = 0

    recalled, warm_result = _recall_until_complete(second_session, timeout_seconds=recall_timeout)
    print(f"[5/7] FRESH SESSION    PASS  recalled {len(recalled)} context chunks")
    print(
        f"[6/7] CONTEXT BENCH    {cold_result.score}/{cold_result.total} → "
        f"{warm_result.score}/{warm_result.total}  "
        f"({', '.join(warm_result.passed)})"
    )

    response = answer_from_chunks(DEMO_QUERY, chunks=recalled, model=model).strip()
    assert response
    normalized = response.lower().replace("‑", "-")
    for required in ("m4 pro", "24 gb", "kv cache"):
        if required not in normalized:
            raise AssertionError(f"Local response did not cite required recalled fact: {required}")
    print("[7/7] LOCAL RESPONSE   PASS  answer cited all three learned facts")
    print("\nMODEL OUTPUT\n" + response)
    print("\nDEMO RESULT: PASS")
    if mode == "live":
        print(
            f"PROVEN LIVE: HydraDB database={database} collection={run_collection}; "
            "fresh client recall; localhost generation; no simulator fallback."
        )
    else:
        print(
            "LAB NOTE: context persistence used the deterministic simulator. "
            "Run ./demo/run.sh --live for competition proof."
        )
    return response


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="hydra-mlx-demo")
    parser.add_argument(
        "--live",
        action="store_true",
        help="Require real HydraDB persistence and fail instead of falling back",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    load_dotenv()
    args = build_parser().parse_args(argv)
    try:
        run_demo(
            base_url=os.environ.get("LOCAL_LLM_BASE_URL", "http://127.0.0.1:1234/v1"),
            model_name=os.environ.get("LOCAL_LLM_MODEL"),
            mode="live" if args.live else "simulated",
            token=os.environ.get("HYDRA_DB_API_KEY", ""),
            database=os.environ.get("HYDRA_DATABASE", "hydra_mlx_context"),
            collection=os.environ.get("HYDRA_COLLECTION", "local_mlx_troubleshooting"),
        )
    except RuntimeError as error:
        raise SystemExit(str(error)) from None
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

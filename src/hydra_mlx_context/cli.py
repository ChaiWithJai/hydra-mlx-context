from __future__ import annotations

import argparse
import os
import uuid

from dotenv import load_dotenv

from .hydra import HydraV2Store
from .local_model import LocalOpenAIModel
from .models import ContextKind
from .pipeline import answer, ingest_approved
from .policy import classify


def _store() -> HydraV2Store:
    token = os.environ.get("HYDRA_DB_API_KEY", "")
    if not token:
        raise SystemExit("HYDRA_DB_API_KEY is required for HydraDB operations.")
    return HydraV2Store(
        token=token,
        database=os.environ.get("HYDRA_DATABASE", "hydra_mlx_context"),
        collection=os.environ.get("HYDRA_COLLECTION", "local_user"),
    )


def _model() -> LocalOpenAIModel:
    return LocalOpenAIModel(
        base_url=os.environ.get("LOCAL_LLM_BASE_URL", "http://127.0.0.1:1234/v1"),
        model=os.environ.get("LOCAL_LLM_MODEL", "local-model"),
        api_key=os.environ.get("LOCAL_LLM_API_KEY", "local"),
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="hydra-mlx")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init", help="Create the HydraDB database and wait for readiness")

    classify_parser = subparsers.add_parser("classify", help="Preview the egress decision")
    classify_parser.add_argument("text")

    remember_parser = subparsers.add_parser("remember", help="Persist approved context")
    remember_parser.add_argument("text")
    remember_parser.add_argument("--kind", choices=["memory", "knowledge"])
    remember_parser.add_argument("--source-id")
    remember_parser.add_argument("--allow-egress", action="store_true")

    ask_parser = subparsers.add_parser("ask", help="Recall context and ask the local model")
    ask_parser.add_argument("question")
    return parser


def main(argv: list[str] | None = None) -> int:
    load_dotenv()
    args = build_parser().parse_args(argv)

    if args.command == "init":
        store = _store()
        store.ensure_database()
        print(f"HydraDB database is ready: {store.database}")
        return 0

    if args.command == "classify":
        result = classify(args.text)
        print(f"kind={result.kind} infer={str(result.infer).lower()} reason={result.reason}")
        return 0

    if args.command == "remember":
        requested = ContextKind(args.kind) if args.kind else None
        result = classify(args.text, requested=requested)
        if result.kind is ContextKind.DENY:
            raise SystemExit(f"Write denied: {result.reason}")
        if not args.allow_egress:
            raise SystemExit(
                f"Would send as {result.kind} (infer={result.infer}). "
                "Re-run with --allow-egress after reviewing the content."
            )
        source_id = args.source_id or f"local_{uuid.uuid4().hex}"
        ingest_approved(
            args.text,
            store=_store(),
            source_id=source_id,
            requested=requested,
        )
        print(f"Accepted for ingestion: {source_id}")
        return 0

    if args.command == "ask":
        print(answer(args.question, store=_store(), model=_model()))
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Iterable, Mapping

from .models import ContextChunk


@dataclass(frozen=True)
class FactRequirement:
    label: str
    keyword_groups: tuple[tuple[str, ...], ...]

    def matches(self, corpus: str) -> bool:
        return all(any(keyword in corpus for keyword in group) for group in self.keyword_groups)


@dataclass(frozen=True)
class BenchmarkResult:
    passed: tuple[str, ...]
    missing: tuple[str, ...]

    @property
    def score(self) -> int:
        return len(self.passed)

    @property
    def total(self) -> int:
        return len(self.passed) + len(self.missing)


TROUBLESHOOTING_REQUIREMENTS = (
    FactRequirement(
        "device profile",
        (("24 gb",), ("m4 pro",)),
    ),
    FactRequirement(
        "compatibility runbook",
        (("kv cache quantization",), ("batched vision", "non-batched")),
    ),
    FactRequirement(
        "prior failure",
        (("failed", "failure"), ("kv cache",)),
    ),
)

TROUBLESHOOTING_PROBES = {
    "device profile": "Which Apple chip and how much unified memory does this user's Mac have?",
    "compatibility runbook": (
        "What does the MLX-VLM compatibility runbook say about batched vision and KV cache "
        "quantization?"
    ),
    "prior failure": (
        "What happened when MLX-VLM was loaded on July 14, and which setting caused it?"
    ),
}


def score_troubleshooting_context(chunks: Iterable[ContextChunk]) -> BenchmarkResult:
    corpus = "\n".join(chunk.text.lower() for chunk in chunks)
    passed = tuple(
        requirement.label
        for requirement in TROUBLESHOOTING_REQUIREMENTS
        if requirement.matches(corpus)
    )
    missing = tuple(
        requirement.label
        for requirement in TROUBLESHOOTING_REQUIREMENTS
        if not requirement.matches(corpus)
    )
    return BenchmarkResult(passed=passed, missing=missing)


def score_troubleshooting_probes(
    results: Mapping[str, Iterable[ContextChunk]],
) -> BenchmarkResult:
    """Score each fact only against its focused retrieval probe."""
    requirements = {requirement.label: requirement for requirement in TROUBLESHOOTING_REQUIREMENTS}
    passed = tuple(
        label
        for label in TROUBLESHOOTING_PROBES
        if requirements[label].matches("\n".join(chunk.text.lower() for chunk in results[label]))
    )
    missing = tuple(label for label in TROUBLESHOOTING_PROBES if label not in passed)
    return BenchmarkResult(passed=passed, missing=missing)

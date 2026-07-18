from __future__ import annotations

import re

from .models import Classification, ContextKind

_SECRET_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\b(?:sk|ghp|github_pat|xox[baprs])[-_][A-Za-z0-9_-]{16,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"(?i)\b(?:api[_ -]?key|password|secret|token)\s*[:=]\s*\S+"),
)

_PRIVATE_MARKERS = (
    "private advisory",
    "confidential",
    "do not share",
    "under nda",
)

_KNOWLEDGE_MARKERS = (
    "documentation",
    "readme",
    "runbook",
    "api reference",
    "project architecture",
)

_RAW_SIGNAL_MARKERS = (
    "conversation:",
    "user:",
    "assistant:",
    "interaction log",
    "keeps asking",
    "repeatedly",
)


def contains_secret(text: str) -> bool:
    return any(pattern.search(text) for pattern in _SECRET_PATTERNS)


def classify(text: str, *, requested: ContextKind | None = None) -> Classification:
    clean = text.strip()
    lowered = clean.lower()

    if not clean:
        return Classification(ContextKind.DENY, "Empty content is not useful context.")
    if contains_secret(clean):
        return Classification(ContextKind.DENY, "Likely credential or secret detected.")
    if any(marker in lowered for marker in _PRIVATE_MARKERS):
        return Classification(ContextKind.DENY, "Private or confidential material stays local.")
    if requested is ContextKind.DENY:
        return Classification(ContextKind.DENY, "Caller explicitly denied egress.")

    if requested in (ContextKind.MEMORY, ContextKind.KNOWLEDGE):
        kind = requested
    elif any(marker in lowered for marker in _KNOWLEDGE_MARKERS):
        kind = ContextKind.KNOWLEDGE
    else:
        kind = ContextKind.MEMORY

    infer = kind is ContextKind.MEMORY and any(marker in lowered for marker in _RAW_SIGNAL_MARKERS)
    reason = (
        "Shared reference material belongs in Knowledge."
        if kind is ContextKind.KNOWLEDGE
        else "User- or session-specific context belongs in Memory."
    )
    if infer:
        reason += " Raw signals require inference to derive a durable memory."
    else:
        reason += " The supplied text is stored verbatim with inference disabled."
    return Classification(kind, reason, infer=infer)

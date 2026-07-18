import pytest

from hydra_mlx_context.models import ContextKind
from hydra_mlx_context.policy import classify, contains_secret


@pytest.mark.parametrize(
    "text",
    [
        "api_key=super-secret-value",
        "-----BEGIN PRIVATE KEY-----\nabc",
        "ghp_abcdefghijklmnopqrstuvwxyz123456",
        "AKIAIOSFODNN7EXAMPLE",
    ],
)
def test_secret_patterns_are_denied(text: str) -> None:
    assert contains_secret(text)
    assert classify(text).kind is ContextKind.DENY


def test_private_advisory_material_is_denied() -> None:
    result = classify("Private advisory: unpublished review notes")
    assert result.kind is ContextKind.DENY


def test_explicit_preference_is_verbatim_memory() -> None:
    result = classify("I prefer concise code reviews")
    assert result.kind is ContextKind.MEMORY
    assert result.infer is False


def test_raw_conversation_uses_inference() -> None:
    result = classify("Conversation: User: can you make that shorter?")
    assert result.kind is ContextKind.MEMORY
    assert result.infer is True


def test_readme_is_knowledge() -> None:
    result = classify("Project README documentation for the public API")
    assert result.kind is ContextKind.KNOWLEDGE
    assert result.infer is False

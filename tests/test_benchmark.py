from hydra_mlx_context.benchmark import score_troubleshooting_context
from hydra_mlx_context.demo import COMPATIBILITY_RUNBOOK, DEVICE_PROFILE, FAILURE_SIGNAL
from hydra_mlx_context.models import ContextChunk


def test_cold_context_scores_zero() -> None:
    result = score_troubleshooting_context([])
    assert result.score == 0
    assert result.total == 3


def test_complete_context_scores_all_required_facts() -> None:
    chunks = [
        ContextChunk(text=DEVICE_PROFILE),
        ContextChunk(text=COMPATIBILITY_RUNBOOK),
        ContextChunk(text=FAILURE_SIGNAL),
    ]
    result = score_troubleshooting_context(chunks)
    assert result.score == result.total == 3
    assert result.missing == ()


def test_partial_context_reports_the_missing_facts() -> None:
    result = score_troubleshooting_context([ContextChunk(text=DEVICE_PROFILE)])
    assert result.passed == ("device profile",)
    assert result.missing == ("compatibility runbook", "prior failure")

from hydra_mlx_context.models import ContextChunk
from hydra_mlx_context.prompting import build_user_prompt, render_context


def test_context_is_bounded_and_labeled_untrusted() -> None:
    chunks = [
        ContextChunk(text="x" * 20, source_id=f"s{i}", title=f"T{i}")
        for i in range(10)
    ]
    rendered = render_context(chunks, max_chunks=2, max_chars_per_chunk=5)
    assert 'trust="untrusted-evidence"' in rendered
    assert rendered.count("<SOURCE ") == 2
    assert "xxxxx" in rendered
    assert "s2" not in rendered


def test_question_is_outside_context_boundary() -> None:
    prompt = build_user_prompt("What next?", [ContextChunk(text="reference")])
    assert prompt.index("</HYDRA_CONTEXT>") < prompt.index("<USER_QUESTION>")


def test_empty_context_is_explicit() -> None:
    assert render_context([]) == '<HYDRA_CONTEXT status="empty" />'

import pytest

from hydra_mlx_context.local_model import LocalOpenAIModel


def test_loopback_urls_are_allowed() -> None:
    LocalOpenAIModel(base_url="http://127.0.0.1:1234/v1", model="test")
    LocalOpenAIModel(base_url="http://localhost:8080/v1", model="test")


def test_cloud_fallback_is_rejected() -> None:
    with pytest.raises(ValueError, match="loopback"):
        LocalOpenAIModel(base_url="https://api.example.com/v1", model="test")

import pytest
from neo_compute.client import NeoCompute, GPU_MODELS

def test_models():
    assert "H100" in GPU_MODELS
    assert "B200" in GPU_MODELS

def test_url_validation():
    with pytest.raises(ValueError):
        NeoCompute("example.com")

def test_gpu_validation():
    with pytest.raises(ValueError):
        NeoCompute("https://example.com").search_offers("BAD_GPU")

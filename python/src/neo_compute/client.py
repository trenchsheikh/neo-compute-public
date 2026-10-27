"""Provider-sourced, read-only Neo Compute API client. No purchasing or wallets."""
from __future__ import annotations
from typing import Any
import httpx

GPU_MODELS = frozenset({"H100","H200","B200","A100","L40S","RTX_4090","RTX_5090","A6000"})

class NeoComputeError(RuntimeError):
    def __init__(self, message: str, status: int):
        super().__init__(message)
        self.status = status

class NeoCompute:
    def __init__(self, base_url: str, timeout: float = 12.0):
        if not base_url.startswith(("https://", "http://")):
            raise ValueError("base_url must be an absolute HTTP(S) URL")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def search_offers(self, gpu: str = "H100") -> dict[str, Any]:
        if gpu not in GPU_MODELS:
            raise ValueError("Unsupported GPU: " + gpu)
        try:
            with httpx.Client(timeout=self.timeout, follow_redirects=False) as client:
                response = client.get(f"{self.base_url}/api/offers", params={"gpu": gpu})
        except httpx.RequestError as exc:
            raise NeoComputeError("Compute API is unreachable", 0) from exc
        if response.status_code >= 400:
            try:
                message = response.json().get("error", "Compute API error")
            except ValueError:
                message = "Compute API error"
            raise NeoComputeError(str(message), response.status_code)
        data = response.json()
        if not isinstance(data, dict) or not isinstance(data.get("offers"), list) or not isinstance(data.get("connected"), bool):
            raise NeoComputeError("Unexpected API response shape", response.status_code)
        return data

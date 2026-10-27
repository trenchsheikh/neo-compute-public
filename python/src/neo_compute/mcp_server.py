"""Local MCP stdio server for read-only GPU discovery.
Run: NEO_COMPUTE_BASE_URL=https://neo-compute.vercel.app neo-compute-mcp
Do not print logs to stdout; MCP reserves stdout for protocol messages.
"""
import os
from .client import NeoCompute, NeoComputeError, GPU_MODELS

def main() -> None:
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:
        raise SystemExit("Install MCP extras: pip install '.[mcp]'") from exc
    mcp = FastMCP("neo-compute")

    @mcp.tool()
    def search_compute(gpu: str = "H100") -> dict:
        """Search provider-reported GPU offers. Read-only; prices are not binding quotes.

        Args:
            gpu: One of H100, H200, B200, A100, L40S, RTX_4090, RTX_5090, A6000.
        Returns:
            Source-linked offers or a clear disconnected provider status.
        """
        if gpu not in GPU_MODELS:
            return {"connected": False, "offers": [], "error": "Unsupported GPU"}
        endpoint = os.getenv("NEO_COMPUTE_BASE_URL", "https://neo-compute.vercel.app")
        try:
            return NeoCompute(endpoint).search_offers(gpu)
        except NeoComputeError as exc:
            return {"connected": False, "offers": [], "error": str(exc), "status": exc.status}

    @mcp.tool()
    def compare_compute(gpu: str = "H100", limit: int = 5) -> dict:
        """Return cheapest available offers in USD per GPU-hour, sorted ascending.

        This is discovery only. Does not reserve, buy or deploy GPU instances.
        """
        data = search_compute(gpu)
        if not data.get("connected"):
            return data
        rank = sorted((o for o in data["offers"] if isinstance(o.get("hourly"), (int, float)) and o["hourly"] >= 0), key=lambda o: o["hourly"])
        return {"connected": True, "gpu":gpu, "offers":rank[:max(1, min(20, limit))], "observedAt":data.get("observedAt"), "unit":"USD/GPU-hour"}

    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()

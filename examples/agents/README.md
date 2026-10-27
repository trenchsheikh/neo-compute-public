# Connect an AI agent to Neo Compute

## MCP (local stdio)

Install from the Python subdirectory:

```bash
cd python
pip install -e '.[mcp]'
```

Example MCP client configuration:

```json
{
  "mcpServers": {
    "neo-compute": {
      "command": "neo-compute-mcp",
      "env": { "NEO_COMPUTE_BASE_URL": "https://neo-compute.vercel.app" }
    }
  }
}
```

This example starts the Neo MCP server as a local process. Your client must support standard MCP stdio transport. Two tools are available: `search_compute` and `compare_compute`. Both are strictly read-only.

## No MCP support? Use HTTP

Any LLM framework or language can call the documented REST endpoint using an HTTP function tool. See the OpenAPI contract in `openapi/neo-compute.yaml`.

## Safety

The server does **not** buy, rent, provision, use wallets or sign transactions. Provider listings may change, and cannot be treated as booked resources. Do not give agents unbounded spend authorizations.

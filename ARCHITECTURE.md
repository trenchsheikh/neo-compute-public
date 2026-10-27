# Architecture and design decisions

## Primary choice: TypeScript + Python + OpenAPI

- **Platform:** TypeScript, React and Node/Vercel. One language across browser UI, serverless adapters and contracts reduces maintenance work for a solo founder.
- **Agent SDK:** Python, because a large proportion of ML and orchestration users work in Python.
- **TypeScript SDK:** Native support for Node and JS agent ecosystems.
- **Universal access:** An OpenAPI 3.1 contract and plain HTTP, allowing Go, Rust, Java, C#, Ruby, PHP and other languages without a bespoke SDK per language.
- **MCP:** A local Python stdio server using the official MCP SDK. It exposes read-only search and comparison tools, and is independent of the frontend framework.
- **EVM:** Future USDC/x402 payment and orchestration adapters are separate bounded domains. Neither an EVM wallet nor a token is required for current discovery.

## Product modules

1. **Discovery:** Provider adapters return offers with source, specification, rates, and timestamp.
2. **Intelligence:** Comparisons and historical series; history needs persistent backing storage and redistribution permission.
3. **Agent access:** MCP tools and REST contracts.
4. **Procurement (future):** Quote reservation, user approval, risk limits, idempotent deploy, billing reconciliation and shutdown.
5. **Onchain payments (future):** x402 challenge, verified USDC settlement and merchant accounting. Never imply a stablecoin payment alone purchases a third-party cloud instance.

## Runtime invariants

No synthetic offers masquerade as live data; disconnected upstream returns an explicit state; all provider tokens stay server-side. Offer prices are per GPU-hour while instance totals must remain distinct. Search never spends funds or provisions instances.

# Neo Compute SDK

**Open-source TypeScript access to GPU compute discovery.** Built for developers, AI agents, tool builders and integration teams.

[Main application](https://github.com/trenchsheikh/neo-compute) · [Product documentation](https://neo-compute-darkbet.vercel.app/docs) · [Issues](https://github.com/trenchsheikh/neo-compute-public/issues)

> **Status:** Early developer release, read-only. This SDK does **not** book GPUs, launch instances, pay stablecoins, sign wallets, or execute derivatives. It is not yet published on npm.

## Why use it?

Instead of teaching every agent to parse a provider's pricing interface, Neo offers a consistent, typed way to discover available GPU offers with source information and hourly pricing.

- Small dependency-free runtime client using native `fetch`.
- Strong TypeScript types for GPUs, offers, and API responses.
- Explicit disconnected-provider states and typed HTTP errors.
- Optional `AbortSignal` to let callers cancel requests.
- No credentials, wallet keys, or payment logic in the SDK.

## Install & build

**Requirements:** Node.js 20+ and npm.

```bash
git clone https://github.com/trenchsheikh/neo-compute-public.git
cd neo-compute-public
npm install
npm run check
npm run build
```

For now, import the compiled client locally or via a workspace reference. **Do not run `npm install @neo-compute/sdk` expecting a published package.**

## Quickstart

```ts
import { NeoCompute } from './dist/index.js';

const neo = new NeoCompute({
  baseUrl: 'https://YOUR-NEO-DEPLOYMENT'
});

const result = await neo.searchOffers({ gpu: 'H100' });

if (!result.connected) {
  console.log('Provider not connected:', result.notice);
} else {
  for (const offer of result.offers) {
    console.log(offer.provider, offer.gpu, offer.hourly, offer.region);
  }
}
```

Replace `YOUR-NEO-DEPLOYMENT` with your deployment domain. This is a **read-only API** call.

## Developer and agent API

### `new NeoCompute({ baseUrl })`

Requires an absolute HTTP(S) URL. Use HTTPS for production deployments.

### `searchOffers({ gpu, signal? })`

```ts
type GPU =
  | 'H100' | 'H200' | 'B200' | 'A100'
  | 'L40S' | 'RTX_4090' | 'RTX_5090' | 'A6000';

interface Offer {
  id: string;
  gpu: string;
  provider: string;
  gpuCount: number;
  hourly: number;         // USD per GPU-hour
  instanceHourly: number; // USD per total instance-hour
  region: string;
  memoryGb: number;       // as reported / normalised from provider
  link: string;
}

interface SearchResponse {
  connected: boolean;
  offers: Offer[];
  observedAt?: string;
  notice?: string;
  error?: string;
}
```

`NeoComputeError` is thrown on unsuccessful HTTP responses and includes `status`. A disconnected provider can instead return HTTP 200 with `connected: false` and an empty offers list—**always check `connected`**.

### Cancellation and errors

```ts
import { NeoCompute, NeoComputeError } from './dist/index.js';

const neo = new NeoCompute({ baseUrl: 'https://YOUR-NEO-DEPLOYMENT' });
const controller = new AbortController();

try {
  const result = await neo.searchOffers({
    gpu: 'B200',
    signal: controller.signal,
  });
  if (!result.connected) {
    console.log('No live data:', result.notice);
  } else {
    console.log(result.offers);
  }
} catch (error) {
  if (error instanceof NeoComputeError) {
    console.error('API returned status', error.status, error.message);
  } else {
    throw error;
  }
}
```

## Integration pattern for AI agents

The SDK can sit behind a tool handler in your own agent system. A safe search tool would:

1. Validate the requested GPU against the supported list.
2. Call `searchOffers` and require `connected === true`.
3. Return source-linked offers with `observedAt` and units.
4. Let the agent rank options according to explicit requirements.
5. **Stop before purchasing or provisioning.** Such actions require a separate, permissioned integration and budget controls that are not included here.

### Example tool result

```json
{
  "connected": false,
  "offers": [],
  "notice": "Add VAST_API_KEY to connect live GPU marketplace offers."
}
```

The example is a disconnected response, **not a simulated market price**.

## HTTP contract

```http
GET /api/offers?gpu=H100
Accept: application/json
```

| Situation | Result |
| --- | --- |
| Successful provider request | HTTP 200, `connected: true`, sourced offers |
| Provider not configured | HTTP 200, `connected: false`, empty offers |
| Unsupported GPU | HTTP 400 |
| Upstream source unavailable | HTTP 502 |
| Wrong HTTP method | HTTP 405 |

The server endpoint resides in the [main app](https://github.com/trenchsheikh/neo-compute/tree/main/api) and currently connects to Vast.ai if its server-side key is configured.

## Security and data quality

- Do not embed provider or wallet secrets in client apps or agent prompts.
- A quoted hourly price is **not** a booking confirmation.
- `hourly` and `instanceHourly` have different meanings; normalise workload quantity before ranking.
- Offers can expire and provider location, specifications, or reliability may vary.
- Respect data licences, provider policies, and rate limits.
- Do not claim x402 settlement or onchain provenance for provider data that originates offchain.

## Project structure

```text
src/index.ts    # Public interfaces, HTTP client, typed error
tsconfig.json   # TypeScript build configuration
package.json    # Package metadata and build scripts
LICENSE         # MIT
```

## Roadmap

Future proposals include multi-provider adapters, historical price queries, an independently documented MCP server, cache and staleness controls, structured quote lifetimes, and x402 USDC access with explicit limits and replay protection. Purchase automation will require provider agreements, quote confirmation, authorised budgets, shutdown procedures, and billing reconciliation.

## Contributing

Issues and PRs are welcome. Keep the API small, precise and backward compatible. Include types and practical usage examples; document response changes and error conditions. Run `npm run check` and `npm run build` before submitting.

## Licence

MIT — see [LICENSE](./LICENSE).

---

**Neo Compute** · Agent-friendly compute discovery, without hidden execution.

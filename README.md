# Neo Compute Public SDK

An open-source, read-only TypeScript SDK for [Neo Compute](https://github.com/trenchsheikh/neo-compute). Not yet published on npm.

## Setup
```bash
npm install
npm run build
```

## Client
```ts
import {NeoCompute} from './dist/index.js';
const neo=new NeoCompute({baseUrl:'https://your-neo-domain.com'});
const {connected,offers}=await neo.searchOffers({gpu:'H100'});
if(connected)console.log(offers);
```

## API
`GET /api/offers?gpu=H100` provides provider-reported offers and observation time, or an explicit disconnected response when backend credentials are unavailable. Supported models: H100, H200, B200, A100, L40S, RTX_4090, RTX_5090, A6000.

## Roadmap
MCP tool server, multi-provider adapters, historical series, x402 USDC payments and safe agent purchase workflows. **Not implemented yet.** No private keys, server credentials, wallet custody or real trade/provisioning code lives in this repository.

## Contribution principles
Normalise GPU-hour units and preserve provider identity. Validate upstream data, respect provider licensing, never invent prices, avoid unintended agent spending and keep secrets off the client.

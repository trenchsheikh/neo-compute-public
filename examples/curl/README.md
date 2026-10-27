# Any-language integration (HTTP)

The canonical API contract is [openapi/neo-compute.yaml](../../openapi/neo-compute.yaml).

```sh
curl --fail-with-body --silent --show-error \
  'https://neo-compute.vercel.app/api/offers?gpu=H100' \
  -H 'Accept: application/json'
```

Agents and applications in Go, Rust, Java, C#, Ruby, PHP and other languages can use their native HTTP clients or an OpenAPI generator. Always inspect `connected` before assuming listings exist, and compare `hourly` (per GPU) separately from `instanceHourly` (per entire instance).

# 6yao.ai API integration

Read this only when the user asks to connect a Skill to 6yao.ai.

## Configuration

Use `SIXYAO_BASE_URL` with default `https://www.6yao.ai`. Read optional authentication from `SIXYAO_API_KEY` and `SIXYAO_ACCESS_TOKEN`. Never print their values.

## Calculation endpoints

| Capability | Method and path | Core request fields |
| --- | --- | --- |
| Liu Yao chart | `POST /api/divination/calculate-hexagram` | `yaos[6]`, `divinationTimestamp`, `timeInfo`, `question` |
| Mei Hua chart | `POST /api/sixya/meihua/calculate` | `method`, then date fields or `numbers`, plus `hour` |
| Qi Men chart | `POST /api/qimen/calculate` | `datetime`, `category`, `panType`, `trueSolarTime`, `longitude` |
| BaZi chart | `POST /api/bazi` | `year`, `month`, `day`, `hour`, `minute`, `sex`, `city`, `istaiyang` |
| Zi Wei chart | `POST /api/ziwei/chart` | `birthInfo` with date, time, gender, calendar and location fields |

Some endpoints require an authenticated account, membership, quota, or a separately issued API key. Treat `401`, `403`, and `429` as expected states and explain the next legitimate step. Do not bypass access controls, scrape private endpoints, or retry payment-required responses.

## Response handling

Keep raw calculation JSON separate from generated prose. Record endpoint, response timestamp, and calculation options. Validate required fields before interpretation. For streaming endpoints, assemble only protocol data events and stop cleanly on an error event.

The website remains the source of truth for currently supported routes. API contracts may evolve; do not hard-code undocumented production credentials or assume every browser route is a public API.

## Helper

Use the dependency-free client when a direct HTTP tool is unavailable:

```bash
python scripts/sixyao_api.py qimen --data '{"datetime":"2026-09-02T10:00:00+08:00","category":"career","longitude":121.47}'
```

It sends only allow-listed calculation requests and reads credentials from the environment. A `401`, `403`, or `429` exit is reported, not bypassed.

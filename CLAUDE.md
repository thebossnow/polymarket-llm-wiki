# CLAUDE.md

Navigation guide for this repository. This is a **read-only knowledge base**, not an application — there is no code to build or run. It is a markdown mirror of <https://docs.polymarket.com/> (173 English pages) used as an LLM reference for the Polymarket APIs.

## How to use this repo

- **Answer questions from these files, not from memory** — Polymarket's API changes; the markdown here is the source of truth as of the capture date in `README.md`.
- **Every file maps to a live URL.** Strip the `.md` and prepend `https://docs.polymarket.com/`. Example: `api-reference/core/get-user-activity.md` → `https://docs.polymarket.com/api-reference/core/get-user-activity`. Cite the live URL when referencing a page.
- **To find a topic:** grep across the tree (e.g. `grep -ri "negRisk" .`), scan `llms.txt` (the machine index with one-line descriptions of every page), read the categorized table of contents in `README.md`, or grep the single-file `llms-full.txt` (every page concatenated — handy for one-shot full-text search).
- Pages are **plain markdown** — the original Mintlify MDX/JSX components (`<Steps>`, `<Tabs>`, `<ParamField>`, etc.) have been stripped out by `scripts/clean_mdx.py`, leaving only headings, prose, tables, and code blocks.

## Where things live

| Path | What's there |
|------|--------------|
| `llms.txt` / `llms-full.txt` | Machine index (one line per page) / every page concatenated into one file for full-text search |
| `index.md`, `quickstart.md`, `polymarket-101.md` | Start here — overview, first API call, core mental model |
| `concepts/` (6) | Foundational concepts: markets/events, positions/tokens, prices/orderbook, order lifecycle, resolution, PUSD |
| `trading/` (25) | How to trade: order placement, `clients/` (L1/L2/public/builder SDK methods), `ctf/` (split/merge/redeem), `orders/`, `bridge/` (deposit/withdraw) |
| `api-reference/` (113) | The REST/WSS API surface — see breakdown below |
| `market-data/` (7) | Fetching markets + websocket channels (market/user/sports) |
| `market-makers/` (7) | MM program: inventory, rebates, liquidity rewards, combos |
| `builders/` (4) | Builder program: API keys, fees, tiers |
| `resources/` (4) | Contracts, error codes, on-chain data, referrals |
| `advanced/` (1) | `neg-risk` (negative-risk / multi-outcome markets) |
| `dev-tooling.md`, `dev-tooling/` | Official Python & TypeScript SDK pointers |

### `api-reference/` map (largest section)

Endpoint docs grouped by domain: `market-data/` (16), `trade/` (12), `markets/` (12), `core/` (10, user positions/activity/leaderboards), `tags/` (7), `rewards/` (7), `relayer/` (6), `events/` (5), `bridge/` (5), `wss/` (4, websocket channels), plus `sports/`, `maker/`, `comments/`, `series/`, `data/`, `builders/`, `combo-markets/`, `search/`, `profiles/`, `rebates/`. Top-level entries: `introduction.md`, `authentication.md` (L1 private-key vs L2 API-key auth), `clients-sdks.md`, `geoblock.md`.

## Common entry points by task

- **"How do I place an order?"** → `quickstart.md`, then `trading/` (order pages) and `trading/clients/`.
- **"How do I authenticate?"** → `api-reference/authentication.md`.
- **"What does the API return for X?"** → search `api-reference/` for the endpoint.
- **"What's a negRisk / combo / CTF token?"** → `concepts/`, `advanced/neg-risk.md`, `trading/ctf/`.
- **Error codes / contract addresses** → `resources/`.

## Maintaining this mirror

Regenerate against the live docs (English only):

```bash
./scripts/build.sh            # pull sitemap (skip /cn/), fetch each page's Mintlify .md endpoint, refresh llms.txt
python scripts/clean_mdx.py   # strip MDX/JSX components from the fetched pages
python scripts/build_llms_full.py   # rebuild llms-full.txt from the cleaned pages
git add -A && git commit -m "refresh docs mirror" && git push
```

`llms-full.txt` is derived from the page files, so **always rebuild it after editing pages** or it drifts out of sync. If page counts shift, update `README.md` and this file's tables.

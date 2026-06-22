# Introduction

> Overview of the Polymarket APIs

The Polymarket API provides programmatic access to the world's largest prediction market. The platform is served by three separate APIs, each handling a different domain.

***

## APIs

- **Gamma API** — **`https://gamma-api.polymarket.com`** Markets, events, tags, series, comments, sports, search, and public profiles. This is the primary API for discovering and browsing market data.

- **Data API** — **`https://data-api.polymarket.com`** User positions, trades, activity, holder data, open interest, leaderboards, and builder analytics.

- **CLOB API** — **`https://clob.polymarket.com`** Orderbook data, pricing, midpoints, spreads, and price history. Also handles order placement, cancellation, and other trading operations. Trading endpoints require [authentication](/api-reference/authentication).

> **Info:** A separate **Bridge API** (`https://bridge.polymarket.com`) handles deposits and withdrawals. Bridges are not handled by Polymarket, it is a proxy of fun.xyz service.

***

## Authentication

The Gamma API and Data API are fully public — no authentication required.

The CLOB API has both public endpoints (orderbook, prices) and authenticated endpoints (order management). See [Authentication](/api-reference/authentication) for details.

***

## Next Steps

- **[Authentication](/api-reference/authentication)** — Learn how to authenticate requests for trading endpoints.

- **[Clients & SDKs](/api-reference/clients-sdks)** — Official TypeScript, Python, and Rust libraries.

# Overview

> Build on the world's largest prediction market. Trade, integrate, and access real-time market data with the Polymarket API.

[🇺🇸 Looking for Polymarket US documentation? Visit US Docs →](https://docs.polymarket.us)

# Polymarket Documentation

Build on the world's largest prediction market. APIs, SDKs, and tools for prediction market developers.

## Developer Quickstart

Make your first API request in minutes. Learn the basics of the Polymarket platform, fetch market data, place orders, and redeem winning positions.

[Get Started →](/quickstart)

```typescript TypeScript
import { ClobClient, Side } from "@polymarket/clob-client-v2";

const client = new ClobClient({ host, chain: chainId, signer, creds });

const order = await client.createAndPostOrder(
  { tokenID, price: 0.50, size: 10, side: Side.BUY },
  { tickSize: "0.01", negRisk: false }
);
```

```python Python
from py_clob_client_v2 import ClobClient, OrderArgs, PartialCreateOrderOptions
from py_clob_client_v2.order_builder.constants import BUY

client = ClobClient(host, key=key, chain_id=chain, creds=creds)
order = client.create_and_post_order(
    OrderArgs(token_id=token_id, price=0.50, size=10, side=BUY),
    options=PartialCreateOrderOptions(tick_size="0.01", neg_risk=False)
)
```

```rust Rust
use polymarket_client_sdk_v2::clob::{Client, Config};
use polymarket_client_sdk_v2::clob::types::Side;
use polymarket_client_sdk_v2::types::dec;

let client = Client::new(host, Config::default())?.authentication_builder(&signer).authenticate().await?;
let order = client.limit_order().token_id(token_id).price(dec!(0.50)).size(dec!(10)).side(Side::Buy).build().await?;
let signed = client.sign(&signer, order).await?;
let response = client.post_order(signed).await?;
```

## Get Familiar with Polymarket

Learn the fundamentals, explore our APIs, and start building on the world's largest prediction market.

- **[Quickstart](/quickstart)** — Set up your environment and make your first API call in minutes.

- **[Core Concepts](/concepts/markets-events)** — Understand markets, events, tokens, and how trading works.

- **[API Reference](/api-reference/introduction)** — Explore REST endpoints, WebSocket streams, and authentication.

- **[SDKs](/api-reference/clients-sdks)** — Official Python, TypeScript, and Rust libraries for faster development.

[![Banner](https://mintcdn.com/polymarket-292d1b1b/FOMte3ewbG-LVy3k/images/banner.png?fit=max&auto=format&n=FOMte3ewbG-LVy3k&q=85&s=d83f2f21e8474e998d8ba0f45810d978)](https://builders.polymarket.com)

- **[Builder Program](https://builders.polymarket.com)** — Build apps on Polymarket and earn rewards for driving volume

- **[Help Desk](https://help.polymarket.com)** — Get support, report issues, and find answers to common questions

- **[Status](https://status.polymarket.com)** — Check API uptime, service health, and incident reports

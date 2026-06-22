# Quickstart

> Fetch a market and place your first order

Get up and running with the Polymarket API in minutes — fetch market data and place your first order.

### Fetch a Market
All data endpoints are public — no API key or authentication needed. Use the markets endpoint to find a market and get its token IDs:

**cURL**
```bash
curl "https://gamma-api.polymarket.com/markets?active=true&closed=false&limit=1"
```

**TypeScript**
```typescript
const response = await fetch(
  "https://gamma-api.polymarket.com/markets?active=true&closed=false&limit=1"
);
const markets = await response.json();

const market = markets[0];
console.log(market.question);
console.log(market.clobTokenIds);
// ["123456...", "789012..."]  — [Yes token ID, No token ID]
```

**Python**
```python
import requests

response = requests.get(
    "https://gamma-api.polymarket.com/markets",
    params={"active": "true", "closed": "false", "limit": 1}
)
markets = response.json()

market = markets[0]
print(market["question"])
print(market["clobTokenIds"])
# ["123456...", "789012..."]  — [Yes token ID, No token ID]
```

**Rust**
```rust
use polymarket_client_sdk_v2::gamma::Client;
use polymarket_client_sdk_v2::gamma::types::request::MarketsRequest;

let client = Client::default();

let request = MarketsRequest::builder()
    .closed(false)
    .limit(1)
    .build();
let markets = client.markets(&request).await?;

let market = &markets[0];
println!("{:?}", market.question);
println!("{:?}", market.clob_token_ids);
// Some(["123456...", "789012..."])  — [Yes token ID, No token ID]
```

Save a token ID from `clobTokenIds` — you'll need it to place an order. The first ID is the Yes token, the second is the No token. See [Fetching Markets](/market-data/fetching-markets) for more strategies like fetching by slug, tag, or event.

### Install the SDK

```bash TypeScript
npm install @polymarket/clob-client-v2 viem
```

```bash Python
pip install py-clob-client-v2
```

```bash Rust
cargo add polymarket_client_sdk_v2 --features gamma,clob
```

### Set Up Your Client
Derive API credentials and initialize the trading client:

**TypeScript**
```typescript
import { ClobClient } from "@polymarket/clob-client-v2";
import { createWalletClient, http } from "viem";
import { privateKeyToAccount } from "viem/accounts";

const HOST = "https://clob.polymarket.com";
const CHAIN_ID = 137; // Polygon mainnet
const account = privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`);
const signer = createWalletClient({ account, transport: http() });

// Derive API credentials (L1 → L2 auth)
const tempClient = new ClobClient({ host: HOST, chain: CHAIN_ID, signer });
const apiCreds = await tempClient.createOrDeriveApiKey();

// Initialize trading client
const client = new ClobClient({
  host: HOST,
  chain: CHAIN_ID,
  signer,
  creds: apiCreds,
  signatureType: 0, // Signature type: 0 = EOA
  funderAddress: account.address, // Funder address
});
```

**Python**
```python
from py_clob_client_v2 import ClobClient
import os

host = "https://clob.polymarket.com"
chain = 137  # Polygon mainnet
private_key = os.getenv("PRIVATE_KEY")

# Derive API credentials (L1 → L2 auth)
temp_client = ClobClient(host, key=private_key, chain_id=chain)
api_creds = temp_client.create_or_derive_api_key()

# Initialize trading client
client = ClobClient(
    host,
    key=private_key,
    chain_id=chain,
    creds=api_creds,
    signature_type=0,  # Signature type: 0 = EOA
    funder="YOUR_WALLET_ADDRESS",  # Funder address
)
```

**Rust**
```rust
use std::str::FromStr;
use polymarket_client_sdk_v2::POLYGON;
use polymarket_client_sdk_v2::auth::{LocalSigner, Signer};
use polymarket_client_sdk_v2::clob::{Client, Config};

let private_key = std::env::var("POLYMARKET_PRIVATE_KEY")?;
let signer = LocalSigner::from_str(&private_key)?
    .with_chain_id(Some(POLYGON));

// Derive API credentials and initialize trading client (L1 → L2 auth)
// Signature type defaults to EOA (0)
let client = Client::new("https://clob.polymarket.com", Config::default())?
    .authentication_builder(&signer)
    .authenticate()
    .await?;
```

> **Note:** This example uses an EOA wallet (signature type `0`) — your wallet pays its own gas. New API users should use deposit wallets with signature type `3`. Existing Proxy and Safe users can keep using signature types `1` and `2`. See [Authentication](/api-reference/authentication) for details on signature types.

> **Warning:** Before trading, your funder address needs **pUSD** (for buying outcome tokens) and **POL** (for gas, if using EOA type `0`).

### Place an Order
Use the `token_id` from Step 1 to place a limit order:

**TypeScript**
```typescript
import { Side, OrderType } from "@polymarket/clob-client-v2";

// Fetch market details to get tick size and neg risk
const market = await client.getMarket("YOUR_CONDITION_ID");
const tickSize = String(market.minimum_tick_size);   // e.g., "0.01"
const negRisk = market.neg_risk;             // e.g., false

const response = await client.createAndPostOrder(
  {
    tokenID: "YOUR_TOKEN_ID", // From Step 1
    price: 0.50,
    size: 10,
    side: Side.BUY,
  },
  {
    tickSize,
    negRisk,
  },
);

console.log("Order ID:", response.orderID);
console.log("Status:", response.status);
```

**Python**
```python
from py_clob_client_v2 import OrderArgs, OrderType, PartialCreateOrderOptions
from py_clob_client_v2.order_builder.constants import BUY

# Fetch market details to get tick size and neg risk
market = client.get_market("YOUR_CONDITION_ID")
tick_size = str(market["minimum_tick_size"])   # e.g., "0.01"
neg_risk = market["neg_risk"]             # e.g., False

response = client.create_and_post_order(
    OrderArgs(
        token_id="YOUR_TOKEN_ID",  # From Step 1
        price=0.50,
        size=10,
        side=BUY,
    ),
    options=PartialCreateOrderOptions(tick_size=tick_size, neg_risk=neg_risk),
    order_type=OrderType.GTC,
)

print("Order ID:", response["orderID"])
print("Status:", response["status"])
```

**Rust**
```rust
use polymarket_client_sdk_v2::clob::types::Side;
use polymarket_client_sdk_v2::types::dec;

// token_id is a U256 — parse from the string returned in Step 1
let token_id = "YOUR_TOKEN_ID".parse()?;

// The Rust SDK auto-fetches tick size, neg risk, and fee rate
// No need to manually look them up — the order builder handles it
let order = client
    .limit_order()
    .token_id(token_id)
    .price(dec!(0.50))
    .size(dec!(10))
    .side(Side::Buy)
    .build()
    .await?;
let signed_order = client.sign(&signer, order).await?;
let response = client.post_order(signed_order).await?;

println!("Order ID: {}", response.order_id);
println!("Status: {:?}", response.status);
```

***

## Next Steps

- **[Authentication](/api-reference/authentication)** — Understand L1/L2 auth, signature types, and API credentials.

- **[Trading Quickstart](/trading/quickstart)** — Detailed trading guide with order management and troubleshooting.

- **[Fetching Markets](/market-data/fetching-markets)** — Strategies for discovering markets by slug, tag, or category.

- **[Core Concepts](/concepts/markets-events)** — Understand markets, events, prices, and positions.

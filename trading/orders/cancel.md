# Cancel Order

> Cancel single, multiple, or all open orders

All cancel endpoints require [L2 authentication](/trading/overview#authentication). The response always includes `canceled` (list of cancelled order IDs) and `not_canceled` (map of order IDs to failure reasons).

***

## Cancel a Single Order

```typescript TypeScript
const resp = await client.cancelOrder("0xb816482a...");
console.log(resp);
// { canceled: ["0xb816482a..."], not_canceled: {} }
```

```python Python
resp = client.cancel(order_id="0xb816482a...")
print(resp)
# {"canceled": ["0xb816482a..."], "not_canceled": {}}
```

```rust Rust
let resp = client.cancel_order("0xb816482a...").await?;
println!("{:?}", resp);
// CancelOrdersResponse { canceled: ["0xb816482a..."], not_canceled: {} }
```

```bash REST
curl -X DELETE "https://clob.polymarket.com/order" \
  -H "Content-Type: application/json" \
  -H "POLY_ADDRESS: ..." \
  -H "POLY_SIGNATURE: ..." \
  -H "POLY_TIMESTAMP: ..." \
  -H "POLY_API_KEY: ..." \
  -H "POLY_PASSPHRASE: ..." \
  -d '{"orderID": "0xb816482a..."}'
```

***

## Cancel Multiple Orders

```typescript TypeScript
const resp = await client.cancelOrders(["0xb816482a...", "0xc927593b..."]);
```

```python Python
resp = client.cancel_orders([
    "0xb816482a...",
    "0xc927593b...",
])
```

```rust Rust
let resp = client.cancel_orders(&["0xb816482a...", "0xc927593b..."]).await?;
```

```bash REST
curl -X DELETE "https://clob.polymarket.com/orders" \
  -H "Content-Type: application/json" \
  -H "POLY_ADDRESS: ..." \
  -H "POLY_SIGNATURE: ..." \
  -H "POLY_TIMESTAMP: ..." \
  -H "POLY_API_KEY: ..." \
  -H "POLY_PASSPHRASE: ..." \
  -d '["0xb816482a...", "0xc927593b..."]'
```

***

## Cancel All Orders

Cancel every open order across all markets:

```typescript TypeScript
const resp = await client.cancelAll();
```

```python Python
resp = client.cancel_all()
```

```rust Rust
let resp = client.cancel_all_orders().await?;
```

```bash REST
curl -X DELETE "https://clob.polymarket.com/cancel-all" \
  -H "POLY_ADDRESS: ..." \
  -H "POLY_SIGNATURE: ..." \
  -H "POLY_TIMESTAMP: ..." \
  -H "POLY_API_KEY: ..." \
  -H "POLY_PASSPHRASE: ..."
```

***

## Cancel by Market

Cancel all orders for a specific market, optionally filtered to a single token. Both `market` and `asset_id` are optional — omit both to cancel all orders.

```typescript TypeScript
const resp = await client.cancelMarketOrders({
  market: "0xbd31dc8a...", // optional: condition ID
  asset_id: "52114319501245...", // optional: specific token
});
```

```python Python
resp = client.cancel_market_orders(
    market="0xbd31dc8a...",
    asset_id="52114319501245...",  # optional
)
```

```rust Rust
use polymarket_client_sdk_v2::clob::types::request::CancelMarketOrderRequest;

let request = CancelMarketOrderRequest::builder()
    .market("0xbd31dc8a...".parse()?)
    .asset_id("52114319501245...".parse()?)
    .build();
let resp = client.cancel_market_orders(&request).await?;
```

```bash REST
curl -X DELETE "https://clob.polymarket.com/cancel-market-orders" \
  -H "Content-Type: application/json" \
  -H "POLY_ADDRESS: ..." \
  -H "POLY_SIGNATURE: ..." \
  -H "POLY_TIMESTAMP: ..." \
  -H "POLY_API_KEY: ..." \
  -H "POLY_PASSPHRASE: ..." \
  -d '{"market": "0xbd31dc8a...", "asset_id": "52114319501245..."}'
```

***

## Querying Orders

### Get a Single Order

```typescript TypeScript
const order = await client.getOrder("0xb816482a...");
console.log(order.status, order.size_matched);
```

```python Python
order = client.get_order("0xb816482a...")
print(order["status"], order["size_matched"])
```

```rust Rust
let order = client.order("0xb816482a...").await?;
println!("{:?} {}", order.status, order.size_matched);
```

### Get Open Orders

Retrieve all open orders, optionally filtered by market or token:

```typescript TypeScript
// All open orders
const orders = await client.getOpenOrders();

// Filtered by market
const marketOrders = await client.getOpenOrders({
  market: "0xbd31dc8a...",
});

// Filtered by token
const tokenOrders = await client.getOpenOrders({
  asset_id: "52114319501245...",
});
```

```python Python
from py_clob_client_v2 import OpenOrderParams

# All open orders
orders = client.get_orders()

# Filtered by market
market_orders = client.get_orders(
    OpenOrderParams(market="0xbd31dc8a...")
)
```

```rust Rust
use polymarket_client_sdk_v2::clob::types::request::OrdersRequest;

// All open orders
let orders = client.orders(&OrdersRequest::default(), None).await?;

// Filtered by market
let request = OrdersRequest::builder()
    .market("0xbd31dc8a...".parse()?)
    .build();
let market_orders = client.orders(&request, None).await?;
```

### OpenOrder Object

| Field              | Type      | Description                                |
| ------------------ | --------- | ------------------------------------------ |
| `id`               | string    | Order ID                                   |
| `status`           | string    | Current order status                       |
| `market`           | string    | Condition ID                               |
| `asset_id`         | string    | Token ID                                   |
| `side`             | string    | `BUY` or `SELL`                            |
| `original_size`    | string    | Size at placement                          |
| `size_matched`     | string    | Amount filled                              |
| `price`            | string    | Limit price                                |
| `outcome`          | string    | Human-readable outcome (e.g., "Yes", "No") |
| `order_type`       | string    | Order type (GTC, GTD, FOK, FAK)            |
| `maker_address`    | string    | Funder address                             |
| `owner`            | string    | API key of the order owner                 |
| `associate_trades` | string\[] | Trade IDs this order has been included in  |
| `expiration`       | string    | Unix expiration timestamp (`0` if none)    |
| `created_at`       | string    | Unix creation timestamp                    |

***

## Trade History

When an order is matched, it creates a trade. Trades progress through these statuses:

| Status      | Terminal | Description                             |
| ----------- | -------- | --------------------------------------- |
| `MATCHED`   | No       | Matched and sent for onchain submission |
| `MINED`     | No       | Mined on the chain, no finality yet     |
| `CONFIRMED` | Yes      | Achieved finality — trade successful    |
| `RETRYING`  | No       | Transaction failed — being retried      |
| `FAILED`    | Yes      | Failed permanently                      |

```typescript TypeScript
// All trades
const trades = await client.getTrades();

// Filtered by market
const marketTrades = await client.getTrades({
  market: "0xbd31dc8a...",
});
```

```python Python
from py_clob_client_v2 import TradeParams

trades = client.get_trades()

market_trades = client.get_trades(
    TradeParams(market="0xbd31dc8a...")
)
```

```rust Rust
use polymarket_client_sdk_v2::clob::types::request::TradesRequest;

// All trades
let trades = client.trades(&TradesRequest::default(), None).await?;

// Filtered by market
let request = TradesRequest::builder()
    .market("0xbd31dc8a...".parse()?)
    .build();
let market_trades = client.trades(&request, None).await?;
```

Additional filter parameters: `id`, `maker_address`, `asset_id`, `before`, `after`.

The Rust SDK uses cursor-based pagination via the `next_cursor` parameter:

```typescript TypeScript
const page = await client.getTradesPaginated({ market: "0xbd31dc8a..." });
console.log(page.trades, page.count); // trades array + total count
```

```python Python
page = client.get_trades_paginated(TradeParams(market="0xbd31dc8a..."))
```

```rust Rust
// First page
let page = client.trades(&request, None).await?;
println!("{} trades, cursor: {}", page.data.len(), page.next_cursor);

// Next page
let page2 = client.trades(&request, Some(page.next_cursor)).await?;
```

### Trade Object

| Field              | Type          | Description                          |
| ------------------ | ------------- | ------------------------------------ |
| `id`               | string        | Trade ID                             |
| `taker_order_id`   | string        | Taker order hash                     |
| `market`           | string        | Condition ID                         |
| `asset_id`         | string        | Token ID                             |
| `side`             | string        | `BUY` or `SELL`                      |
| `size`             | string        | Trade size                           |
| `price`            | string        | Execution price                      |
| `fee_rate_bps`     | string        | Fee rate in basis points             |
| `status`           | string        | Trade status (see table above)       |
| `match_time`       | string        | Unix timestamp when matched          |
| `last_update`      | string        | Unix timestamp of last status change |
| `outcome`          | string        | Human-readable outcome (e.g., "Yes") |
| `maker_address`    | string        | Maker's funder address               |
| `owner`            | string        | API key of the trade owner           |
| `transaction_hash` | string        | Onchain transaction hash             |
| `bucket_index`     | number        | Index for trade reconciliation       |
| `trader_side`      | string        | `TAKER` or `MAKER`                   |
| `maker_orders`     | MakerOrder\[] | Maker orders that filled this trade  |

> **Note:** A single trade can be split across multiple onchain transactions due to gas limits. Use `bucket_index` and `match_time` to reconcile related transactions back to a single logical trade.

***

## Order Scoring

Check if your resting orders are eligible for [maker rebates](/market-makers/maker-rebates) scoring:

```typescript TypeScript
// Single order
const scoring = await client.isOrderScoring({ orderId: "0x..." });

// Multiple orders
const batch = await client.areOrdersScoring({
  orderIds: ["0x...", "0x..."],
});
```

```python Python
from py_clob_client_v2 import OrderScoringParams, OrdersScoringParams

scoring = client.is_order_scoring(
    OrderScoringParams(orderId="0x...")
)

batch = client.are_orders_scoring(
    OrdersScoringParams(orderIds=["0x...", "0x..."])
)
```

```rust Rust
// Single order
let scoring = client.is_order_scoring("0x...").await?;

// Multiple orders
let batch = client.are_orders_scoring(&["0x...", "0x..."]).await?;
```

***

## Next Steps

- **[Order Attribution](/trading/orders/attribution)** — Attribute orders to your builder account for volume credit

- **[Fees](/trading/fees)** — Understand fee structures and maker rebates

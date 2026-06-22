# Builder Methods

> Methods for querying orders and trades attributed to your builder code.

## Overview

Builder attribution in V2 is handled natively through the order struct — you attach your **builder code** (a `bytes32` identifier from your [Builder Profile](https://polymarket.com/settings?tab=builder)) to every order you submit. No separate client configuration is required.

```typescript TypeScript
import { ClobClient } from "@polymarket/clob-client-v2";

const client = new ClobClient({
  host: "https://clob.polymarket.com",
  chain: 137,
  signer,
  creds: apiCreds,
  signatureType,
  funderAddress,
});

// Attach your builder code on every order
const response = await client.createAndPostOrder(
  {
    tokenID: "0x...",
    price: 0.55,
    size: 100,
    side: Side.BUY,
    builderCode: process.env.POLY_BUILDER_CODE!,
  },
  { tickSize: "0.01", negRisk: false },
);
```

```python Python
from py_clob_client_v2 import ClobClient
from py_clob_client_v2 import OrderArgs, PartialCreateOrderOptions
from py_clob_client_v2.order_builder.constants import BUY
import os

client = ClobClient(
    host="https://clob.polymarket.com",
    chain_id=137,
    key=os.getenv("PRIVATE_KEY"),
    creds=creds,
    signature_type=signature_type,
    funder=funder,
)

# Attach your builder code on every order
response = client.create_and_post_order(
    OrderArgs(
        token_id="0x...",
        price=0.55,
        size=100,
        side=BUY,
        builder_code=os.environ["POLY_BUILDER_CODE"],
    ),
    options=PartialCreateOrderOptions(tick_size="0.01", neg_risk=False),
)
```

> **Info:** See [Order Attribution](/trading/orders/attribution) for the full attribution flow.

***

## Methods

***

### getOrder

Get details for a specific order by ID.

```typescript Signature
async getOrder(orderID: string): Promise<OpenOrder>
```

```typescript TypeScript
const order = await client.getOrder("0xb816482a...");
console.log(order);
```

```python Python
order = client.get_order("0xb816482a...")
print(order)
```

***

### getOpenOrders

Get all open orders attributed to your builder code.

```typescript Signature
async getOpenOrders(
  params?: OpenOrderParams,
  only_first_page?: boolean,
): Promise<OpenOrder[]>
```

**Params**

**`id`** `string`
Optional. Filter by order ID.

**`market`** `string`
Optional. Filter by market condition ID.

**`asset_id`** `string`
Optional. Filter by token ID.

```typescript TypeScript
// All open orders for this builder
const orders = await client.getOpenOrders();

// Filtered by market
const marketOrders = await client.getOpenOrders({
  market: "0xbd31dc8a...",
});
```

***

### getBuilderTrades

Retrieves all trades attributed to your builder code. Use this to track which trades were routed through your platform.

```typescript Signature
async getBuilderTrades(
  params?: TradeParams,
): Promise<BuilderTradesPaginatedResponse>
```

**Params (`TradeParams`)**

**`id`** `string`
Optional. Filter trades by trade ID.

**`maker_address`** `string`
Optional. Filter trades by maker address.

**`market`** `string`
Optional. Filter trades by market condition ID.

**`asset_id`** `string`
Optional. Filter trades by asset (token) ID.

**`before`** `string`
Optional. Return trades created before this cursor value.

**`after`** `string`
Optional. Return trades created after this cursor value.

**Response (`BuilderTradesPaginatedResponse`)**

**`trades`** `BuilderTrade[]`
Array of trades attributed to the builder account.

**`next_cursor`** `string`
Cursor string for fetching the next page of results.

**`limit`** `number`
Maximum number of trades returned per page.

**`count`** `number`
Total number of trades returned in this response.

**`BuilderTrade` fields**

**`id`** `string`
Unique identifier for the trade.

**`tradeType`** `string`
Type of the trade.

**`takerOrderHash`** `string`
Hash of the taker order associated with this trade.

**`builder`** `string`
Builder code attributed to this trade.

**`market`** `string`
Condition ID of the market this trade belongs to.

**`assetId`** `string`
Token ID of the asset traded.

**`side`** `string`
Side of the trade (e.g. BUY or SELL).

**`size`** `string`
Size of the trade in shares.

**`sizeUsdc`** `string`
Size of the trade denominated in USDC.

**`price`** `string`
Price at which the trade was executed.

**`status`** `string`
Current status of the trade.

**`outcome`** `string`
Outcome label associated with the traded asset.

**`outcomeIndex`** `number`
Index of the outcome within the market.

**`owner`** `string`
Address of the order owner (taker).

**`maker`** `string`
Address of the maker in the trade.

**`transactionHash`** `string`
On-chain transaction hash for the trade.

**`matchTime`** `string`
Timestamp when the trade was matched.

**`bucketIndex`** `number`
Bucket index used for trade grouping.

**`fee`** `string`
Fee charged for the trade in shares.

**`feeUsdc`** `string`
Fee charged for the trade denominated in USDC.

**`err_msg`** `string | null`
Optional. Error message if the trade encountered an issue, otherwise null.

**`createdAt`** `string | null`
Timestamp when the trade record was created, or null if unavailable.

**`updatedAt`** `string | null`
Timestamp when the trade record was last updated, or null if unavailable.

***

## See Also

- **[Builders Program](/builders/overview)** — Learn about the Builders Program and its benefits.

- **[Order Attribution](/trading/orders/attribution)** — Attach your builder code to orders for volume credit.

- **[L2 Methods](/trading/clients/l2)** — Place and manage orders with API credentials.

- **[Gasless Transactions](/trading/gasless)** — Execute onchain operations without paying gas.

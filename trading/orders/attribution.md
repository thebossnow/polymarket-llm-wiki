# Order Attribution

> Attribute orders to your builder code for volume credit and fee rewards

Order attribution credits trades to your builder account by attaching your **builder code** to every order. This enables:

* Volume tracking on the [Builder Leaderboard](https://builders.polymarket.com/)
* Fee rewards through the [Builder Program](/builders/overview)
* Performance monitoring via the Data API

***

## Builder Code

Your **builder code** is a `bytes32` identifier tied to your builder profile. Find it at [polymarket.com/settings?tab=builder](https://polymarket.com/settings?tab=builder).

That's the only credential you need for attribution — no HMAC signing, no separate API key, no special headers.

> **Note:** Builder codes are public identifiers — they appear onchain in the `builder` field of every order you attribute. Only you control which orders include your code, so keep it scoped to apps you own.

***

## Attaching the Builder Code

Pass `builderCode` in the order struct on every order you submit. The SDK serializes it into the onchain order's `builder` field, and the protocol attributes every matched trade to your profile.

```typescript TypeScript
import { ClobClient, Side, OrderType } from "@polymarket/clob-client-v2";

const client = new ClobClient({
  host: "https://clob.polymarket.com",
  chain: 137,
  signer,
  creds: apiCreds,
  signatureType: 3,
  funderAddress: depositWalletAddress,
});

const response = await client.createAndPostOrder(
  {
    tokenID: "0x...",
    price: 0.55,
    size: 100,
    side: Side.BUY,
    builderCode: "0xabc123...", // your builder code from polymarket.com/settings?tab=builder
  },
  { tickSize: "0.01", negRisk: false },
  OrderType.GTC,
);
```

```python Python
from py_clob_client_v2 import ClobClient
from py_clob_client_v2 import OrderArgs, OrderType, PartialCreateOrderOptions
from py_clob_client_v2.order_builder.constants import BUY

client = ClobClient(
    host="https://clob.polymarket.com",
    chain_id=137,
    key=private_key,
    creds=api_creds,
    signature_type=3,
    funder=deposit_wallet_address,
)

response = client.create_and_post_order(
    OrderArgs(
        token_id="0x...",
        price=0.55,
        size=100,
        side=BUY,
        builder_code="0xabc123...",  # your builder code from polymarket.com/settings?tab=builder
    ),
    options=PartialCreateOrderOptions(tick_size="0.01", neg_risk=False),
    order_type=OrderType.GTC,
)
```

Every order placed with `builderCode` attached is credited to your builder profile — no additional configuration needed.

***

## Verifying Attribution

Query trades attributed to your builder code:

```typescript TypeScript
const trades = await client.getBuilderTrades();

// Filtered by market
const marketTrades = await client.getBuilderTrades({
  market: "0xbd31dc8a...",
});
```

```python Python
trades = client.get_builder_trades()

market_trades = client.get_builder_trades(
    market="0xbd31dc8a..."
)
```

Each `BuilderTrade` includes: `id`, `market`, `assetId`, `side`, `size`, `price`, `status`, `outcome`, `owner`, `maker`, `builder`, `transactionHash`, `matchTime`, `fee`, and `feeUsdc`.

***

## Troubleshooting

#### Volume not appearing on the leaderboard

Confirm your `builderCode` is correctly attached to every order
Check that orders are being matched, not just placed
Allow up to 24 hours for volume to appear on the leaderboard

#### Invalid builder code
Verify the code matches what's shown on [your Builder
Profile](https://polymarket.com/settings?tab=builder). Builder codes are
`bytes32` hex values starting with `0x`.

***

## Next Steps

- **[Builder Program](/builders/overview)** — Learn about the Builder Program tiers and rewards

- **[Create Orders](/trading/orders/create)** — Build, sign, and submit orders

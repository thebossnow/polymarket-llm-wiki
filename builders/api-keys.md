# Builder Code

> Your builder code for order attribution

Your **Builder Code** is a `bytes32` identifier that attributes orders routed through your application to your builder profile. Attach it to every order you submit — no additional authentication is required.

## Accessing Your Builder Profile

### Direct Link
Go to
[polymarket.com/settings?tab=builder](https://polymarket.com/settings?tab=builder)

### From MenuClick your profile image → Select "Builders"

## Getting Your Builder Code

In the **Builder Code** section of your profile, copy the `bytes32` value. It looks like:

```
0x0000000000000000000000000000000000000000000000000000000000000001
```

Store it in your environment variables or a secrets manager.

> **Note:** Builder codes are public identifiers — they appear onchain in the `builder` field of every order you attribute. Only you control which orders include your code, so keep it scoped to the apps you own.

## Profile Settings

Your builder profile includes customizable settings:

| Setting             | Description                                                             |
| ------------------- | ----------------------------------------------------------------------- |
| **Profile Picture** | Displayed on the [Builder Leaderboard](https://builders.polymarket.com) |
| **Builder Name**    | Public name shown on the leaderboard                                    |
| **Builder Address** | Your unique builder identifier (read-only)                              |
| **Builder Code**    | The `bytes32` code you attach to orders                                 |
| **Current Tier**    | Your rate limit tier: Unverified, Verified, or Partner                  |

## Environment Variables

Store your builder code as an environment variable:

**Bash**
```bash .env
POLY_BUILDER_CODE=0x0000000000000000000000000000000000000000000000000000000000000001
```

**TypeScript**
```typescript
const builderCode = process.env.POLY_BUILDER_CODE!;
```

**Python**
```python
import os

builder_code = os.environ["POLY_BUILDER_CODE"]
```

## Using Your Builder Code

Pass `builderCode` on every order to attribute it to your builder profile:

```typescript TypeScript
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
from py_clob_client_v2 import OrderArgs, PartialCreateOrderOptions
from py_clob_client_v2.order_builder.constants import BUY

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

See [Order Attribution](/trading/orders/attribution) for full details.

## Troubleshooting

#### Rate limit exceeded
**Cause:** You've exceeded your tier's daily transaction limit.

**Solution:**

* Wait until the daily limit resets
* [Contact Polymarket](/builders/tiers#contact) to upgrade your tier

#### Builder code not found
**Cause:** You haven't created a builder profile yet.

**Solution:** Go to
[polymarket.com/settings?tab=builder](https://polymarket.com/settings?tab=builder)
and set up your profile to get a builder code.

## Next Steps

- **[Attribute Orders](/trading/orders/attribution)** — Attach your builder code to orders for volume credit.

- **[Understand Tiers](/builders/tiers)** — Learn about rate limits and how to upgrade.

# Merge Tokens

> Convert outcome token pairs back to pUSD

**Merging** is the inverse of splitting — it converts a full set of outcome tokens back into pUSD collateral. For every 1 Yes token and 1 No token you merge, you receive \$1 pUSD. The condition must already be prepared on the CTF contract (via `prepareCondition`).

```
100 Yes tokens + 100 No tokens → $100 pUSD
```

## Prerequisites

Before merging, you need:

1. **Equal amounts** of both Yes and No tokens
2. **Condition ID** of the market
3. **Sufficient gas** for the transaction

> **Note:** Polymarket uses thin collateral adapter contracts for pUSD-native CTF actions. Approve the adapter once, then route split, merge, and redeem actions through it. For merge flows, the adapter calls the underlying CTF contract, receives the released USDC.e collateral, wraps it into pUSD, and returns pUSD to your wallet automatically.

## How It Works

1. You call the adapter's merge flow with the amount and market details
2. One unit of each position in a full set is burned in return for 1 collateral unit
3. The adapter converts the released collateral into pUSD and returns pUSD to your wallet

The operation is atomic — if you don't have enough of both tokens, the transaction reverts.

## Function Parameters

**`collateralToken`** `IERC20`
pUSD (Polymarket USD) contract address: `0xC011a7E12a19f7B1f670d46F03B03f3342E82DFB`

**`parentCollectionId`** `bytes32`
Always `0x0000...0000` (32 zero bytes) for Polymarket markets

**`conditionId`** `bytes32`
The market's condition ID, available from the Markets API

**`partition`** `uint[]`
Array of index sets: `[1, 2]` for binary markets

**`amount`** `uint256`
The number of full sets to merge. Also the amount of collateral to receive.

## Next Steps

- **[Redeem Tokens](/trading/ctf/redeem)** — Exchange winning tokens for pUSD after resolution

- **[CTF Overview](/trading/ctf/overview)** — Learn more about the Conditional Token Framework

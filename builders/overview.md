# Builder Program

> Build applications that route orders through Polymarket

A **builder** is a person, group, or organization that routes orders from users to Polymarket. If you've created a platform that allows users to trade on Polymarket through your system, this program is for you.

## Program Benefits

- **Gasless Transactions** — All onchain operations are gas-free through our relayer

- **Order Attribution** — Get credit for orders and compete for grants on the Builder Leaderboard

### What You Get

| Benefit             | Description                                                                     |
| ------------------- | ------------------------------------------------------------------------------- |
| **Relayer Access**  | Gas-free wallet deployment, approvals, order execution and CTF operations       |
| **Volume Tracking** | All orders attributed to your builder profile                                   |
| **Leaderboard**     | Public visibility on [builders.polymarket.com](https://builders.polymarket.com) |
| **Support**         | Telegram channel and engineering support (Verified+)                            |

> **Warning:** EOA wallets do not have relayer access. Users trading directly from an EOA pay their own gas fees.

## How It Works

### User Places Order
User places an order through your application.

### Attach Builder Code
Your app adds your `builderCode` to the order struct.

### Submit to CLOB
Order is submitted to Polymarket's CLOB — the builder code is serialized
onchain as part of the signed order.

### Trade Execution
Polymarket matches the order and covers gas fees for onchain operations.

### Volume Attribution
Volume is credited to your builder account for every matched trade where
your code is attached.

## Getting Started

### Create Builder Profile
Go to
[polymarket.com/settings?tab=builder](https://polymarket.com/settings?tab=builder)
and copy your builder code.

### Attach Your Builder Code
Pass `builderCode` on every order you submit — see [Order
Attribution](/trading/orders/attribution).

### Enable Gasless Transactions
Use the Relayer Client for gas-free wallet deployment and onchain
operations.

### Track Performance
Monitor your volume on the [Builder
Leaderboard](https://builders.polymarket.com).

## SDKs and Libraries

- **[CLOB Client (TypeScript)](https://github.com/Polymarket/clob-client-v2)** — Place orders with builder attribution

- **[CLOB Client (Python)](https://github.com/Polymarket/py-clob-client-v2)** — Place orders with builder attribution

- **[Relayer Client (TypeScript)](https://github.com/Polymarket/builder-relayer-client)** — Gasless onchain transactions

- **[Relayer Client (Python)](https://github.com/Polymarket/py-builder-relayer-client)** — Gasless onchain transactions

- **[CLOB Client (Rust)](https://github.com/Polymarket/rs-clob-client-v2)** — Place orders with builder attribution

## Examples

These open-source demo applications show how to integrate Polymarket's CLOB Client and Builder Relayer Client for gasless trading with builder order attribution.

- **Authentication** — Multiple wallet providers

- **Gasless Trading** — Deposit wallet support for new API users

- **Full Integration** — Orders, positions, CTF ops

### Deposit Wallet Integrations

New API users should use deposit wallets. Use the Builder Relayer Client to
deploy deposit wallets and execute signed wallet batches, then place CLOB
orders with `POLY_1271`.

See the [Deposit Wallet Guide](/trading/deposit-wallets) for TypeScript,
Python, Rust, and direct API integration details.

### Existing Safe Wallet Examples

Existing Safe integrations can continue using Gnosis Safe wallets:

- **[wagmi + Safe](https://github.com/Polymarket/wagmi-safe-builder-example)** — MetaMask, Phantom, Rabby, and other browser wallets

- **[Privy + Safe](https://github.com/Polymarket/privy-safe-builder-example)** — Privy embedded wallets

- **[Magic Link + Safe](https://github.com/Polymarket/magic-safe-builder-example)** — Magic Link email/social authentication

- **[Turnkey + Safe](https://github.com/Polymarket/turnkey-safe-builder-example)** — Turnkey embedded wallets

### Existing Proxy Wallet Examples

For existing Magic Link users from Polymarket.com:

- **[Magic Link + Proxy](https://github.com/Polymarket/magic-proxy-builder-example)** — Auto-deploying proxy wallets for Polymarket.com Magic users

### What Each Demo Covers

**Authentication**

User sign-in via wallet provider
User API credential derivation (L2 auth)
Builder config with remote signing
Signature types for Deposit Wallet, Safe, and Proxy wallets

**Wallet Operations**

Deposit wallet deployment via Relayer
Batch token approvals (pUSD + outcome tokens)
CTF operations (split, merge, redeem)
Transaction monitoring

**Trading**

CLOB client initialization
Order placement with builder attribution
Position and order management
Market discovery via Gamma API

***

## Next Steps

- **[Get API Keys](/builders/api-keys)** — Create and manage your Builder API credentials.

- **[Understand Tiers](/builders/tiers)** — Learn about rate limits and how to upgrade.

- **[Attribute Orders](/trading/orders/attribution)** — Configure your client to credit trades to your account.

- **[Gasless Guide](/trading/gasless)** — Set up gasless transactions for your users.

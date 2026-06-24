# TypeScript SDK

> Build with the unified Polymarket TypeScript SDK.

The unified TypeScript SDK gives you a consistent surface across Polymarket discovery, market data, trading, account data, and realtime streams.

> **Note:** The TypeScript SDK is currently in beta. We are keeping it in this beta phase while we address issues and harden the SDK before transitioning to a more stable release.

## Quickstart

### Install the Package
Install the SDK from your package manager.

```bash pnpm
pnpm add @polymarket/client@beta
```

```bash npm
npm install @polymarket/client@beta
```

```bash yarn
yarn add @polymarket/client@beta
```

### Create a Public Client
Create an instance of the `PublicClient`.

```ts
import { createPublicClient } from "@polymarket/client";

const client = createPublicClient();
```

### Fetch Markets
Fetch a page of markets to discover active trading opportunities.

```ts
const markets = client.listMarkets({
  closed: false,
  pageSize: 5,
});

const firstPage = await markets.firstPage();

for (const market of firstPage.items) {
  // market: Market
}
```

## SDK Patterns

The SDK normalizes data across API seams and uses consistent patterns for pagination and typed error handling across public and authenticated workflows.

### Typed Primitives

Common primitives such as IDs, decimal values, date/time strings, and EVM addresses are represented with explicit SDK types so integrations can avoid treating every value as a plain string.

```ts
type Market = {
  id: MarketId;
  conditionId: ConditionId | null;
  state: {
    startDate?: IsoDateTimeString | null;
    endDate?: IsoDateTimeString | null;
  };
  outcomes: {
    yes: {
      tokenId: TokenId | null;
      price: DecimalString | null;
    };
  };
  resolution: {
    resolvedBy: EvmAddress | null;
  };
  // …
};
```

### Market and Event Data

Market and event responses use normalized field names and TypeScript shapes instead of service-specific response formats.

```ts Market
type Market = {
  id: MarketId;
  slug?: string | null;
  conditionId: ConditionId | null;
  question?: string | null;
  description?: string | null;
  category?: string | null;
  image?: string | null;
  icon?: string | null;
  state: MarketState;
  outcomes: MarketOutcomes;
  metrics: MarketMetrics;
  prices: MarketPrices;
  trading: MarketTrading;
  resolution: MarketResolution;
  rewards: MarketRewards;
  sports: MarketSportsMetadata;
  tags: MarketTag[];
  // …
};
```

```ts Event
type Event = {
  id: EventId;
  slug?: string | null;
  title?: string | null;
  subtitle?: string | null;
  description?: string | null;
  category?: string | null;
  subcategory?: string | null;
  image?: string | null;
  icon?: string | null;
  createdAt?: IsoDateTimeString | null;
  updatedAt?: IsoDateTimeString | null;
  publishedAt?: IsoDateTimeString | null;
  state: EventState;
  schedule: EventSchedule;
  metrics: EventMetrics;
  trading: EventTrading;
  estimation: EventEstimation;
  sports: EventSportsMetadata;
  partners: EventPartner[];
  markets: Market[];
  series: EventSeries[];
  // …
};
```

### Pagination

List methods return a consistent paginator interface across paginated endpoints. Use `for await` to iterate through pages.

```ts
const markets = client.listMarkets({
  closed: false,
  pageSize: 10,
});

for await (const page of markets) {
  // page.items: Market[]
}
```

You can also fetch the first page directly and resume later from a cursor.

```ts
const firstPage = await markets.firstPage();
// firstPage.items: Market[]

for await (const page of markets.from(firstPage.nextCursor)) {
  // page.items: Market[]
}
```

### Error Handling

Each public action exposes a matching error guard. Use it to handle expected SDK errors and rethrow anything unexpected.

> **Note:** Error guards make exhaustive checks easier and help surface newly added SDK error cases during upgrades.

```ts
import { ListMarketsError } from "@polymarket/client";

try {
  const markets = client.listMarkets({
    closed: false,
    pageSize: 10,
  });

  const firstPage = await markets.firstPage();
  // firstPage.items: Market[]
} catch (error) {
  if (!ListMarketsError.isError(error)) {
    throw error;
  }

  switch (error.name) {
    case "RateLimitError":
      // Retry later.
      break;
    case "UserInputError":
      // Fix the request parameters.
      break;
    default:
    // …
  }
}
```

## Market Data

Use market data methods to fetch market and event details, order books, current prices, historical prices, and batch quotes.

```ts Market
const market = await client.fetchMarket({
  url: "https://polymarket.com/market/eth-flipped-in-2026",
});

const market = await client.fetchMarket({
  slug: "eth-flipped-in-2026",
});

const market = await client.fetchMarket({
  id: "12345",
});
```

```ts Event
const event = await client.fetchEvent({
  url: "https://polymarket.com/event/presidential-election-2028",
});

const event = await client.fetchEvent({
  slug: "presidential-election-2028",
});

const event = await client.fetchEvent({
  id: "12345",
});
```

Then fetch related tags, order books, prices, and history.

```ts Tags
const marketTags = await client.fetchMarketTags({
  id: market.id,
});

const eventTags = await client.fetchEventTags({
  id: event.id,
});
```

```ts Order Book
const book = await client.fetchOrderBook({
  tokenId: market.outcomes.yes.tokenId!,
});
```

```ts Prices
import { OrderSide } from "@polymarket/client";

const buyPrice = await client.fetchPrice({
  tokenId: market.outcomes.yes.tokenId!,
  side: OrderSide.BUY,
});

const midpoint = await client.fetchMidpoint({
  tokenId: market.outcomes.yes.tokenId!,
});

const spread = await client.fetchSpread({
  tokenId: market.outcomes.yes.tokenId!,
});

const lastTrade = await client.fetchLastTradePrice({
  tokenId: market.outcomes.yes.tokenId!,
});
```

```ts History
const history = await client.fetchPriceHistory({
  tokenId: market.outcomes.yes.tokenId!,
  interval: "1d",
});
```

```ts Batch Reads
import { OrderSide } from "@polymarket/client";

const prices = await client.fetchPrices([
  {
    tokenId: market.outcomes.yes.tokenId!,
    side: OrderSide.BUY,
  },
  {
    tokenId: market.outcomes.no.tokenId!,
    side: OrderSide.BUY,
  },
]);

const midpoints = await client.fetchMidpoints([
  {
    tokenId: market.outcomes.yes.tokenId!,
  },
  {
    tokenId: market.outcomes.no.tokenId!,
  },
]);
```

## Discovery

Use discovery methods to browse events, markets, teams, tags, comments, sports metadata, and search results. The examples below show a few common entry points.

**Events**
```ts
const events = client.listEvents({
  pageSize: 10,
});

for await (const page of events) {
  // page.items: Event[]
}
```

**Markets**
```ts
const markets = client.listMarkets({
  closed: false,
  pageSize: 10,
});

for await (const page of markets) {
  // page.items: Market[]
}
```

**Teams**
```ts
const teams = client.listTeams({
  league: ["NBA"],
  pageSize: 10,
});

for await (const page of teams) {
  // page.items: Team[]
}
```

**Tags**
```ts
const tags = client.listTags({
  pageSize: 10,
});

for await (const page of tags) {
  // page.items: Tag[]
}

const tag = await client.fetchTag({
  slug: "politics",
});

const relatedTags = await client.fetchRelatedTags({
  slug: "politics",
});

const relatedResources = await client.fetchRelatedTagResources({
  slug: "politics",
  status: "active",
});
```

**Comments**
```ts
const comments = client.listComments({
  parentEntityId: "12345",
  parentEntityType: "Event",
  pageSize: 20,
});

for await (const page of comments) {
  // page.items: Comment[]
}

const thread = await client.fetchCommentsById({
  id: "456",
  getPositions: true,
});

const userComments = client.listCommentsByUserAddress({
  address: "0x1234…",
  pageSize: 10,
  order: "DESC",
});

for await (const page of userComments) {
  // page.items: Comment[]
}
```

**Sports**
```ts
const sports = await client.listSports();

// sports: SportsMetadata[]
```

**Search**
```ts
const results = client.search({
  q: "ethereum",
  pageSize: 10,
});

for await (const page of results) {
  // page.items.events: Event[]
  // page.items.tags: SearchTag[]
  // page.items.profiles: Profile[]
}
```

## Realtime Streams

Subscribe through one SDK interface even when events are served by different websocket surfaces. The SDK routes each subscription spec to the right stream and merges the results into one stream.

```ts
const stream = await client.subscribe([
  {
    topic: "market",
    tokenIds: [market.outcomes.yes.tokenId!],
  },
  {
    topic: "prices.crypto.binance",
    symbols: ["btcusdt"],
  },
]);

for await (const event of stream) {
  // event:
  //   | MarketBookEvent
  //   | MarketPriceChangeEvent
  //   | MarketLastTradePriceEvent
  //   | MarketTickSizeChangeEvent
  //   | CryptoPricesBinanceEvent

  if (shouldStopStreaming()) {
    await stream.close();
  }
}
```

## Authenticated Client

Create a secure client when you need wallet-scoped reads or trading.

By default, `createSecureClient` uses the signer's deterministic Deposit Wallet
as the account wallet. The SDK deploys that wallet if needed during client
creation. Pass `wallet` only when you want to authenticate an existing wallet,
such as an existing Deposit Wallet, Poly Safe, Poly Proxy, or the signer address
itself for EOA trading.

The examples below pass `wallet` to make account selection explicit. Omit
`wallet` to use the default Deposit Wallet flow.

### Wallet Integrations

The SDK is intended to support a variety of wallet libraries. At launch, we support [Viem](https://viem.sh), [Privy](https://www.privy.io/docs), and [Ethers v5](https://docs.ethers.org/v5/). We will expand support for more libraries based on demand.

**Viem**

### Install the Packages
Install the SDK and Viem wallet tools.

```bash
pnpm add @polymarket/client@beta viem
```

### Create the Secure Client
Use the private-key helper, or adapt an existing `viem` wallet client.

```ts Private Key
import { createSecureClient } from "@polymarket/client";
import { privateKey } from "@polymarket/client/viem";

const secureClient = await createSecureClient({
  wallet: "YOUR_POLYMARKET_WALLET_ADDRESS",
  signer: privateKey(process.env.PRIVATE_KEY),
});
```

```ts Wallet Client
import { createSecureClient } from "@polymarket/client";
import { signerFrom } from "@polymarket/client/viem";
import { createWalletClient, http } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { polygon } from "viem/chains";

const walletClient = createWalletClient({
  account: privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`),
  chain: polygon,
  transport: http(),
});

const secureClient = await createSecureClient({
  wallet: "YOUR_POLYMARKET_WALLET_ADDRESS",
  signer: signerFrom(walletClient),
});
```

**Privy**

### Install the Packages
Install the SDK and Privy Node client.

```bash
pnpm add @polymarket/client@beta @privy-io/node
```

### Create the Secure Client
Use the Privy Node client with the SDK's Privy signer adapter.

```ts
import { createSecureClient } from "@polymarket/client";
import { signerFrom } from "@polymarket/client/privy";
import { PrivyClient } from "@privy-io/node";

const privy = new PrivyClient({
  appId: process.env.PRIVY_APP_ID!,
  appSecret: process.env.PRIVY_APP_SECRET!,
});

const secureClient = await createSecureClient({
  wallet: "YOUR_POLYMARKET_WALLET_ADDRESS",
  signer: signerFrom({
    privy,
    walletId: process.env.PRIVY_WALLET_ID!,
  }),
});
```

**Ethers v5**

### Install the Packages
Install the SDK and the Ethers v5 package alias used by the adapter.

```bash
pnpm add @polymarket/client@beta ethers-v5@npm:ethers@^5.8.0
```

### Create the Secure Client
Use the Ethers v5 signer adapter when your integration already manages an `ethers.Signer`.

```ts
import { createSecureClient } from "@polymarket/client";
import { signerFrom } from "@polymarket/client/ethers-v5";
import { ethers } from "ethers-v5";

const provider = new ethers.providers.JsonRpcProvider(
  process.env.POLYGON_RPC_URL,
);
const wallet = new ethers.Wallet(process.env.PRIVATE_KEY!, provider);

const secureClient = await createSecureClient({
  wallet: "YOUR_POLYMARKET_WALLET_ADDRESS",
  signer: signerFrom(wallet),
});
```

### Trading Setup

Before placing orders, make sure the authenticated wallet is deployed and has
the required trading approvals. `createSecureClient` resolves the signer's
deterministic Deposit Wallet by default and deploys it if needed.

### Configure API Key Authorization
Configure API key authorization when the SDK needs to deploy a Deposit Wallet or
submit approval transactions.

```ts Relayer API Key
import { createSecureClient, relayerApiKey } from "@polymarket/client";

const secureClient = await createSecureClient({
  wallet: "YOUR_POLYMARKET_WALLET_ADDRESS",
  signer,
  apiKey: relayerApiKey({
    key: process.env.RELAYER_API_KEY!,
    address: process.env.RELAYER_API_KEY_ADDRESS!,
  }),
});
```

```ts Builder API Key
import { createSecureClient } from "@polymarket/client";
import { builderApiKey } from "@polymarket/client/node";

const secureClient = await createSecureClient({
  wallet: "YOUR_POLYMARKET_WALLET_ADDRESS",
  signer,
  apiKey: builderApiKey({
    key: process.env.BUILDER_API_KEY!,
    secret: process.env.BUILDER_SECRET!,
    passphrase: process.env.BUILDER_PASSPHRASE!,
  }),
});
```

> **Note:** Builder API keys are supported for backwards compatibility with builders that still use them for wallet operations. They are not used for order attribution. Use `builderCode` on orders for attribution.

### Set Up Trading Approvals
Then set up trading approvals.

```ts
await secureClient.setupTradingApprovals();
```

`setupTradingApprovals()` waits for the setup transaction internally and is
idempotent. If the wallet already has the required approvals, it returns without
submitting a transaction.

### Trading

Use a secure client to create, sign, and submit orders. Limit orders specify the price and size you want to trade. Market orders execute against resting liquidity immediately.

Order placement returns a discriminated response. Check `response.ok` before reading order details.

#### Place Orders

**Limit Order**
```ts
import { OrderSide } from "@polymarket/client";

const response = await secureClient.placeLimitOrder({
  tokenId: market.outcomes.yes.tokenId!,
  side: OrderSide.BUY,
  price: 0.52,
  size: 10,
});

if (response.ok) {
  // response.orderId: string
} else {
  // response.code: OrderResponseErrorCode
  // response.message: string
}
```

**Expiring Limit Order**
```ts
import { OrderSide } from "@polymarket/client";

const response = await secureClient.placeLimitOrder({
  tokenId: market.outcomes.yes.tokenId!,
  side: OrderSide.SELL,
  price: 0.52,
  size: 10,
  expiration: Math.floor(Date.now() / 1000) + 60 * 60,
});

if (response.ok) {
  // response.orderId: string
} else {
  // response.code: OrderResponseErrorCode
  // response.message: string
}
```

**Partial-Fill Market Order**
```ts
import { OrderSide, OrderType } from "@polymarket/client";

const response = await secureClient.placeMarketOrder({
  tokenId: market.outcomes.yes.tokenId!,
  side: OrderSide.BUY,
  amount: 10,
  maxSpend: 11,
  orderType: OrderType.FAK,
});

if (response.ok) {
  // response.orderId: string
} else {
  // response.code: OrderResponseErrorCode
  // response.message: string
}
```

**All-Or-Nothing Market Order**
```ts
import { OrderSide, OrderType } from "@polymarket/client";

const response = await secureClient.placeMarketOrder({
  tokenId: market.outcomes.yes.tokenId!,
  side: OrderSide.SELL,
  shares: 10,
  orderType: OrderType.FOK,
});

if (response.ok) {
  // response.orderId: string
} else {
  // response.code: OrderResponseErrorCode
  // response.message: string
}
```

**Builder Code**
```ts
import { OrderSide } from "@polymarket/client";

const response = await secureClient.placeLimitOrder({
  tokenId: market.outcomes.yes.tokenId!,
  side: OrderSide.BUY,
  price: 0.52,
  size: 10,
  builderCode: "0xabc123…",
});

if (response.ok) {
  // response.orderId: string
} else {
  // response.code: OrderResponseErrorCode
  // response.message: string
}
```

#### Create, Then Post

Create signed orders separately when you want to review, store, or batch them before submitting.

**Single Order**
```ts
import { OrderSide } from "@polymarket/client";

const order = await secureClient.createLimitOrder({
  tokenId: market.outcomes.yes.tokenId!,
  side: OrderSide.BUY,
  price: 0.52,
  size: 10,
});

const response = await secureClient.postOrder(order);

if (response.ok) {
  // response.orderId: string
} else {
  // response.code: OrderResponseErrorCode
  // response.message: string
}
```

**Batch Orders**
```ts
import { OrderSide } from "@polymarket/client";

const firstOrder = await secureClient.createLimitOrder({
  tokenId: market.outcomes.yes.tokenId!,
  side: OrderSide.BUY,
  price: 0.52,
  size: 10,
});

const secondOrder = await secureClient.createLimitOrder({
  tokenId: market.outcomes.yes.tokenId!,
  side: OrderSide.SELL,
  price: 0.58,
  size: 5,
});

const responses = await secureClient.postOrders([firstOrder, secondOrder]);

for (const response of responses) {
  if (response.ok) {
    // response.orderId: string
  } else {
    // response.code: OrderResponseErrorCode
    // response.message: string
  }
}
```

### Position Lifecycle

Use position lifecycle methods to split collateral into outcome tokens, merge
complete sets back into collateral, or redeem resolved positions. These examples
assume you created a secure client and set up trading approvals as shown above.

**Split Position**
```ts
const handle = await secureClient.splitPosition({
  conditionId: market.conditionId!,
  amount: 1n,
});

const outcome = await handle.wait();

// outcome.transactionHash: TxHash
```

**Merge Positions**
```ts
const handle = await secureClient.mergePositions({
  conditionId: market.conditionId!,
  amount: "max",
});

const outcome = await handle.wait();

// outcome.transactionHash: TxHash
```

**Redeem Positions**
```ts
const handle = await secureClient.redeemPositions({
  marketId: market.id,
});

const outcome = await handle.wait();

// outcome.transactionHash: TxHash
```

### Wallet Operations

Use wallet operation methods for direct token movements from the authenticated
wallet. These examples assume you created a secure client as shown above.

```ts
const handle = await secureClient.transferErc20({
  amount: 1n,
  recipientAddress: "RECIPIENT_ADDRESS",
  tokenAddress: secureClient.environment.collateralToken,
});

const outcome = await handle.wait();

// outcome.transactionHash: TxHash
```

### Order Management

Manage open orders for the authenticated wallet after placement. These examples assume `orderId` comes from an accepted order response.

**Fetch Order**
```ts
const order = await secureClient.fetchOrder({
  orderId,
});

// order: OpenOrder
```

**List Open Orders**
```ts
const openOrders = secureClient.listOpenOrders({
  market: market.id, // Or market.conditionId
});

for await (const page of openOrders) {
  // page.items: OpenOrder[]
}
```

**Cancel Order**
```ts
const response = await secureClient.cancelOrder({
  orderId,
});

// response.canceled: string[]
```

**Cancel Market Orders**
```ts
const response = await secureClient.cancelMarketOrders({
  tokenId: market.outcomes.yes.tokenId!,
});

// response.canceled: string[]
```

### Rewards and Scoring

Use rewards methods to inspect active reward programs and scoring methods to check whether orders are eligible for scoring.

**Current Rewards**
```ts
const rewards = client.listCurrentRewards();

for await (const page of rewards) {
  // page.items: CurrentReward[]
}
```

**Market Rewards**
```ts
const rewards = client.listMarketRewards({
  conditionId: market.conditionId!,
});

for await (const page of rewards) {
  // page.items: MarketReward[]
}
```

**Order Scoring**
```ts
const scoring = await secureClient.fetchOrderScoring({
  orderId,
});

// scoring: boolean
```

**Batch Order Scoring**
```ts
const scoring = await secureClient.fetchOrdersScoring({
  orderIds: [firstOrderId, secondOrderId],
});

// scoring: OrdersScoringResponse
```

### Account Data

Secure clients can read account-scoped data for the authenticated wallet.

**Positions**
```ts
const positions = secureClient.listPositions({
  market: [market.id], // Or market.conditionId
  pageSize: 10,
});

for await (const page of positions) {
  // page.items: Position[]
}
```

**Portfolio Value**
```ts
const value = await secureClient.fetchPortfolioValue({
  market: [market.id], // Or market.conditionId
});

// value: Value[]
```

**Activity**
```ts
import { ActivityType } from "@polymarket/client";

const activity = secureClient.listActivity({
  market: [market.id], // Or market.conditionId
  pageSize: 10,
});

for await (const page of activity) {
  for (const item of page.items) {
    switch (item.type) {
      case ActivityType.TRADE:
        // item.tokenId: TokenId
        // item.shares: DecimalString
        break;
      case ActivityType.REWARD:
        // item.amount: DecimalString
        break;
      default:
      // …
    }
  }
}
```

**Trades**
```ts
const yesTokenId = market.outcomes.yes.tokenId!;

const trades = secureClient.listAccountTrades({
  tokenId: yesTokenId,
});

for await (const page of trades) {
  // page.items: ClobTrade[]
}
```

**Notifications**
```ts
const notifications = await secureClient.fetchNotifications();

// notifications: Notification[]
```

### Authentication Sessions

Secure clients expose the API credentials created for the authenticated session. Store them securely if you want to reuse the session later without requiring a new authentication signature while the credentials remain valid.

**Save Credentials**
```ts
const secureClient = await createSecureClient({
  wallet: "YOUR_POLYMARKET_WALLET_ADDRESS",
  signer,
});

await storage.set("polymarketCredentials", secureClient.credentials);
```

**Reuse Credentials**
```ts
const credentials = await storage.get("polymarketCredentials");

const secureClient = await createSecureClient({
  wallet: "YOUR_POLYMARKET_WALLET_ADDRESS",
  signer,
  credentials,
});
```

## Changelog

### `0.1.0-beta.8`

* RFQ quoter sessions now emit typed `trade` events for confirmed Combos fills.
* RFQ rejection errors now expose `errorId` values and parse `INVALID_SIGNATURE` and `INTERNAL_ERROR` codes.

### `0.1.0-beta.7`

* Added `parentEventId` to `Event` so child events can link back to their parent event.
* Added `maxPrice` and `minPrice` protection fields to market order requests.
* Handle legacy multi-outcome markets more safely: `listMarkets` skips markets that cannot be represented by the binary market model, and `fetchMarket` returns a typed SDK error for unsupported markets.
* Normalize empty-string order and activity fields to SDK values: decimal amounts become `"0"`, missing maker order fee rates become `null`, and missing trade or position market icons become `null`.
* Parse Combo trade activity rows with an `isCombo` discriminated union.
* Support new Combos RFQ websocket error codes for balance, allowance, and pre-execution reservation failures.
* Broad user websocket subscriptions now omit market filters so all-market streams receive trade events.
* Retry rejected JSON-RPC `eth_call` batches by splitting them into smaller batches.

### `0.1.0-beta.6`

* Point Combos RFQ endpoints at the production domains: `combos-rfq-api.polymarket.com` (REST) and `combos-rfq-gateway-quoter.polymarket.com` (quoter WebSocket).

### `0.1.0-beta.5`

* Added `listComboMarkets` for fetching the Combo market catalog with typed bindings and SDK-owned pagination. See [Combos](/market-makers/combos).
* Parse RFQ quote rejections that use the `SUBMISSION_WINDOW_CLOSED` gateway error code.

### `0.1.0-beta.4`

* Added Combos support for multi-leg RFQ positions. See [Combos](/market-makers/combos).
* Reject whitespace-only search queries and trim leading or trailing search input.
* `ConditionId` is now deprecated in favor of `CtfConditionId`; existing
`ConditionId` exports remain available as deprecated aliases.

### `0.1.0-beta.3`

**Secure client setup now defaults to the Deposit Wallet flow**

`createSecureClient` can now derive and use the signer's deterministic Deposit
Wallet when you omit `wallet`. If you already know which Polymarket wallet you
want to use, keep passing `wallet`.

```diff
const secureClient = await createSecureClient({
-  wallet: "YOUR_POLYMARKET_WALLET_ADDRESS",
   signer,
});
```

If you want to keep account selection explicit, no change is required:

```ts
const secureClient = await createSecureClient({
  wallet: "YOUR_POLYMARKET_WALLET_ADDRESS",
  signer,
});
```

**`setupTradingApprovals()` now waits internally**

You no longer need to wait on the returned handle. Call the method once before
trading; it is safe to call again if approvals are already set.

```diff
-const handle = await secureClient.setupTradingApprovals();
-await handle.wait();
+await secureClient.setupTradingApprovals();
```

**Gasless setup helpers are deprecated**

You no longer need to call `isGaslessReady()` or `setupGaslessWallet()` in the
normal setup path. Create the secure client, then set up trading approvals.

```diff
-const ready = await secureClient.isGaslessReady();
-
-if (!ready) {
-  secureClient = await secureClient.setupGaslessWallet();
-}
-
 await secureClient.setupTradingApprovals();
```

### `0.1.0-beta.2`

First beta release of the unified TypeScript SDK. Install the beta package with
your package manager:

```bash
pnpm add @polymarket/client@beta
```

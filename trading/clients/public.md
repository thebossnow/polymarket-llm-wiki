# Public Methods

> These methods can be called without a signer or user credentials. Use these for reading market data, prices, and order books.

## Client Initialization

Public methods require the client to initialize with the host URL and Polygon chain ID.

**TypeScript**
```typescript
import { ClobClient } from "@polymarket/clob-client-v2";

const client = new ClobClient({
  host: "https://clob.polymarket.com",
  chain: 137,
});

// Ready to call public methods
const markets = await client.getMarkets();
```

**Python**
```python
from py_clob_client_v2 import ClobClient

client = ClobClient(
    host="https://clob.polymarket.com",
    chain_id=137
)

# Ready to call public methods
markets = client.get_markets()
```

***

## Health Check

***

### getOk

Health check endpoint to verify the CLOB service is operational.

```typescript Signature
async getOk(): Promise<any>
```

***

## Markets

***

### getMarket

Get details for a single market by condition ID.

```typescript Signature
async getMarket(conditionId: string): Promise<Market>
```

**`accepting_order_timestamp`** `string`
Timestamp from which the market started accepting orders, or null if not set.

**`accepting_orders`** `boolean`
Whether the market is currently accepting orders.

**`active`** `boolean`
Whether the market is active.

**`archived`** `boolean`
Whether the market has been archived.

**`closed`** `boolean`
Whether the market is closed.

**`condition_id`** `string`
The unique condition ID for the market.

**`description`** `string`
Human-readable description of the market.

**`enable_order_book`** `boolean`
Whether the order book is enabled for this market.

**`end_date_iso`** `string`
ISO 8601 end date of the market.

**`fpmm`** `string`
Address of the Fixed Product Market Maker contract.

**`game_start_time`** `string`
Start time of the underlying game or event.

**`icon`** `string`
URL of the market icon image.

**`image`** `string`
URL of the market image.

**`is_50_50_outcome`** `boolean`
Whether the market has equal 50/50 outcomes.

**`maker_base_fee`** `number`
Base fee charged to makers in basis points.

**`market_slug`** `string`
URL-friendly slug identifier for the market.

**`minimum_order_size`** `number`
Minimum order size allowed in this market.

**`minimum_tick_size`** `number`
Minimum price increment allowed in this market.

**`neg_risk`** `boolean`
Whether the market uses negative risk (binary complementary tokens).

**`neg_risk_market_id`** `string`
Negative risk market identifier, if applicable.

**`neg_risk_request_id`** `string`
Negative risk request identifier, if applicable.

**`notifications_enabled`** `boolean`
Whether notifications are enabled for this market.

**`question`** `string`
The market question text.

**`question_id`** `string`
Unique identifier for the market question.

**`rewards`** `object`
Object containing reward config: `max_spread` (number), `min_size` (number), `rates` (any)

**`seconds_delay`** `number`
Delay in seconds before orders are processed.

**`tags`** `string[]`
List of tags associated with the market.

**`taker_base_fee`** `number`
Base fee charged to takers in basis points.

**`tokens`** `MarketToken[]`
Array of market tokens, each containing `outcome` (string), `price` (number), `token_id` (string), and `winner` (boolean).

***

### getMarkets

Get details for multiple markets paginated.

```typescript Signature
async getMarkets(): Promise<PaginationPayload>
```

**`limit`** `number`
Maximum number of results per page.

**`count`** `number`
Total number of markets returned.

**`data`** `Market[]`
Array of Market objects. See `getMarket()` for the full Market structure.

***

### getSimplifiedMarkets

Get simplified market data paginated for faster loading.

```typescript Signature
async getSimplifiedMarkets(): Promise<PaginationPayload>
```

**`limit`** `number`
Maximum number of results per page.

**`count`** `number`
Total number of markets returned.

**`data`** `SimplifiedMarket[]`
Array of simplified market objects, each containing `accepting_orders` (boolean), `active` (boolean), `archived` (boolean), `closed` (boolean), `condition_id` (string), `rewards` (object with `rates`, `min_size`, `max_spread`), and `tokens` (SimplifiedToken\[]) with `outcome` (string), `price` (number), `token_id` (string).

***

### getSamplingMarkets

Get markets eligible for sampling/liquidity rewards.

```typescript Signature
async getSamplingMarkets(): Promise<PaginationPayload>
```

***

### getSamplingSimplifiedMarkets

Get simplified market data for markets eligible for sampling/liquidity rewards.

```typescript Signature
async getSamplingSimplifiedMarkets(): Promise<PaginationPayload>
```

***

## Order Books and Prices

***

### calculateMarketPrice

Calculate the estimated price for a market order of a given size.

```typescript Signature
async calculateMarketPrice(
  tokenID: string,
  side: Side,
  amount: number,
  orderType: OrderType = OrderType.FOK
): Promise<number>
```

**`tokenID`** `string`
The token ID to calculate the market price for.

**`side`** `Side`
The side of the order. One of: `BUY`, `SELL`

**`amount`** `number`
The size of the order to calculate price for.

**`orderType`** `OrderType`
The order type. One of: `GTC` (Good Till Cancelled), `FOK` (Fill or Kill), `GTD` (Good Till Date), `FAK` (Fill and Kill). Defaults to `FOK`.

**`returns`** `number`
The calculated estimated market price for the given order size.

***

### getOrderBook

Get the order book for a specific token ID.

```typescript Signature
async getOrderBook(tokenID: string): Promise<OrderBookSummary>
```

**`market`** `string`
The market condition ID.

**`asset_id`** `string`
The token/asset ID for this order book.

**`timestamp`** `string`
Timestamp of the order book snapshot.

**`bids`** `OrderSummary[]`
Array of bid entries, each with `price` (string) and `size` (string).

**`asks`** `OrderSummary[]`
Array of ask entries, each with `price` (string) and `size` (string).

**`min_order_size`** `string`
Minimum order size for this market.

**`tick_size`** `string`
Minimum price increment for this market.

**`neg_risk`** `boolean`
Whether the market uses negative risk.

**`hash`** `string`
Hash of the order book state.

***

### getOrderBooks

Get order books for multiple token IDs.

```typescript Signature
async getOrderBooks(params: BookParams[]): Promise<OrderBookSummary[]>
```

**`token_id`** `string`
The token ID to fetch the order book for.

**`side`** `Side`
The side of the book to query. One of: `BUY`, `SELL`

**`returns`** `OrderBookSummary[]`
Array of OrderBookSummary objects. See `getOrderBook()` for the full structure.

***

### getPrice

Get the current best price for buying or selling a token ID.

```typescript Signature
async getPrice(
  tokenID: string,
  side: "BUY" | "SELL"
): Promise<any>
```

**`price`** `string`
The current best price for the requested side.

***

### getPrices

Get the current best prices for multiple token IDs.

```typescript Signature
async getPrices(params: BookParams[]): Promise<PricesResponse>
```

**`returns`** `PricesResponse`
A map of token IDs to their prices. Each entry contains an optional `BUY` (string) and/or `SELL` (string) price.

***

### getMidpoint

Get the midpoint price (average of best bid and best ask) for a token ID.

```typescript Signature
async getMidpoint(tokenID: string): Promise<any>
```

**`mid`** `string`
The midpoint price, calculated as the average of best bid and best ask.

***

### getMidpoints

Get the midpoint prices for multiple token IDs.

```typescript Signature
async getMidpoints(params: BookParams[]): Promise<any>
```

**`returns`** `object`
A map of token IDs to their midpoint price strings. Each key is a token ID and its value is the midpoint price as a string.

***

### getSpread

Get the spread (difference between best ask and best bid) for a token ID.

```typescript Signature
async getSpread(tokenID: string): Promise<SpreadResponse>
```

**`spread`** `string`
The spread value, calculated as the difference between best ask and best bid.

***

### getSpreads

Get the spreads for multiple token IDs.

```typescript Signature
async getSpreads(params: BookParams[]): Promise<SpreadsResponse>
```

**`returns`** `object`
A map of token IDs to their spread strings. Each key is a token ID and its value is the spread as a string.

***

### getPricesHistory

Get historical price data for a token.

```typescript Signature
async getPricesHistory(params: PriceHistoryFilterParams): Promise<MarketPrice[]>
```

**`market`** `string`
The token ID to fetch price history for.

**`startTs`** `number`
Optional start timestamp (Unix seconds) for the price history range.

**`endTs`** `number`
Optional end timestamp (Unix seconds) for the price history range.

**`fidelity`** `number`
Optional fidelity/resolution of the price history data.

**`interval`** `PriceHistoryInterval`
Time interval for the price history. One of: `max`, `1w`, `1d`, `6h`, `1h`

**`t`** `number`
Unix timestamp of the price data point.

**`p`** `number`
Price value at the corresponding timestamp.

***

## Trades

***

### getLastTradePrice

Get the price of the most recent trade for a token.

```typescript Signature
async getLastTradePrice(tokenID: string): Promise<LastTradePrice>
```

**`price`** `string`
The price of the most recent trade.

**`side`** `string`
The side of the most recent trade.

***

### getLastTradesPrices

Get the most recent trade prices for multiple tokens.

```typescript Signature
async getLastTradesPrices(params: BookParams[]): Promise<LastTradePriceWithToken[]>
```

**`price`** `string`
The price of the most recent trade for the token.

**`side`** `string`
The side of the most recent trade.

**`token_id`** `string`
The token ID this trade price corresponds to.

***

### getMarketTradesEvents

Get recent trade events for a market.

```typescript Signature
async getMarketTradesEvents(conditionID: string): Promise<MarketTradeEvent[]>
```

**`event_type`** `string`
The type of trade event.

**`market`** `object`
Object containing market info: `condition_id` (string), `asset_id` (string), `question` (string), `icon` (string), `slug` (string).

**`user`** `object`
Object containing user info: `address` (string), `username` (string), `profile_picture` (string), `optimized_profile_picture` (string), `pseudonym` (string).

**`side`** `Side`
The side of the trade. One of: `BUY`, `SELL`

**`size`** `string`
The size of the trade.

**`fee_rate_bps`** `string`
The fee rate in basis points for the trade.

**`price`** `string`
The price at which the trade was executed.

**`outcome`** `string`
The outcome label for the traded token.

**`outcome_index`** `number`
The index of the outcome in the market.

**`transaction_hash`** `string`
The on-chain transaction hash for the trade.

**`timestamp`** `string`
The timestamp of when the trade event occurred.

***

## Market Parameters

***

### getClobMarketInfo

Fetch all CLOB-level parameters for a market in a single call — tokens, tick size, base fees, rewards config, RFQ status, and fee details.

```typescript Signature
async getClobMarketInfo(conditionID: string): Promise<ClobMarketDetails>
```

**`conditionID`** `string`
The condition ID of the market.

**Response (`ClobMarketDetails`)**

**`gst`** `string | null`
Game start time (used for sports markets), ISO 8601 timestamp or `null`.

**`r`** `object`
Rewards configuration for the market.

**`t`** `ClobToken[]`
Tokens for this market. Each entry has:

* `t` (string) — token ID
* `o` (string) — outcome label (e.g. `Yes`, `No`)

**`mos`** `number`
Minimum order size.

**`mts`** `number`
Minimum tick size (price increment).

**`mbf`** `number`
Maker base fee in basis points.

**`tbf`** `number`
Taker base fee in basis points.

**`rfqe`** `boolean`
Whether RFQ (Request for Quote) is enabled for this market.

**`itode`** `boolean`
Whether taker order delay is enabled.

**`ibce`** `boolean`
Whether Blockaid check is enabled.

**`fd`** `object`
Fee curve parameters:

* `r` (number) — fee rate
* `e` (number) — fee curve exponent
* `to` (boolean) — whether fees apply to takers only

**`oas`** `number`
Minimum order age in seconds.

***

### getFeeRateBps

Get the fee rate in basis points for a token.

```typescript Signature
async getFeeRateBps(tokenID: string): Promise<number>
```

**`returns`** `number`
The fee rate in basis points for the specified token.

***

### getFeeExponent

Get the fee curve exponent for a token. The exponent shapes the fee curve used by the protocol when calculating fees at match time.

```typescript Signature
async getFeeExponent(tokenID: string): Promise<number>
```

**`returns`** `number`
The fee curve exponent for the specified token's market.

***

### getTickSize

Get the tick size (minimum price increment) for a market.

```typescript Signature
async getTickSize(tokenID: string): Promise<TickSize>
```

**`returns`** `string`
The tick size for the market. One of: `0.1`, `0.01`, `0.001`, `0.0001`

***

### getNegRisk

Check if a market uses negative risk (binary complementary tokens).

```typescript Signature
async getNegRisk(tokenID: string): Promise<boolean>
```

**`returns`** `boolean`
Whether the market uses negative risk.

***

## Time and Server Info

### getServerTime

Get the current server timestamp.

```typescript Signature
async getServerTime(): Promise<number>
```

**`returns`** `number`
Unix timestamp in seconds representing the current server time.

***

## See Also

- **[L1 Methods](/trading/clients/l1)** — Private key authentication to create or derive API credentials.

- **[L2 Methods](/trading/clients/l2)** — Place orders, cancel orders, and query your trades.

- **[REST API Reference](/api-reference/introduction)** — Complete REST endpoint documentation.

- **[WebSocket](/market-data/websocket/overview)** — Real-time market data streaming.

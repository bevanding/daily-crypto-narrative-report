---
name: crypto-narrative-intel
description: Give a trading or research agent crypto/AI/macro narrative context before it acts — cross-source narrative convergence (how many independent sources agree on a story now) and capital divergence (narrative vs. price, two signed axes). Use alongside a price feed and/or a stock-sentiment source; this is the crypto-narrative layer, read-only, fails safe. Powered by the signaldaemon API/MCP.
version: 1.0.0
license: MIT
metadata:
  homepage: https://signaldaemon.com
  requires: signaldaemon API key (free demo, no signup) — or the signaldaemon MCP server
---

# Crypto Narrative Intel

Read-only crypto/AI/macro **narrative context** for an agent that's about to trade,
size a position, post a strategy, or explain a market view. It is **not** price data
and **not** an order-execution tool — it's the layer a price feed or a raw
sentiment score can't give you: *which stories are converging across independent
sources, and whether capital is confirming them.*

## When to use

Before acting on a crypto/AI/macro view: to check whether a narrative is
**corroborated** (many independent sources, not one headline) and whether it is
**matched by price** (or loud-but-unfunded). Pair it with your price/execution
source and, for equities, a stock-sentiment source — this skill covers the crypto/
AI/macro narrative slice. Not for price quotes, order placement, or sub-second timing
(data is news-derived, ~20-min cadence).

## Get access (no signup)

```bash
# free demo key: 200 narrative calls/day, 5 feed calls/day, valid 7 days
curl -s -X POST https://api.signaldaemon.com/v1/request-key
```

A free **account key** (500/day, no expiry) is available at
https://signaldaemon.com/console. Pass the key as the `x-api-key` header.

## Two ways to call it

**MCP (recommended — agent-native).** Remote MCP over Streamable HTTP:
`https://api.signaldaemon.com/mcp`, header `x-api-key: <KEY>`. Tools (both read-only):

- `get_market_narratives(limit)` — the day's ranked narratives + a `market_snapshot`.
- `get_clean_feed(query, category, limit)` — de-noised, source-attributed feed for a topic.

**REST.**

```bash
curl -s https://api.signaldaemon.com/v1/narratives \
  -H "x-api-key: <KEY>" -H "content-type: application/json" -d '{"limit":8}'
```

## Procedure (before a trade/decision)

1. **Frame with the regime.** Read `market_snapshot.market_regime` (crash/range/bull)
   and `market_7d`. Every divergence reading is relative to this.
2. **Pull the narratives.** For each: `name` + `gist`; `strength` (cross-source
   convergence — independent trust-weighted sources agreeing now; higher = more
   corroborated, harder to fake than one loud headline); `momentum.members_24h`
   (accelerating?); and `divergence`.
3. **Read `divergence` as TWO independent signed axes — never infer one from the other:**
   - `direction` ∈ `up`/`down` = the asset's **absolute** 7d move.
   - `vs_market` ∈ `outperform`/`underperform` = move **relative** to `market_7d`.
   - `narrative_no_flow` → strong story, capital not following (loud but unfunded).
   - `narrative_price_aligned` → story matched by capital.
   - `no_asset` → no single tradeable asset; report the story, **do not invent a ticker**.
4. **Use it as context and risk-framing, not a buy/sell signal.** signaldaemon treats
   divergence as a *structured observation*, not a proven edge (it is being backtested
   with momentum controls). Let your own strategy decide; this informs the prior.
5. **Fail safe.** If results are sparse or `coverage: "thin"`, say so. A trustworthy
   read states what it doesn't know.

## Pitfalls

- **Don't read `narrative_price_aligned` as bullish.** In a crash an asset can be
  `direction=down` AND `vs_market=outperform` — it fell *slower* than the market
  (relative strength), not a bullish price move. Always report both axes.
- **Don't treat divergence as alpha** — it's context until proven; don't size trades on it alone.
- **Don't invent prices** for `no_asset` narratives, and don't pad `thin` coverage.
- **Don't use this for equities single-name sentiment** — it's crypto/AI/macro narrative,
  sector/narrative-level. Pair with a stock-sentiment source for stocks.

## Verification

A good use: states the **regime** first; per narrative reports convergence + momentum
+ a divergence line carrying **both** absolute and relative; flags `thin`/`no_asset`
honestly; and treats divergence as context, not a trade trigger.

## Coexists with

A price/execution source (Hyperliquid, exchange APIs) and, for equities, a stock-
sentiment source — signaldaemon adds the crypto/AI/macro narrative-convergence +
divergence layer those don't compute. How to read the signals:
https://signaldaemon.com/signals

---

_Crypto narrative & signal via signaldaemon · https://signaldaemon.com · MIT-licensed skill, no secrets (the key lives in your env / MCP config, not here)._

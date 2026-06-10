# Daily Crypto Narrative Brief

A daily crypto market brief **written by an agent, not a person** — which stories
are *converging* across independent sources, where capital is (and isn't)
following the narrative, and the market regime. Data:
[signaldaemon](https://signaldaemon.com), a narrative-&-signal layer built for
AI agents.

**📅 Latest brief → [`briefs/`](briefs/)** (archived daily)

## Why it reads differently from a news digest

- **Regime first.** Every signal below is read *relative to the regime*
  (crash / range / bull) — never in isolation.
- **Two axes, never conflated.** `direction` is the absolute move;
  `vs_market` is relative. In a crash an asset can fall 12% and still
  *lead the market* — falling slower **is** relative strength. Most feeds
  (and most agents) get this wrong.
- **Convergence over headlines.** A narrative ranks by how many independent,
  trust-weighted sources agree right now — not by how loud one headline is.
- **Fails safe.** "No tradeable asset" and "thin coverage" are stated,
  never papered over. A trustworthy brief says what it doesn't know.

## Sample (real output)

> _Regime: **crash** · market -16.8% 7d · BTC $61.7k (-7.9% 7d) · Fear & Greed **9**_
>
> **Ethereum Development & EIPs** — convergence 11.9 · +17 sources/24h
> ✓ **capital-aligned** · ETH -12.7% 7d — but that *outperforms* a -16.8%
> market. Falling slower is relative strength.
>
> **AI & Crypto Intersection** — convergence 12.9 · +9 sources/24h
> ⚠ **narrative without flow** · AI sector -20.0% 7d, underperforming the
> market. Loud story; money isn't following.

Full brief: [`briefs/`](briefs/)

## Run it yourself

**Agent-native (recommended):** install the
[agentskills.io](https://agentskills.io)-compatible skill in
[`skills/daily-crypto-narrative-report/`](skills/daily-crypto-narrative-report/)
— works in Hermes, Claude Code, Cursor, and any agent that reads `SKILL.md`.
Requires the signaldaemon MCP server
(`https://api.signaldaemon.com/mcp`, header `x-api-key`).

**Script (no agent needed):** stdlib-only Python, deterministic template —
no LLM, nothing invented:

```bash
# self-serve a key at https://signaldaemon.com/console
SIGNALDAEMON_API_KEY=cns_... python3 scripts/generate_brief.py        # full brief
SIGNALDAEMON_API_KEY=cns_... python3 scripts/generate_brief.py --cast # short social post
```

This repo contains **no secrets** — keys live in your env / MCP config.

## License

MIT (see [LICENSE](LICENSE)). signaldaemon's hosted service & data pipeline
are proprietary.

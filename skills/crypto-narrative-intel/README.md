# crypto-narrative-intel

An [agentskills.io](https://agentskills.io) skill that gives a **trading or research
agent** crypto/AI/macro **narrative context** before it acts:

- **Cross-source convergence** — how many independent, trust-weighted sources agree on
  a story right now (a narrative, not a single headline).
- **Capital divergence** — narrative vs. price, as two signed axes (`direction`
  absolute vs `vs_market` relative). Reported as *context, not a proven trading edge*.
- **Fails safe** — says `no_asset` / "no coverage" instead of inventing.

This is the **crypto-narrative layer** — designed to sit *beside* your price/execution
source and (for equities) a stock-sentiment source, not replace them. In an agent
stack like [AI-Trader](https://github.com/HKUDS/AI-Trader) you can load this alongside
a sentiment skill and read both before acting.

## Requires

The **signaldaemon** API/MCP (tools `get_market_narratives`, `get_clean_feed`).
Self-serve a key — `curl -X POST https://api.signaldaemon.com/v1/request-key` (no
signup) — and follow [`SKILL.md`](SKILL.md). **No secrets in this skill**: the key
lives in your env / MCP config.

- MCP endpoint: `https://api.signaldaemon.com/mcp` (header `x-api-key`)
- How to read the signals: https://signaldaemon.com/signals
- Quickstart (incl. running beside a trading agent): https://signaldaemon.com/quickstart

## License

MIT. signaldaemon's hosted service & data pipeline are proprietary.

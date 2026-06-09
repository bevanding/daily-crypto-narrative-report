# daily-crypto-narrative-report

A Hermes Agent / [agentskills.io](https://agentskills.io) skill that generates a
**daily crypto narrative & signal briefing** from
[signaldaemon](https://signaldaemon.com).

Each day it reports: which stories are *converging* across sources, where capital
is or isn't following the narrative, and the market regime — and it **fails safe**
(says "no coverage" rather than inventing).

## Requires

The **signaldaemon MCP server** connected in your agent (it provides the tools
`get_market_narratives` and `get_clean_feed`). Self-serve a key and follow the MCP
setup at **https://signaldaemon.com/api** (endpoint `https://api.signaldaemon.com/mcp`,
authenticated with your `x-api-key`).

This skill contains **no secrets** — the API key is held by the MCP server
connection, not by this skill.

## Use

Trigger it by asking your agent for a daily/morning crypto briefing, a market-
narrative summary, "what's moving in crypto", sector rotation, or a research digest.

Portable: the same `SKILL.md` works in any agentskills.io-compatible agent
(Hermes, Claude Code, Cursor, …).

## License

MIT (see [LICENSE](LICENSE)). signaldaemon's hosted service & data pipeline are
proprietary.
</content>

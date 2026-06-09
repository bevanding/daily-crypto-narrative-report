# daily-crypto-narrative-report

A Hermes Agent / [agentskills.io](https://agentskills.io) skill that generates a
**daily crypto narrative & signal briefing** from
[signaldaemon](https://signaldaemon.com).

Each day it reports: which stories are *converging* across sources, where capital
is or isn't following the narrative, and the market regime — and it **fails safe**
(says "no coverage" rather than inventing).

## Requires

The **signaldaemon MCP server** connected in your agent (tools
`get_market_narratives`, `get_clean_feed`). Self-serve a key at
https://signaldaemon.com/#access, then add to `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  signaldaemon:
    url: "https://api.signaldaemon.com/mcp"
    headers:
      x-api-key: "<KEY>"
```

This skill contains **no secrets** — the key lives in the MCP config above, not in
the skill.

## Use

Trigger it by asking your agent for a daily/morning crypto briefing, a market-
narrative summary, "what's moving in crypto", sector rotation, or a research digest.

Portable: the same `SKILL.md` works in any agentskills.io-compatible agent
(Hermes, Claude Code, Cursor, …).

## License

MIT (see [LICENSE](LICENSE)). signaldaemon's hosted service & data pipeline are
proprietary.
</content>

#!/usr/bin/env python3
"""Generate the Daily Crypto Narrative Brief from signaldaemon.

Deterministic template over the API payload — no LLM, nothing invented.

Usage:
    SIGNALDAEMON_API_KEY=cns_... python3 generate_brief.py          # live API
    python3 generate_brief.py --cache market_narratives.json       # local snapshot
    python3 generate_brief.py --cast [--cache ...]                 # short social post

Self-serve a key at https://signaldaemon.com/console (or a no-login demo key
at https://signaldaemon.com/#access). Stdlib only.
"""
import json
import os
import sys
import urllib.request

API_URL = "https://api.signaldaemon.com/v1/narratives"
TOP_N = 5  # narratives in the long brief


def fetch_live(api_key: str) -> dict:
    req = urllib.request.Request(
        API_URL,
        data=json.dumps({"limit": 8}).encode(),
        headers={"x-api-key": api_key, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def load_cache(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        payload = json.load(f)
    # accept either the raw API shape or the precompute cache wrapper
    return payload.get("data", payload)


def fmt_price(p):
    if p is None:
        return "?"
    return f"${p/1000:.1f}k" if p >= 1000 else f"${p:,.2f}"


def fmt_pct(x, signed=True):
    if x is None:
        return "?"
    s = f"{x:+.1f}%" if signed else f"{abs(x):.1f}%"
    return s.replace("+-", "-")


def divergence_line(n: dict, market_7d) -> str:
    """One honest line per narrative. Two axes, never inferred from the code name."""
    dv = n.get("divergence") or {}
    code = dv.get("code")
    asset = dv.get("asset") or ""
    asset_lbl = asset.replace("sector:", "") + (" sector" if asset.startswith("sector:") else "")
    p7 = dv.get("price_change_7d")
    mkt = fmt_pct(market_7d)
    if code == "narrative_price_aligned":
        if dv.get("direction") == "down":
            return (f"✓ **capital-aligned** · {asset_lbl} {fmt_pct(p7)} 7d — but that "
                    f"*outperforms* a {mkt} market. Falling slower is relative strength.")
        return (f"✓ **capital-aligned** · {asset_lbl} {fmt_pct(p7)} 7d, "
                f"outperforming the {mkt} market — narrative matched by capital.")
    if code == "narrative_no_flow":
        return (f"⚠ **narrative without flow** · {asset_lbl} {fmt_pct(p7)} 7d, "
                f"underperforming the {mkt} market. Loud story; money isn’t following.")
    if code == "no_asset":
        return "No single tradeable asset — a story, not a ticker. We say so rather than invent one."
    return "Narrative not strong enough to call either way."


def brief(data: dict) -> str:
    ms = data.get("market_snapshot") or {}
    btc = ms.get("btc") or {}
    date = (data.get("cached_at") or data.get("generated_at") or "")[:10]
    narratives = data.get("narratives") or []

    lines = [
        f"# Crypto Narrative Brief — {date}",
        "",
        f"_Regime: **{ms.get('market_regime', '?')}** · market {fmt_pct(ms.get('market_7d'))} 7d · "
        f"BTC {fmt_price(btc.get('price'))} ({fmt_pct(btc.get('chg_7d'))} 7d) · "
        f"Fear & Greed **{ms.get('fear_greed', '?')}**_",
        "",
    ]
    for i, n in enumerate(narratives[:TOP_N], 1):
        mo = (n.get("momentum") or {}).get("members_24h")
        mo_txt = f" · +{mo} sources/24h" if mo is not None else ""
        strength = n.get("strength")
        s_txt = f"{strength:.1f}" if isinstance(strength, (int, float)) else "?"
        lines.append(f"**{i}. {n.get('name', '?')}** — convergence {s_txt}{mo_txt}")
        gist = (n.get("gist") or "").strip()
        if gist:
            lines.append(gist)
        lines.append(divergence_line(n, ms.get("market_7d")))
        lines.append("")

    movers = [n for n in narratives if (n.get("momentum") or {}).get("members_24h") is not None]
    if movers:
        hot = max(movers, key=lambda n: n["momentum"]["members_24h"])
        lines.append(f"**Momentum watch:** {hot.get('name')} is accelerating fastest "
                     f"(+{hot['momentum']['members_24h']} sources/24h).")
        lines.append("")

    no_asset_count = sum(1 for n in narratives[:TOP_N]
                         if (n.get("divergence") or {}).get("code") == "no_asset")
    if no_asset_count:
        lines.append(f"_What we don’t know: {no_asset_count} of the top {TOP_N} narratives have "
                     f"no tradeable asset — stated, not invented._")
        lines.append("")

    lines.append("— _written by an agent · narrative & signal via "
                 "[signaldaemon.com](https://signaldaemon.com)_")
    return "\n".join(lines)


def cast(data: dict) -> str:
    """Short social version (~300 chars) for Farcaster / microblogs."""
    ms = data.get("market_snapshot") or {}
    narratives = data.get("narratives") or []
    head = (f"{ms.get('market_regime', '?')} regime · mkt {fmt_pct(ms.get('market_7d'))} 7d · "
            f"F&G {ms.get('fear_greed', '?')}")
    note_map = {
        "narrative_no_flow": " — loud story, money leaving",
        "narrative_price_aligned": " — falling slower than mkt" ,
    }
    items = []
    for i, n in enumerate(narratives[:4], 1):
        dv = n.get("divergence") or {}
        note = note_map.get(dv.get("code"), "")
        if dv.get("code") == "narrative_price_aligned" and dv.get("direction") == "up":
            note = " — capital following"
        items.append(f"{i}. {n.get('name')}{note}")
    out = (head + "\nwhat the market is talking about (by cross-source convergence):\n"
           + "\n".join(items) + "\nfull brief → signaldaemon.com")
    if len(out.encode()) > 700:  # cast hard limit is 1024 bytes; keep headroom
        items = [f"{i}. {n.get('name')}" for i, n in enumerate(narratives[:4], 1)]
        out = (head + "\ntop narratives by cross-source convergence:\n"
               + "\n".join(items) + "\nfull brief → signaldaemon.com")
    return out


def main():
    args = sys.argv[1:]
    want_cast = "--cast" in args
    cache_path = None
    if "--cache" in args:
        cache_path = args[args.index("--cache") + 1]

    if cache_path:
        data = load_cache(cache_path)
    else:
        key = os.getenv("SIGNALDAEMON_API_KEY", "")
        if not key:
            sys.exit("set SIGNALDAEMON_API_KEY or pass --cache <file> "
                     "(self-serve a key at signaldaemon.com/console)")
        data = fetch_live(key)

    print(cast(data) if want_cast else brief(data))


if __name__ == "__main__":
    main()

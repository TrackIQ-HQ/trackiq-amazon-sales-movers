# TrackIQ: Amazon Sales Movers and Root Cause

"Sales are down 12%" is not a finding. **Which products, and was it traffic, conversion, basket size or price?**

Every ASIN that moved is decomposed into four factors that multiply back to revenue exactly, so the explanation always adds up.

Part of **Amazon Management & Operations** in the
[TrackIQ skills catalog](https://github.com/TrackIQ-HQ/amazon-seller-skills).

Built as an [Agent Skill](https://code.claude.com/docs/en/skills). Runs in
Claude Code, Claude web, Claude desktop and ChatGPT from the same folder.

---

## Powered by the TrackIQ MCP

[![TrackIQ MCP — connect your AI assistant to Amazon data. 16 tools, full MCP access, $69/mo. Works with Claude, ChatGPT and Cursor.](.github/trackiq-mcp-banner.png)](https://trackiq.com/mcp)

This skill reads your live Amazon account through the
**[TrackIQ MCP](https://trackiq.com/mcp)** — 16 tools connecting your AI
assistant to Amazon data:

Sales & Traffic · Orders · Inventory · Returns · Sponsored Products · Sponsored
Brands · Sponsored Display · Amazon DSP · AMC Cloud · Keywords · Search Terms ·
Targeting · Search Query Performance · Organic Rank · Best Seller Rank · Buy Box
History · Brand Analytics · Export

Works with Claude, ChatGPT and Cursor. **[Get access →](https://trackiq.com/mcp)**

---

## What you get

![A TrackIQ: Amazon Sales Movers and Root Cause report](.github/preview.png)

Ranks an Amazon catalogue by how much each product's revenue moved between two periods and decomposes every mover into its cause — traffic, conversion rate, units per order, or average selling price — so the answer is "sessions fell 31%", not "sales are down". Use when the user asks why sales are down or up, what moved, which products changed, root cause, what happened last week, sales diagnosis, or why revenue dropped.

### The rules that keep it honest

- **`granularity="daily"` is silently ignored by `get_product_performance`**
- **The two windows must be the same length and the same weekdays**
- **Roll SKUs up to ASIN before comparing**
- **The four factors must multiply back to revenue exactly**

The full list is in `SKILL.md`, and each one exists because getting it wrong
produces a confident, wrong answer rather than an obvious error.

## Requirements

- The TrackIQ MCP, for `list_marketplaces`, `get_product_performance` and `get_account_overview`. - Nothing else. No filesystem, no shell, no internet. - **Without the MCP:** works from two Business Reports exports — one per period — with sessions, units, orders and revenue by ASIN.

---

## Install

### Claude Code

```
/plugin marketplace add TrackIQ-HQ/amazon-seller-skills
/plugin install trackiq-amazon-sales-movers@trackiq
```

### Claude web, desktop, mobile

1. Download the `.zip` from the
   [latest release](https://github.com/TrackIQ-HQ/trackiq-amazon-sales-movers/releases)
2. **Settings → Capabilities → Skills** (code execution must be on)
3. **Create skill → Upload a skill**, choose the `.zip`
4. Toggle it on

### ChatGPT

Same zip. **Plugins → Skills → Create → Upload from your computer.**

---

## Setup

Answers live in `account.md`, copied from
[`assets/account.example.md`](skills/trackiq-amazon-sales-movers/assets/account.example.md).
**Every TrackIQ skill reads the same file**, so an account already set up for
another TrackIQ report needs nothing added.

## Delivery

Asked once and stored in `account.md`: **in-chat** (default), **file**,
**Slack**, **n8n** or **email**. Anything leaving the chat confirms with you
first and falls back to in-chat, with a note.

---

## Customizing

| File | What it controls |
|---|---|
| `checks.md` | the pre-send checks |
| `decompose.py` | the bundled script |
| `method.md` | the method and every threshold |
| `pulls.md` | the call sequence and its traps |
| `report-template.html` | the report shell |

---

## Contributing

```bash
python scripts/validate.py    # must exit 0 before any commit
python scripts/build.py       # writes dist/ zip + registry.json
```

Read [AUTHORING.md](https://github.com/TrackIQ-HQ/amazon-seller-skills/blob/main/AUTHORING.md)
before proposing changes.

## License

MIT. See [LICENSE](LICENSE).

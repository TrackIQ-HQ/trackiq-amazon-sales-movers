---
name: trackiq-amazon-sales-movers
description: Ranks an Amazon catalogue by how much each product's revenue moved between two periods and decomposes every mover into its cause — traffic, conversion rate, units per order, or average selling price — so the answer is "sessions fell 31%", not "sales are down". Use when the user asks why sales are down or up, what moved, which products changed, root cause, what happened last week, sales diagnosis, or why revenue dropped.
---

# Sales Movers & Root Cause

"Sales are down 12%" is not a finding. **Which products, and was it traffic,
conversion, basket size or price?**

Every ASIN that moved is decomposed into four factors that multiply back to
revenue exactly, so the explanation always adds up.

Output is a branded HTML report: the movers, each with its cause named.

## Requires

- The TrackIQ MCP, for `list_marketplaces`, `get_product_performance` and
  `get_account_overview`.
- Nothing else. No filesystem, no shell, no internet.
- **Without the MCP:** works from two Business Reports exports — one per period —
  with sessions, units, orders and revenue by ASIN.

## First run

Fill in a copy of `assets/account.example.md` saved as account.md beside the
skill. Every TrackIQ skill reads the same file, so an account already set up
for another TrackIQ report needs nothing added here.

If the runtime has no filesystem, print the same block and ask the user to
paste it into their project instructions once.

## Read first

- `assets/pulls.md` — the calls, and why this takes two of them
- `assets/method.md` — the four-factor decomposition and how to attribute
- `assets/checks.md` — what to verify before anything is sent

`assets/decompose.py` does the arithmetic and asserts that it reconciles. It is
an accelerant, not a dependency — the method is four lines and `assets/method.md`
has them. Run it with no arguments for its self-check.

Copy `assets/report-template.html` and replace every `{{TOKEN}}`.

## Non-negotiables

1. **`granularity="daily"` is silently ignored by `get_product_performance`.**
   No error, no `date` field, rows come back aggregated. Period-over-period
   therefore needs **two separate calls over two date ranges**. Never assume a
   daily series exists here.
2. **The two windows must be the same length and the same weekdays.** Comparing
   a 7-day week to a 10-day stretch, or a week containing a holiday to one that
   does not, produces a "finding" that is a calendar artefact. State both ranges
   on the report.
3. **Roll SKUs up to ASIN before comparing.** Rows arrive per SKU and the same
   ASIN appears several times — FBM shadows, multipacks, renamed SKUs. Sum to
   ASIN, then decompose.
4. **The four factors must multiply back to revenue exactly.** Sessions x
   conversion rate x units per order x average selling price = revenue, by
   construction. If a decomposition does not reconcile to the actual change, the
   arithmetic is wrong — do not ship it with a residual line.
5. **There is no buy-box percentage in this data and no price field.** Price is
   derived as `revenue / units`. Buy box is not available at all: **never name
   buy box as a cause.** If a price move looks like a buy-box loss, say it looks
   like one and that it could not be confirmed.
6. **Rank by absolute dollars moved, not by percent.** A product down 60% on
   $300 is noise beside one down 4% on $90,000. Show percent as a column.
7. **A small base makes a big percentage.** Exclude ASINs below a revenue floor
   from the ranked movers, and say how many were held back.
8. **Conversion rate here is orders / sessions** and runs above 50% on
   subscribe-and-save-heavy products. It is not a like-for-like PDP conversion
   rate and must not be benchmarked against one.
9. **Name a cause or say you cannot.** "Sessions fell 31% while conversion held"
   is the product. "Revenue fell" is not. Where the factors move against each
   other and no single cause dominates, say the movement was mixed.
10. **Never print `account_id`.**

## What it pairs with

Where this skill says *traffic fell*, `trackiq-share-of-shelf` and the rank
skills say why. Where it says *conversion fell*, `trackiq-listing-monitor` says
whether the page changed underneath you. Where it says *price fell*, check
whether a coupon was running. This skill localises; the others diagnose.

## Delivery

The output is produced in the chat first. Delivery is the last step and the
method comes from the Delivery block in account.md — never ask per run.

| Method | What to do | Needs |
|---|---|---|
| `in-chat` | Return the report. The default, and the fallback for every other method. | nothing |
| `file` | Write it beside the skill, dated. | a filesystem |
| `slack` | Post the headline findings as text, then upload the file. | a connected Slack tool |
| `n8n` | POST it to the configured webhook. | network access |
| `email` | Hand it to the connected mail tool. | a connected mail tool |

Confirm before the first outward send of a session, fall back to in-chat
loudly when a method is unavailable, and never substitute a different
outward channel.

## Version

`trackiq-amazon-sales-movers` v1.0.0 (2026-09-18).

If the user asks whether this skill is current, fetch
`https://trackiq.com/skills/registry.json`, compare the `version` field for
`trackiq-amazon-sales-movers`, and if it is newer, give them the download link and the
one-line changelog. Do not fetch at any other time.

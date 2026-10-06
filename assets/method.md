# Method

## The identity

Revenue is exactly the product of four things:

```
revenue = sessions x conversion_rate x units_per_order x average_selling_price

  sessions               from the API
  conversion_rate  C  =  orders / sessions
  units_per_order  U  =  units / orders
  avg_selling_price P  =  revenue / units
```

Multiply them out and the `orders`, `units` terms cancel, leaving `revenue`.
That is the point: the decomposition cannot fail to reconcile, so there is never
a residual line to explain away.

Derive C, U and P yourself from `orders`, `units` and `revenue`. Do **not** use
the API's `conversion_rate` field for the arithmetic — use it only as a
cross-check. Deriving everything from the same three counts is what guarantees
the identity holds.

## The decomposition

Sequential substitution, swapping one factor at a time from the base period to
the current one:

```
traffic  = (S1 - S0) x C0 x U0 x P0
convert  =  S1 x (C1 - C0) x U0 x P0
basket   =  S1 x C1 x (U1 - U0) x P0
price    =  S1 x C1 x U1 x (P1 - P0)

traffic + convert + basket + price  ==  revenue1 - revenue0     exactly
```

**Assert that equality** before writing a row. If it fails by more than a cent,
something upstream is wrong — a SKU counted twice, a division by zero patched
with a default — and the row must not ship.

`assets/decompose.py` implements this with a self-check. It is an accelerant,
not a dependency: the four lines above are the whole method.

### The order matters, so state it

Sequential substitution attributes interaction effects to whichever factor is
swapped later. Traffic first, then conversion, then basket, then price is the
order used here, chosen because it runs from the least to the most controllable
by the listing itself.

A different order gives slightly different splits. That is a property of the
method, not a bug. Say which order was used in the method note so two runs are
comparable.

## Naming the cause

```
dominant = the factor with the largest absolute contribution
share    = abs(dominant) / sum of abs(all four)
```

| `share` | What to write |
|---|---|
| >= 0.6 | name it: "sessions fell 31%, conversion held" |
| 0.4–0.6 | name the top two |
| < 0.4 | "mixed — no single cause" and show the four numbers |

Never force a single cause onto a mixed movement. A report that always has an
answer stops being believed.

## What the causes usually mean

| Factor | Usually means | Where to look next |
|---|---|---|
| **Traffic** | rank, share of shelf, ad spend, seasonality, a stockout | `trackiq-share-of-shelf`, the rank skills |
| **Conversion** | the page changed, reviews moved, price is uncompetitive, out of stock | `trackiq-listing-monitor` |
| **Basket** | a multipack took over, or a promotion on quantity | variation mix |
| **Price** | a coupon, a promotion, a price change, or losing the buy box | see the caveat below |

**Buy box is not in this data.** There is no buy-box percentage field anywhere
in `get_product_performance`. A price move can look exactly like a buy-box loss
and this skill cannot tell them apart. Where price is the dominant factor and no
promotion is known, write that it *may* be a buy-box loss and needs checking in
the console. Never assert it.

## Which ASINs get ranked

```
floor = max($500, 0.5% of catalogue revenue in the base period)
```

Below the floor, a $200 product going to $80 is a 60% collapse and a rounding
error. Keep those rows in the full table, out of the ranked movers, and state
how many were held back.

**Rank by `abs(revenue1 - revenue0)` in dollars.** Percent is a column, never
the sort.

## The two windows

Same length, same weekdays, no holiday in one and not the other. Seven or
fourteen days is the useful range for a "what moved" question; twenty-eight
compares a month to a month and smooths out the thing being looked for.

Default: the last 7 complete days against the 7 before them.

State both ranges on the report, and end them at yesterday — today is partial
and will read as a collapse in traffic.

## Reconciling to the account

The sum of ASIN-level revenue changes should be close to the account's change
from `get_account_overview` over the same two windows. It will not match exactly
— the product feed excludes some revenue — so:

- Show both figures.
- If they differ by more than 10%, say so on the page and do not claim the
  ASIN list explains the account movement.

## What this skill does not do

- **No buy box.** Not available in this data.
- **No daily trend per ASIN.** `granularity="daily"` is ignored by this tool.
- **No forecast.** It explains what happened between two periods.
- **No advertising decomposition.** Ad spend moves traffic and this skill will
  attribute it to traffic; which campaign did it is a different question.

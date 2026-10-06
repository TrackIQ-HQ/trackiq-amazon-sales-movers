# The pull sequence

## 0. Account and the two windows

`list_marketplaces` first — several TrackIQ MCPs can be connected with
identical tool names. Never print `account_id`.

Pick two windows before pulling anything:

- **Same length.** Seven against seven, or fourteen against fourteen.
- **Same weekdays.** Sunday-to-Saturday against Sunday-to-Saturday. Amazon
  weekdays and weekends are different businesses.
- **Ending yesterday.** Today is partial and reads as a traffic collapse.
- **No holiday in one and not the other.** If there is, say so on the report
  rather than pretending the comparison is clean.

Default: the last 7 complete days against the 7 before them.

## 1. Two calls, because there is no daily series

```
get_product_performance(account_id, start_date=<base start>, end_date=<base end>,
                        group_by='product', limit=200)
get_product_performance(account_id, start_date=<curr start>, end_date=<curr end>,
                        group_by='product', limit=200)
```

**`granularity="daily"` does not work on this tool.** Passing it produces no
error and no `date` field — the rows come back aggregated exactly as if it had
not been passed. Silently ignored. So a period comparison is genuinely two
calls, and any attempt to build a daily trend per ASIN from this endpoint will
quietly produce a flat line.

Paginate each call until a page returns fewer rows than the limit.

## 2. The fields

```
product_id, asin, sku, title, link, image_thumbnail,
revenue, units, sessions, orders, conversion_rate
```

What is **not** there, and matters:

- **No price.** Derive it: `revenue / units`.
- **No buy-box percentage.** Not available at all. Never name buy box as a
  cause — see `assets/method.md`.
- **No inventory.** An ASIN whose traffic held and conversion collapsed may
  simply have gone out of stock. Cross-check with `get_inventory_snapshot` or
  `trackiq-restock-priority` before blaming the listing.

`conversion_rate` is `orders / sessions` and runs above 50% on
subscribe-and-save-heavy products. It is not a PDP conversion rate and must not
be compared to a category benchmark. Derive your own from `orders` and
`sessions` for the arithmetic and use the field only as a cross-check.

## 3. Roll up to ASIN

Rows come back **per SKU**. The same ASIN appears more than once — FBM shadows,
multipack SKUs, renamed SKUs from a listing migration.

Sum `revenue`, `units`, `sessions` and `orders` to ASIN, **then** derive the
rates. Deriving rates per SKU and averaging them is wrong and will not
reconcile.

Carry one title per ASIN — the longest, which is usually the live one.

## 4. The account check

```
get_account_overview(account_id, start_date, end_date)    # once per window
```

Sum `total_revenue` across each window. The sum of ASIN-level changes should be
close to the account change, but will not match exactly — the product feed does
not carry every dollar.

Show both. If they differ by more than 10%, say so and do not claim the ASIN
list explains the account movement.

## 5. Optional context, when a cause needs confirming

- `get_inventory_snapshot` — was it out of stock? This is the single most common
  real cause of a conversion collapse.
- `get_campaigns` over both windows — did ad spend move, explaining traffic?
- `get_bsr` — a point-in-time rank reading. **It has no history**: every row
  carries the same `tracked_date` whatever range is requested, so it cannot show
  rank movement across the two windows.

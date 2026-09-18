# Before you send it

## 1. The comparison is fair

- Both windows are the **same length** and cover the **same weekdays**.
- Both ranges are printed on the report.
- Neither window includes today.
- If a holiday or a Prime event sits in one and not the other, the report says so
  before showing any number.

## 2. The roll-up

- Sums were taken to **ASIN** before any rate was derived.
- No ASIN appears twice in the ranked list.
- Rates were derived from `orders`, `units`, `sessions` and `revenue` — not
  averaged from per-SKU rates.

## 3. The arithmetic reconciles

- **Every row's four factors sum to its revenue change, to the cent.** This is
  the check that matters; run `python assets/decompose.py` and confirm its
  self-check passes.
- No residual or "other" line appears anywhere.
- The attribution order (traffic, conversion, basket, price) is stated in the
  method note.

## 4. The causes are honest

- No row names **buy box** as a cause. It is not in this data.
- Where price dominates and no promotion is known, the report says it *may* be a
  buy-box loss and needs checking — it does not assert it.
- Rows where no factor reaches 40% of the movement are labelled **mixed**, with
  all four numbers shown.
- Conversion rate is not benchmarked against any external figure.
- Before blaming a listing for a conversion collapse, stock was checked. An ASIN
  that went out of stock is labelled as such.

## 5. The ranking

- Sorted by **absolute dollars moved**, not by percent.
- ASINs below the revenue floor are out of the ranked list, in the full table,
  and the count held back is stated.
- Top movers up and top movers down are both shown. A report that only shows
  losses gets read as pessimism rather than as analysis.

## 6. Reconciliation to the account

- The sum of ASIN changes and the account change from `get_account_overview` are
  both on the page.
- If they differ by more than 10%, the report says so and does not claim the
  ASIN list explains the account.

## 7. Render check

```js
({ overflows: document.documentElement.scrollWidth > document.documentElement.clientWidth,
   tables: document.querySelectorAll('table').length,
   rows: [...document.querySelectorAll('table')].map(t => t.querySelectorAll('tbody tr').length),
   logos: [...document.images].map(i => i.naturalWidth > 0),
   // must be zero: buy box is not in this data and must not appear as a cause
   buybox: (document.body.innerText.match(/buy box/gi) || []).length })
```

`overflows` false, `logos` all true. `buybox` may be 0, or 1 where the single
permitted caveat sentence appears — anything more means it leaked into the cause
column. Then look at it; if it will not paint, say the check was structural.

## 8. Ship

Save as `<client>-sales-movers-<YYYY-MM-DD>.html`.

Lead with the largest mover and its cause in one sentence — "grill covers down
$4,100, sessions fell 31% while conversion held" — not with the account total.
The account total is what they already knew.

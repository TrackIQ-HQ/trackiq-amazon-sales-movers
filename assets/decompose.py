"""Four-factor revenue decomposition for period-over-period movers.

An accelerant, never a dependency. The method is four lines and lives in
assets/method.md; this just guarantees they reconcile.

    revenue = sessions x conversion x units_per_order x avg_selling_price

Run with no arguments for the self-check:  python decompose.py
"""
import sys
import json

FACTORS = ("traffic", "convert", "basket", "price")


def factors(row):
    """sessions, conversion, units/order, price from the three raw counts."""
    s, o, u, r = (float(row["sessions"]), float(row["orders"]),
                  float(row["units"]), float(row["revenue"]))
    # A period with no sessions or no orders has no rate to speak of. Zero the
    # rate and let the surviving factors carry the whole move; the identity
    # still holds because revenue is zero on that side too.
    c = o / s if s else 0.0
    upo = u / o if o else 0.0
    p = r / u if u else 0.0
    return s, c, upo, p


def decompose(base, curr):
    """Sequential substitution: traffic, then conversion, then basket, then price.

    Returns {factor: dollars}. The four sum exactly to the revenue change.
    """
    s0, c0, u0, p0 = factors(base)
    s1, c1, u1, p1 = factors(curr)
    return {
        "traffic": (s1 - s0) * c0 * u0 * p0,
        "convert": s1 * (c1 - c0) * u0 * p0,
        "basket":  s1 * c1 * (u1 - u0) * p0,
        "price":   s1 * c1 * u1 * (p1 - p0),
    }


def cause(parts):
    """Name the dominant factor, or say the movement was mixed."""
    total = sum(abs(v) for v in parts.values())
    if total == 0:
        return "no movement", 0.0
    top = max(parts, key=lambda k: abs(parts[k]))
    share = abs(parts[top]) / total
    if share >= 0.6:
        return top, share
    if share >= 0.4:
        ranked = sorted(parts, key=lambda k: -abs(parts[k]))
        return "%s and %s" % (ranked[0], ranked[1]), share
    return "mixed", share


def reconcile(base, curr, parts, tol=0.01):
    """The identity must hold. A decomposition with a residual does not ship."""
    actual = float(curr["revenue"]) - float(base["revenue"])
    assert abs(sum(parts.values()) - actual) <= tol, (
        "decomposition does not reconcile: parts %.4f vs actual %.4f"
        % (sum(parts.values()), actual))
    return True


def run(rows):
    """rows: [{asin, base: {...}, curr: {...}}, ...] -> ranked movers."""
    out = []
    for r in rows:
        parts = decompose(r["base"], r["curr"])
        reconcile(r["base"], r["curr"], parts)
        name, share = cause(parts)
        out.append(dict(asin=r["asin"],
                        moved=float(r["curr"]["revenue"]) - float(r["base"]["revenue"]),
                        cause=name, share=round(share, 3),
                        **{k: round(v, 2) for k, v in parts.items()}))
    return sorted(out, key=lambda x: -abs(x["moved"]))


def demo():
    # Traffic collapses, everything else holds: the whole move must land on traffic.
    base = dict(sessions=10000, orders=500, units=600, revenue=12000)
    curr = dict(sessions=6900, orders=345, units=414, revenue=8280)
    parts = decompose(base, curr)
    reconcile(base, curr, parts)
    name, share = cause(parts)
    assert name == "traffic", name
    assert share > 0.99, share
    assert abs(parts["convert"]) < 0.01 and abs(parts["price"]) < 0.01

    # Price alone: same sessions, orders and units, less money.
    base = dict(sessions=5000, orders=250, units=250, revenue=5000)
    curr = dict(sessions=5000, orders=250, units=250, revenue=4000)
    parts = decompose(base, curr)
    reconcile(base, curr, parts)
    assert cause(parts)[0] == "price"
    assert abs(parts["price"] - (-1000)) < 0.01

    # Two factors pulling against each other must still reconcile exactly.
    base = dict(sessions=8000, orders=400, units=500, revenue=10000)
    curr = dict(sessions=12000, orders=360, units=430, revenue=9500)
    parts = decompose(base, curr)
    reconcile(base, curr, parts)
    assert parts["traffic"] > 0 and parts["convert"] < 0

    # An ASIN that went to zero. No crash, and the identity still holds.
    base = dict(sessions=3000, orders=150, units=150, revenue=3000)
    curr = dict(sessions=0, orders=0, units=0, revenue=0)
    parts = decompose(base, curr)
    reconcile(base, curr, parts)

    # Ranking is by absolute dollars, not percent.
    ranked = run([
        {"asin": "SMALL", "base": dict(sessions=100, orders=10, units=10, revenue=300),
         "curr": dict(sessions=40, orders=4, units=4, revenue=120)},          # -60%
        {"asin": "BIG", "base": dict(sessions=90000, orders=4500, units=4500, revenue=90000),
         "curr": dict(sessions=86400, orders=4320, units=4320, revenue=86400)},  # -4%
    ])
    assert ranked[0]["asin"] == "BIG", "must rank on dollars, not percent"
    print("self-check passed")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(json.dumps(run(json.load(open(sys.argv[1], encoding="utf-8"))), indent=2))
    else:
        demo()

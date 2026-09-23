"""Pin the numbers quoted in the paper. Run with ``pytest`` or as a script."""
from math import comb, isclose, log

from mta.theory import (P_agg, P_vis, M, K_star, D, Rate_agg, Rate_vis,
                        r_star, RATE_CROSSOVER_BOUNDARY, K_MIN_SPLIT)


def test_point_values():
    assert round(P_agg(10, 0.7), 3) == 0.901
    assert round(P_vis(10, 0.7), 3) == 0.851
    assert round(P_vis(20, 0.9), 3) == 0.608          # main text: about 61%
    assert round(r_star(0.7), 3) == 0.124


def test_disclosure_reference_scale():
    assert K_star(0.6) == 6
    assert K_star(0.65) == 8
    assert K_star(0.7) == 14
    assert K_star(0.75) == 32
    assert K_star(0.78) == 102
    assert K_star(0.79) == 238
    assert K_star(0.795) == 550


def test_strict_tie_breaking():
    assert K_star(0.7, tie="strict") == 10
    assert K_star(0.6, tie="strict") == 6
    assert K_star(0.75, tie="strict") == 28
    for p in (0.6, 0.65, 0.7, 0.75):
        assert K_star(p, tie="strict") <= K_star(p)
    assert P_agg(10, 0.7, tie="strict") < P_agg(10, 0.7)
    assert P_agg(11, 0.7, tie="strict") == P_agg(11, 0.7)   # odd K: no tie


def test_no_crossover_at_and_above_the_boundary():
    assert RATE_CROSSOVER_BOUNDARY == 0.8
    assert K_star(0.8) is None
    assert K_star(0.85) is None
    assert K_star(0.99) is None
    assert P_agg(100, 0.8) > P_vis(100, 0.8)
    assert isclose(P_agg(100, 0.8) - P_vis(100, 0.8), 5.28e-9, rel_tol=1e-2)


def test_kstar_search_failure_raises():
    try:
        K_star(0.79, Kmax=50)
    except RuntimeError:
        pass
    else:
        raise AssertionError("exhausting Kmax below 4/5 must raise")


def test_pvis_domain_below_four():
    assert K_MIN_SPLIT == 4
    for K in (0, 1, 2, 3):
        assert P_vis(K, 0.7) == 0.0
    p, q = 0.7, 0.3
    assert 1 - q * (2 * p + q) - p * (2 * q + p) < 0   # the raw formula at K = 2
    assert P_vis(4, 0.7) > 0


def test_pvis_symmetry_and_limit():
    for K in (4, 7, 12, 25):
        assert isclose(P_vis(K, 0.7), P_vis(K, 0.3), abs_tol=1e-12)
    assert P_vis(200, 0.7) > 0.999


def test_dissenting_fraction_to_q():
    for p in (0.6, 0.7, 0.8):
        assert isclose(M(60, p) / 60, 1 - p, abs_tol=0.02)


def test_rates_and_boundary():
    assert isclose(Rate_vis(1e-9, 0.7), log(1 / 0.7), abs_tol=1e-6)
    assert isclose(D(0.7, 0.7), 0.0, abs_tol=1e-12)
    assert r_star(0.8) == 0.0
    assert r_star(0.85) == 0.0
    assert r_star(0.7) > 0.0
    assert Rate_vis(1e-9, 0.7) > Rate_agg(0.7)
    assert Rate_vis(1e-9, 0.85) < Rate_agg(0.85)


def test_note6_all_wrong_rates():
    """Supplementary Note 6: one all-wrong item in ~2,000 (rho=0.2) and ~66
    (rho=0.5) at p=0.7, K=14, read from the pinned simulation CSV."""
    q = 1 - 0.7
    assert isclose(q ** 14, 4.783e-8, rel_tol=1e-3)
    import csv
    import os
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "data", "raw", "figS2_nullmodel.csv")
    if not os.path.exists(path):
        print("  (simulation CSV not present; correlated pins skipped)")
        return
    with open(path) as f:
        k14 = next(r for r in csv.DictReader(f) if r["K"] == "14")
    assert round(1 / float(k14["allwrong_0.5"])) == 66
    assert 1900 < 1 / float(k14["allwrong_0.2"]) < 2200


def test_conditional_accuracy():
    """Main text: at p=0.7, K=14, P_agg = 0.938 but 0.845 given an 8-6 split."""
    p, q, K = 0.7, 0.3, 14
    assert round(P_agg(K, p), 3) == 0.938
    pmf = lambda y: comb(K, y) * p ** y * q ** (K - y)
    cond = pmf(8) / (pmf(8) + pmf(6))
    assert round(cond, 3) == 0.845
    assert isclose(cond, 1 / (1 + (q / p) ** 2), rel_tol=1e-12)


def test_note6_counterexamples():
    """Supplementary Note 6: exchangeable panels with positive pairwise
    correlation that split more (K=4) or vote more accurately (K=3) than
    independence, given as distributions of Y."""
    def stats(K, dist):
        p = sum(y * w for y, w in dist.items()) / K
        p11 = sum(w * y * (y - 1) / (K * (K - 1)) for y, w in dist.items())
        return p, (p11 - p * p) / (p * (1 - p))
    p, rho = stats(4, {4: 0.5, 2: 0.4, 0: 0.1})
    assert isclose(p, 0.7) and round(rho, 2) == 0.37
    assert round(P_vis(4, 0.7), 2) == 0.26                   # vs 0.40 (Y = 2)
    p, rho = stats(3, {3: 0.5, 2: 0.3, 0: 0.2})
    assert isclose(p, 0.7) and round(rho, 2) == 0.52
    assert round(P_agg(3, 0.7), 3) == 0.784                  # vs 0.80 (Y >= 2)


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"ok: {fn.__name__}")
    print(f"all {len(fns)} theory tests passed")

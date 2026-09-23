"""Closed forms for a panel of K independent advisers, each correct with
probability p > 1/2 (Y ~ Binomial(K, p) correct votes).

Binomial sums are evaluated in log space so that the residuals 1 - P_agg and
1 - P_vis stay resolvable at large K, where the probabilities themselves round
to 1.0 in float64.
"""
from math import lgamma, log, exp, inf

#: Adviser accuracy at which the two convergence rates cross; no finite K*
#: exists at or above it (Supplementary Note 5).
RATE_CROSSOVER_BOUNDARY = 0.8

#: Smallest panel on which a split (>= 2 dissenters on each side) can occur.
K_MIN_SPLIT = 4


def _logsumexp(xs):
    xs = [x for x in xs if x != -inf]
    if not xs:
        return -inf
    m = max(xs)
    return m + log(sum(exp(x - m) for x in xs))


def _logcomb(K, k):
    return lgamma(K + 1) - lgamma(k + 1) - lgamma(K - k + 1)


def _logbinom(K, k, lp, lq):
    return _logcomb(K, k) + k * lp + (K - k) * lq


def _check_tie(tie):
    if tie not in ("fair", "strict"):
        raise ValueError(f"tie must be 'fair' or 'strict', got {tie!r}")


def P_agg(K, p, tie="fair"):
    """Majority accuracy. tie="fair": a tied panel is correct with probability
    1/2 (the paper's convention); tie="strict": a tie counts as incorrect."""
    _check_tie(tie)
    q = 1.0 - p
    lp, lq = log(p), log(q)
    s = exp(_logsumexp([_logbinom(K, k, lp, lq) for k in range(K // 2 + 1, K + 1)]))
    if K % 2 == 0 and tie == "fair":
        s += 0.5 * exp(_logbinom(K, K // 2, lp, lq))
    return min(1.0, s)          # guard float noise at large K


def P_vis(K, p):
    """Probability of visible dissent (>= 2 advisers on each side):
    1 - q^(K-1)(Kp + q) - p^(K-1)(Kq + p)."""
    # The closed form is only meaningful for K >= 4 (at K = 2 it exceeds 1).
    if K < K_MIN_SPLIT:
        return 0.0
    q = 1.0 - p
    val = 1.0 - q**(K - 1) * (K * p + q) - p**(K - 1) * (K * q + p)
    return max(0.0, val)


def P_any(K, p):
    """Probability of any disagreement: 1 - p^K - q^K."""
    q = 1.0 - p
    return 1.0 - p**K - q**K


def M(K, p):
    """Expected minority size E[min(Y, K - Y)]; the dissenting fraction is M/K."""
    q = 1.0 - p
    lp, lq = log(p), log(q)
    total = 0.0
    for y in range(K + 1):
        w = min(y, K - y)
        if w > 0:
            total += w * exp(_logbinom(K, y, lp, lq))
    return total


def log1m_P_vis(K, p):
    """log(1 - P_vis(K, p))."""
    q = 1.0 - p
    a = (K - 1) * log(q) + log(K * p + q)
    b = (K - 1) * log(p) + log(K * q + p)
    return _logsumexp([a, b])


def log1m_P_agg(K, p, tie="fair"):
    """log(1 - P_agg(K, p, tie))."""
    _check_tie(tie)
    q = 1.0 - p
    lp, lq = log(p), log(q)
    half = K // 2
    if K % 2 == 1:
        return _logsumexp([_logbinom(K, k, lp, lq) for k in range(0, half + 1)])
    lower = _logsumexp([_logbinom(K, k, lp, lq) for k in range(0, half)])
    tie_term = _logbinom(K, half, lp, lq)
    if tie == "fair":
        tie_term += log(0.5)
    return _logsumexp([lower, tie_term])


def K_star(p, tie="fair", Kmax=3000):
    """Disclosure reference scale: the smallest K with P_vis >= P_agg.

    Returns None for p >= 4/5, where no finite crossover exists (proved in
    Supplementary Note 5, so no search is run). Below 4/5 a crossover must
    exist, so exhausting Kmax raises RuntimeError instead of returning None.
    """
    _check_tie(tie)
    if p >= RATE_CROSSOVER_BOUNDARY:
        return None
    for K in range(K_MIN_SPLIT, Kmax + 1):
        if log1m_P_vis(K, p) <= log1m_P_agg(K, p, tie):
            return K
    raise RuntimeError(f"no crossover found for p={p} (tie={tie}) up to Kmax={Kmax}; raise Kmax")

"""Large-deviation convergence rates and the speed boundary r*(p)."""
from math import log

from scipy.optimize import brentq

from .condorcet import RATE_CROSSOVER_BOUNDARY


def D(x, p):
    """Bernoulli KL divergence D(x || p), with 0 log 0 = 0."""
    q = 1.0 - p
    def xl(a, b):
        return 0.0 if a <= 0 else a * log(a / b)
    return xl(x, p) + xl(1.0 - x, q)


def Rate_agg(p):
    """Error exponent of the majority: (1/2) log(1 / 4pq)."""
    q = 1.0 - p
    return 0.5 * log(1.0 / (4.0 * p * q))


def Rate_vis(r, p):
    """Exponent of the r-form of visible dissent (a fraction >= r on each side): D(1 - r || p)."""
    return D(1.0 - r, p)


def r_star(p):
    """Root of Rate_vis(r, p) = Rate_agg(p); 0 for p >= 4/5."""
    if p >= RATE_CROSSOVER_BOUNDARY:
        return 0.0
    q = 1.0 - p
    return brentq(lambda r: Rate_vis(r, p) - Rate_agg(p), 1e-9, q - 1e-9)

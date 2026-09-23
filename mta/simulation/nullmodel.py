"""Gaussian-copula null model behind Fig. S2.

K advisers each correct with marginal probability p, their errors coupled
through a single-factor Gaussian copula of correlation rho.
"""
import numpy as np
from scipy.special import ndtri


def panel_stats(rng, K, p, rho, N):
    """Observed rates over N panels: (visible dissent 2 <= Y <= K-2, all wrong Y = 0)."""
    thr = ndtri(p)
    Z = np.sqrt(rho) * rng.standard_normal((N, 1)) + np.sqrt(1 - rho) * rng.standard_normal((N, K))
    Y = (Z < thr).sum(1)
    return ((Y >= 2) & (Y <= K - 2)).mean(), (Y == 0).mean()


def simulate(seed=7, N=400_000, p=0.7, Ks=range(4, 31), rhos=(0.2, 0.5),
             extra_Ks=(2, 3)):
    """Run the (K, rho) grid; returns one dict per K with the observed rates."""
    rng = np.random.default_rng(seed)
    # Draw order is fixed (rho-major, then K; the extra small panels last) so
    # that the published K >= 4 rates do not change when the grid is extended.
    stats = {rho: {K: panel_stats(rng, K, p, rho, N) for K in Ks}
             for rho in rhos}
    for K in extra_Ks:
        for rho in rhos:
            stats[rho][K] = panel_stats(rng, K, p, rho, N)
    return [
        {"K": K, "p": p,
         **{f"rho_{rho}": stats[rho][K][0] for rho in rhos},
         **{f"allwrong_{rho}": stats[rho][K][1] for rho in rhos}}
        for K in sorted(set(Ks) | set(extra_Ks))
    ]

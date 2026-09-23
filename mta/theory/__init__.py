"""Analytical closed forms (the single source of truth)."""
from .condorcet import (P_agg, P_vis, P_any, M, K_star, log1m_P_vis, log1m_P_agg,
                        RATE_CROSSOVER_BOUNDARY, K_MIN_SPLIT)
from .rates import D, Rate_agg, Rate_vis, r_star

__all__ = ["P_agg", "P_vis", "P_any", "M", "K_star", "log1m_P_vis", "log1m_P_agg",
           "RATE_CROSSOVER_BOUNDARY", "K_MIN_SPLIT",
           "D", "Rate_agg", "Rate_vis", "r_star"]

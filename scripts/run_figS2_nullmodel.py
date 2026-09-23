"""Fig. S2, step 1: run the null-model simulation -> data/raw/figS2_nullmodel.csv."""
import csv
import os

from mta import ROOT
from mta.simulation import simulate

OUT = os.path.join(ROOT, "data", "raw", "figS2_nullmodel.csv")


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    rows = simulate()
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"saved: {OUT}  ({len(rows)} rows)")


if __name__ == "__main__":
    main()

import glob
import sys


import pandas as pd


def main(fname):
    tables = glob.glob(f"../outputs/{'_'.join(fname.split('_')[:2])}*_stats.csv")
    scores = pd.concat([pd.read_csv(table) for table in tables])
    scores["text"] = scores["text"].str.replace(";; ", "")
    scores["js_distance"] = scores["js_distance"].apply(lambda x: f"{x:.3f}")
    scores["pval_fdr"] = scores["pval_fdr"].apply(
        lambda x: f"{x:.3f} *" if x < 0.05 else f"{x:.3f}"
    )
    scores = scores.loc[:, ["text", "js_distance", "pval_fdr"]].rename(
        columns={
            "text": "Sentence",
            "js_distance": "JSD",
            "pval_fdr": "p-value",
        }
    )
    scores.to_latex(f"../outputs/{fname}", index=False)


if __name__ == "__main__":
    main(sys.argv[1])

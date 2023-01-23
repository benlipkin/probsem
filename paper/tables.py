import re
import glob
import sys


import pandas as pd
import statsmodels.stats.multitest


def main(fname):
    tables = glob.glob(f"../outputs/{'_'.join(fname.split('_')[:2])}*_stats.csv")
    scores = pd.concat([pd.read_csv(table) for table in tables])
    scores["text"] = (
        scores["text"]
        .str.replace(";; ", "")
        .apply(lambda x: r"parbox{5cm}{" + f"{x}" + r"}")
    )
    scores["js_distance"] = scores["js_distance"].apply(lambda x: f"{x:.3f}")
    scores["pval_fdr"] = statsmodels.stats.multitest.multipletests(
        scores["pval"], method="fdr_bh"
    )[1]
    scores["pval_fdr"] = scores["pval_fdr"].apply(
        lambda x: f"STARTBOLD{x:.3f} *ENDBOLD" if x < 0.05 else f"{x:.3f}"
    )
    scores = scores.loc[:, ["text", "js_distance", "pval_fdr"]].rename(
        columns={
            "text": "Sentence",
            "js_distance": "JSD",
            "pval_fdr": "p-value",
        }
    )
    with pd.option_context("max_colwidth", 1000):
        latex = scores.to_latex(index=False)
    latex = (
        latex.replace("STARTBOLD", r"\textbf{")
        .replace("ENDBOLD", "}")
        .replace("0.000", "$<$0.001")
    )
    latex = (
        latex.replace("lll", "p{5cm}ll")
        .replace("parbox", r"\parbox")
        .replace(r"\{", "{")
        .replace(r"\}", "}")
        .replace("Jack", r"``Jack")
        .replace(r".}", r'."}\vspace{1mm}')
    )
    latex = (
        latex.replace(r"\toprule", r"\hline")
        .replace(r"\midrule", r"\hline")
        .replace(r"\bottomrule", r"\hline")
    )
    latex = re.sub("\s+", " ", latex)
    with open(f"../outputs/{fname}", "w") as f:
        f.write(latex)


if __name__ == "__main__":
    main(sys.argv[1])

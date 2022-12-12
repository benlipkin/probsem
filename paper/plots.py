import itertools
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def make_av_plot(av_suite):
    table = pd.read_csv(f"../outputs/{av_suite}_results.csv")
    fig, axes = plt.subplots(3, 3, figsize=(10, 6), sharex=True, sharey=True)
    for i, j in itertools.product(range(3), range(3)):
        ax = axes[i, j]
        n = i * 3 + j
        text = table["text"].unique()[[0, 4, 5, 2, 3, 1, 6, 7, 8][n]]
        samples = table[table["text"] == text]
        assert np.abs(1.0 - samples["score"].sum()) < 1e-6
        theta = samples["program"].str[31:33].astype(int).values
        ax.bar(theta, samples["score"], width=10, color="darkgreen", edgecolor="black")
        args = {"fontname": "serif", "fontweight": "bold"}
        ax.set_xticks(
            np.arange(10, 91, 10),
            labels=np.arange(10, 91, 10),
            rotation=45,
            fontsize=10,
            **args,
        )
        ax.set_yticks(
            np.arange(0, 1.1, 0.25),
            labels=["0", "0.25", "0.50", "0.75", "1.00"],
            fontsize=10,
            **args,
        )
        ax.set_title(text.strip("; "), fontsize=14, **args)
        ax.set_xlabel(r"$\theta$", fontsize=12, **args) if i == 2 else None
        ax.set_ylabel("Probability Mass", fontsize=12, **args) if j == 0 else None
        for spine in ["top", "right", "left"]:
            ax.spines[spine].set_visible(False)
    fig.tight_layout()
    fig.savefig(f"../outputs/{av_suite}_plot.png", dpi=600)
    plt.close()


def make_pp_plot(pp_suite):
    table = pd.read_csv(f"../outputs/{pp_suite.replace('_c','b_c')}_results.csv")
    fig, axes = plt.subplots(2, 4, figsize=(7, 5), sharex=True, sharey=True)
    for i, j in itertools.product(range(2), range(4)):
        ax = axes[i, j]
        n = i * 4 + j
        text = table["text"].unique()[[0, 2, 4, 6, 1, 3, 5, 7][n]]
        samples = table[table["text"] == text]
        assert np.abs(1.0 - samples["score"].sum()) < 1e-6
        modifier = (
            (samples["text"] + ",baseline")
            .str.split(",")
            .str[1]
            .str.strip(" .")
            .values[0]
            .capitalize()
        )
        interpretation = ["Collective", "Distributive"]
        ax.bar(interpretation, samples["score"], color="darkgreen", edgecolor="black")
        args = {"fontname": "serif", "fontweight": "bold"}
        ax.set_xticks(
            range(2),
            labels=interpretation,
            rotation=45,
            fontsize=10,
            **args,
        )
        ax.set_yticks(
            np.arange(0, 1.1, 0.25),
            labels=["0", "0.25", "0.50", "0.75", "1.00"],
            fontsize=10,
            **args,
        )
        ax.set_title(f"{modifier}", fontsize=14, **args)
        ax.set_xlabel("Interpretation", fontsize=12, **args) if i == 2 else None
        ax.set_ylabel("Probability Mass", fontsize=12, **args) if j == 0 else None
        for spine in ["top", "right", "left"]:
            ax.spines[spine].set_visible(False)
    text = table["text"][0].replace("together", "<INSERT>").strip("; ")
    collective = f"Collective: {table.program.unique()[0]}"
    distributive = f"Distributive: {table.program.unique()[1]}"
    title = "\n".join([text, "", collective, distributive])
    fig.suptitle(title, fontsize=8, **args)
    fig.tight_layout()
    fig.savefig(f"../outputs/{pp_suite}_plot.png", dpi=600)
    plt.close()


def make_pp_plot2(pp_suite):
    table = pd.read_csv(f"../outputs/{pp_suite.replace('_c','c_c')}_results.csv")
    fig, axes = plt.subplots(2, 2, figsize=(8, 5), sharex=True, sharey=True)
    for i, j in itertools.product(range(2), range(2)):
        ax = axes[i, j]
        n = i * 2 + j
        text = table["text"].unique()[[0, 2, 1, 3][n]]
        samples = table[table["text"] == text]
        assert np.abs(1.0 - samples["score"].sum()) < 1e-6
        interpretation = ["Collective", "Distributive"]
        ax.bar(interpretation, samples["score"], color="darkgreen", edgecolor="black")
        args = {"fontname": "serif", "fontweight": "bold"}
        ax.set_xticks(
            range(2),
            labels=interpretation,
            rotation=45,
            fontsize=10,
            **args,
        )
        ax.set_yticks(
            np.arange(0, 1.1, 0.25),
            labels=["0", "0.25", "0.50", "0.75", "1.00"],
            fontsize=10,
            **args,
        )
        ax.set_title(text.replace(";; ", "").split("\n")[0], fontsize=7, **args)
        ax.set_xlabel("Interpretation", fontsize=12, **args) if i == 2 else None
        ax.set_ylabel("Probability Mass", fontsize=12, **args) if j == 0 else None
        for spine in ["top", "right", "left"]:
            ax.spines[spine].set_visible(False)
    title = "<INSERT>\n" + text.replace(";; ", "").split("\n")[1]
    fig.suptitle(title, fontsize=12, **args)
    fig.tight_layout()
    fig.savefig(f"../outputs/{pp_suite}_plot2.png", dpi=600)
    plt.close()


def main(suite):
    if suite in [
        "tug-of-war_AV-1_code-davinci-002",
        "tug-of-war_AV-2_code-davinci-002",
    ]:
        make_av_plot(suite)
    elif suite in [
        "tug-of-war_PP-1_code-davinci-002",
        "tug-of-war_PP-2_code-davinci-002",
    ]:
        make_pp_plot(suite)
        make_pp_plot2(suite)
    else:
        raise ValueError(f"Unknown suite: {suite}")


if __name__ == "__main__":
    main(sys.argv[1])

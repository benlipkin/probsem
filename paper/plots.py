import itertools

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def make_av_plot(data, name):
    fig, axes = plt.subplots(3, 3, figsize=(10, 6), sharex=True, sharey=True)
    for i, j in itertools.product(range(3), range(3)):
        for k, source in enumerate(data["source"].unique()):
            ax = axes[i, j]
            n = i * 3 + j
            text = data["text"].unique()[[4, 0, 5, 2, 3, 1, 6, 7, 8][n]]
            samples = data[data["text"] == text]
            samples = samples[samples["source"] == source]
            assert np.abs(1.0 - samples["prob"].sum()) < 1e-6
            ax.bar(
                samples["theta"],
                samples["prob"],
                width=10,
                color=["darkgreen", "darkblue"][k],
                edgecolor="black",
                alpha=0.5,
                label=source.capitalize(),
            )
            ax.set_ylim(0, 1.05)
            args = {"fontname": "serif", "fontweight": "bold"}
            ax.set_xticks(
                np.arange(0, 101, 10),
                labels=np.arange(0, 101, 10),
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
        if not i + j:
            ax.legend(
                loc="upper left",
                fontsize=12,
                frameon=False,
                prop={"family": "serif", "weight": "bold"},
            )
    fig.tight_layout()
    fig.savefig(f"../outputs/tug-of-war_AV-1_{name}_plot.png", dpi=600)
    plt.close()


def main():
    data = pd.read_csv("../outputs/tug-of-war_AV-1_data.csv")
    strong_filter = (
        (data["text"].str.contains("strong") & ~data["text"].str.contains("not"))
        | (data["text"].str.contains("not") & data["text"].str.contains("weak"))
        | (data["text"].str.contains("least"))
    )
    weak_filter = (
        (data["text"].str.contains("weak") & ~data["text"].str.contains("not"))
        | (data["text"].str.contains("not") & data["text"].str.contains("strong"))
        | (data["text"].str.contains("most"))
    )
    make_av_plot(data[strong_filter], "strong")
    make_av_plot(data[weak_filter], "weak")


if __name__ == "__main__":
    main()

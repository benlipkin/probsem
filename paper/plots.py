import itertools
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def make_av_plot(data, fname, dims):
    fig, axes = plt.subplots(
        dims[0], dims[1], figsize=(3 * dims[1], 2 * dims[0]), sharex=True, sharey=True
    )
    for i, j in itertools.product(range(dims[0]), range(dims[1])):
        for k, source in enumerate(data["source"].unique()[::-1]):
            ax = axes[i, j]
            n = i * dims[1] + j
            text = data["text"].unique()
            idx = [4, 0, 5, 2, 3, 1, 6, 7, 8][n] if "AV-1" in fname else n
            text = text[idx]
            samples = data[data["text"] == text]
            samples = samples[samples["source"] == source]
            assert np.abs(1.0 - samples["prob"].sum()) < 1e-6
            ax.bar(
                samples["theta"],
                samples["prob"],
                width=10,
                color=["tab:blue", "darkgreen"][k],
                edgecolor="black",
                alpha=[1.0, 0.7][k],
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
            ax.set_title(
                text.strip("; ").replace(" for ", "\nfor ").replace(" of ", "\nof "),
                fontsize=10,
                **args,
            )
            ax.set_xlabel(r"$\theta$", fontsize=12, **args) if i == 2 else None
            ax.set_ylabel("Probability Mass", fontsize=12, **args) if j == 0 else None
            for spine in ["top", "right", "left"]:
                ax.spines[spine].set_visible(False)
        if not i + j:
            ax.legend(
                loc="upper right",
                fontsize=12,
                frameon=False,
                prop={"family": "serif", "weight": "bold"},
            )
    fig.tight_layout()
    fig.savefig(f"../outputs/{fname}", dpi=600)
    plt.close()


def main(fname):
    data = pd.read_csv(f"../outputs/{fname.replace('_plot.png', '_data.csv')}")
    dims = [3, 3] if "AV-1" in fname else [2, 3]
    make_av_plot(data, fname, dims)


if __name__ == "__main__":
    main(sys.argv[1])

import collections

import numpy as np
import pandas as pd

import scipy
import scipy.optimize
import statsmodels.stats.multitest

np.random.seed(0)

metric = scipy.spatial.distance.jensenshannon


def load_model_data():
    data = pd.concat(
        (
            pd.read_csv("../outputs/tug-of-war_AV-1a_code-davinci-002_results.csv"),
            pd.read_csv("../outputs/tug-of-war_AV-1b_code-davinci-002_results.csv"),
        )
    )
    data["theta"] = data["program"].str[31:34].str.strip(")").astype(float).values
    return data


def load_human_data():
    data = pd.read_csv("tug-of-war_AV-1_human_results.csv").set_index("subject_id")
    counts = collections.defaultdict(list)
    for sentence in data.columns:
        samples = data[sentence].values
        for theta in np.linspace(0, 100, 11):
            counts["text"].append(f";; {sentence.capitalize()}.")
            counts["theta"].append(theta)
            counts["count"].append(np.sum(samples == theta))
    return pd.DataFrame(counts)


def calc_human_probs(data):
    for sentence in data["text"].unique():
        samples = data.loc[data["text"] == sentence]
        weights = np.array(samples["count"]).astype(float)
        probs = weights / weights.sum()
        data.loc[data["text"] == sentence, "prob"] = probs
    return data


def norm_model_probs(model_data, human_data):
    def normalize(weights):
        return np.exp(weights) / np.sum(np.exp(weights))

    def optim_loss(train_model_samples, train_human_samples, temperature):
        loss = 0
        for sentence in train_model_samples["text"].unique():
            model_samples = train_model_samples.loc[
                train_model_samples["text"] == sentence, :
            ]
            human_samples = train_human_samples.loc[
                train_human_samples["text"] == sentence, :
            ]
            model_probs = normalize(model_samples["weights"].values / temperature)
            human_probs = human_samples["prob"].values
            loss += metric(human_probs, model_probs)
        return loss

    for sentence in model_data["text"].unique():
        train_model_samples = model_data.loc[model_data["text"] != sentence, :]
        train_human_samples = human_data.loc[human_data["text"] != sentence, :]
        test_model_samples = model_data.loc[model_data["text"] == sentence, :]

        x0 = np.array([1.0])
        f = lambda x: optim_loss(train_model_samples, train_human_samples, x)
        temperature = scipy.optimize.fmin(f, x0, disp=False)[0]

        model_probs = normalize(test_model_samples["weights"].values / temperature)
        model_data.loc[model_data["text"] == sentence, "temperature"] = temperature
        model_data.loc[model_data["text"] == sentence, "prob"] = model_probs
    return model_data


def compare_distributions(model_data, human_data):
    scores = collections.defaultdict(list)
    for sentence in model_data["text"].unique():
        model_table = model_data.loc[model_data["text"] == sentence, :]
        human_table = human_data.loc[human_data["text"] == sentence, :]
        model_probs = model_table.sort_values("theta")["prob"].values
        human_probs = human_table.sort_values("theta")["prob"].values
        js_distance = metric(human_probs, model_probs)
        null_distances = np.array(
            [
                metric(
                    human_probs[np.random.permutation(human_probs.size)],
                    model_probs[np.random.permutation(model_probs.size)],
                )
                for _ in range(10000)
            ]
        )
        pval = np.sum(null_distances <= js_distance) / null_distances.size
        scores["text"].append(sentence)
        scores["temperature"].append(model_table["temperature"].values[0])
        scores["js_distance"].append(js_distance)
        scores["pval"].append(pval)
    scores["pval_fdr"] = statsmodels.stats.multitest.multipletests(
        scores["pval"], method="fdr_bh"
    )[1]
    scores["significant"] = (scores["pval_fdr"] < 0.05).astype(int)
    return pd.DataFrame(scores)


def merge_data(model_data, human_data):
    model_data["source"] = "model"
    human_data["source"] = "human"
    return pd.concat(
        (
            t.loc[:, ["source", "text", "theta", "prob"]]
            for t in (model_data, human_data)
        )
    )


def export_scores(scores):
    scores.to_csv("../outputs/tug-of-war_AV-1_stats.csv", index=False)
    scores["text"] = scores["text"].str.replace(";; ", "")
    scores["js_distance"] = scores["js_distance"].apply(lambda x: f"{x:.3f}")
    scores["pval_fdr"] = scores["pval_fdr"].apply(
        lambda x: f"{x:.3f} *" if x < 0.05 else f"{x:.3f}"
    )
    scores.loc[:, ["text", "js_distance", "pval_fdr"]].rename(
        columns={
            "text": "Sentence",
            "js_distance": "Jensen-Shannon Distance",
            "pval_fdr": "FDR p-value",
        }
    ).to_latex("../outputs/tug-of-war_AV-1_stats.tex", index=False)


def main():
    human_data = calc_human_probs(load_human_data())
    model_data = norm_model_probs(load_model_data(), human_data)
    merge_data(model_data, human_data).to_csv(
        "../outputs/tug-of-war_AV-1_data.csv", index=False
    )
    export_scores(compare_distributions(model_data, human_data))


if __name__ == "__main__":
    main()

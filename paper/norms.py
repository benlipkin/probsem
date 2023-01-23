import collections
import sys

import numpy as np
import pandas as pd

import scipy
import scipy.optimize
import statsmodels.stats.multitest

np.random.seed(0)

metric = scipy.spatial.distance.jensenshannon


def load_model_data(fname):
    data = pd.read_csv(f"../outputs/{fname.replace('data','results')}")
    data["theta"] = data["program"].str[31:34].str.strip(")").astype(float).values
    return data


def load_human_data(fname):
    data = pd.read_csv(
        f"{'_'.join(fname.split('_')[:2])[:-1]}_human_results.csv"
    ).set_index("subject_id")
    counts = collections.defaultdict(list)
    for sentence in data.columns:
        samples = data[sentence].values
        for theta in np.linspace(0, 100, 11):
            counts["text"].append(f";; {sentence.capitalize()}.")
            counts["theta"].append(theta)
            counts["count"].append(np.sum(samples == theta))
    return pd.DataFrame(counts)


def filter_human_data(human_data, model_data):
    return human_data.loc[human_data["text"].isin(model_data["text"].unique()), :]


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
        if temperature <= 0:
            return np.inf
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
    human_data["temperature"] = np.nan
    return pd.concat(
        (
            t.loc[:, ["source", "text", "theta", "temperature", "prob"]]
            for t in (model_data, human_data)
        )
    )


def main(fname):
    model_data = load_model_data(fname)
    human_data = load_human_data(fname)
    human_data = filter_human_data(human_data, model_data)
    human_data = calc_human_probs(human_data)
    model_data = norm_model_probs(model_data, human_data)
    merge_data(model_data, human_data).to_csv(f"../outputs/{fname}", index=False)
    compare_distributions(model_data, human_data).to_csv(
        f"../outputs/{fname.replace('data','stats')}", index=False
    )


if __name__ == "__main__":
    main(sys.argv[1])

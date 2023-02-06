import pickle
from datasets import load_metric

# Metric
wer_metric = load_metric("wer")

def check_wer_score(pkl_path: str):
    results = None
    with open(pkl_path, mode="rb") as f:
        results = pickle.load(f)
    print(len(results))

### MAIN ###
if "__main__" == __name__:
    print("byT5 결과 분석")

    check_wer_score(pkl_path="../sents_unit_result.pkl")

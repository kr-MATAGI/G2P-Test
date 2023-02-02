import datasets
import pandas as pd
from datasets import Dataset
import evaluate

from g2pk.g2pk import G2p
from open_lib.kog2p_advanced.KoG2Padvanced import KoG2Padvanced

from utils.data_parser import SIG_parser


# Metrics
wer_metric = evaluate.load("wer")
per_metric = evaluate.load("cer")


#====================================
def run_test_g2pk(target_dataset: Dataset):
#====================================
    print(f"[run_test_g2pk] dataset.size: {len(target_dataset)}")
    print(f"[run_test_g2pk] {target_dataset[:5]}")

    g2pk = G2p()

    correct_list = []
    in_correct_list = []
    answer_list = []
    pred_list = []
    for idx, item in enumerate(target_dataset):
        word = item["word"]
        ipa = item["ipa"]
        pron = item["pron"]

        res_g2pk = g2pk(word)
        print(f"[run_test_g2pk] {idx}, {res_g2pk}, {ipa}, {pron}")

        answer_list.append(pron)
        pred_list.append(res_g2pk)

        if res_g2pk == pron:
            correct_list.append(item)
        else:
            in_correct_list.append(item)
    print(f"[run_test_g2pk] total_cnt : {len(correct_list) + len(in_correct_list)}")
    print(f"[run_test_g2pk] result: correct_cnt: {len(correct_list)}, in_correct_cnt: {len(in_correct_list)}")

    wer_score = wer_metric.compute(predictions=pred_list, references=answer_list)
    per_score = per_metric.compute(predictions=pred_list, references=answer_list)
    print(f"[run_test_kr_g2pk] wer: {wer_score}, per: {per_score}")

    return {"wer": wer_score, "per": per_score}

#===================================
def run_test_ko_g2p_advanced(target_dataset: Dataset):
#===================================
    print(f"[run_test_ko_g2p_advanced] dataset.size: {len(target_dataset)}")
    print(f"[run_test_ko_g2p_advanced] {target_dataset[:5]}")

    g2pk = G2p()

    correct_list = []
    in_correct_list = []
    answer_list = []
    pred_list = []
    for idx, item in enumerate(target_dataset):
        word = item["word"]
        ipa = item["ipa"]
        pron = item["pron"]

        res_kog2p_advanced = KoG2Padvanced(word)
        print(f"[run_test_ko_g2p_advanced] {idx}, {res_kog2p_advanced}, {ipa}, {pron}")

        answer_list.append(pron)
        pred_list.append(res_kog2p_advanced)

        if res_kog2p_advanced == pron:
            correct_list.append(item)
        else:
            in_correct_list.append(item)
    print(f"[run_test_ko_g2p_advanced] total_cnt : {len(correct_list) + len(in_correct_list)}")
    print(f"[run_test_ko_g2p_advanced] result: correct_cnt: {len(correct_list)}, in_correct_cnt: {len(in_correct_list)}")

    wer_score = wer_metric.compute(predictions=pred_list, references=answer_list)
    per_score = per_metric.compute(predictions=pred_list, references=answer_list)
    print(f"[run_test_ko_g2p_advanced] wer: {wer_score}, per: {per_score}")

    return {"wer": wer_score, "per": per_score}

### MAIN ###
if "__main__" == __name__:
    print("[run_kr_g2p_test][__main__]")

    sig_parser = SIG_parser(src_dir="./data/kr/pronunciation")
    train_dataset = sig_parser.sig_proun_data_load(target_lang="kor", mode="train")
    dev_dataset = sig_parser.sig_proun_data_load(target_lang="kor", mode="dev")
    test_dataset = sig_parser.sig_proun_data_load(target_lang="kor", mode="test")

    print(f"[run_kr_g2p_test][__main__] dataset.size - train: {len(train_dataset)}, "
          f"dev: {len(dev_dataset)}, test: {len(test_dataset)}")

    results = {}
    running_method = ["g2pk", "KoG2Padvanced"]
    # Run g2pk
    if "g2pk" in running_method:
        g2pk_score = run_test_g2pk(target_dataset=test_dataset)
        results.update({"g2pk": g2pk_score})

    # Run KoG2Padvanced
    if "KoG2Padvanced" in running_method:
        kog2p_adv_score = run_test_ko_g2p_advanced(target_dataset=test_dataset)
        results.update({"koG2Padv": kog2p_adv_score})

    print("---------------------------------")
    print("[run_kr_g2p_test][__main__] Total Results: ")
    print(f"[run_kr_g2p_test][__main__] results: {results}")
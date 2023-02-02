import datasets
import pandas as pd
from datasets import Dataset
import evaluate

from g2pk.g2pk import G2p
from open_lib.smart_g2p.trans import sentranslit as trans
from open_lib.kog2p_advanced.KoG2Padvanced import KoG2Padvanced
from open_lib.KoG2P.g2p import runKoG2P

from hangul_utils import join_jamos
from utils.data_parser import SIG_parser
from jamo import h2j, j2hcj

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
    wer_ans_list = []
    wer_pred_list = []

    per_ans_list = []
    per_pred_list = []

    for idx, item in enumerate(target_dataset):
        word = item["word"]
        ipa = item["ipa"]
        pron = item["pron"]

        res_g2pk = g2pk(word)
        print(f"[run_test_g2pk] {idx}, {res_g2pk}, {ipa}, {pron}")

        wer_ans_list.append(pron)
        wer_pred_list.append(res_g2pk)

        jamo_ans = j2hcj(h2j(pron))
        jamo_pred = j2hcj(h2j(res_g2pk))
        per_ans_list.append(jamo_ans)
        per_pred_list.append(jamo_pred)

        if res_g2pk == pron:
            correct_list.append(item)
        else:
            in_correct_list.append(item)
    print(f"[run_test_g2pk] total_cnt : {len(correct_list) + len(in_correct_list)}")
    print(f"[run_test_g2pk] result: correct_cnt: {len(correct_list)}, in_correct_cnt: {len(in_correct_list)}")

    wer_score = wer_metric.compute(predictions=wer_pred_list, references=wer_ans_list)
    per_score = per_metric.compute(predictions=per_pred_list, references=per_ans_list)
    print(f"[run_test_kr_g2pk] wer: {wer_score}, per: {per_score}")

    return {"wer": wer_score, "per": per_score}

#===================================
def run_test_ko_g2p_advanced(target_dataset: Dataset):
#===================================
    print(f"[run_test_ko_g2p_advanced] dataset.size: {len(target_dataset)}")
    print(f"[run_test_ko_g2p_advanced] {target_dataset[:5]}")

    correct_list = []
    in_correct_list = []
    wer_ans_list = []
    wer_pred_list = []
    per_ans_list = []
    per_pred_list = []
    for idx, item in enumerate(target_dataset):
        word = item["word"]
        ipa = item["ipa"]
        pron = item["pron"]

        res_kog2p_advanced = KoG2Padvanced(word)
        print(f"[run_test_ko_g2p_advanced] {idx}, {res_kog2p_advanced}, {ipa}, {pron}")

        wer_ans_list.append(pron)
        wer_pred_list.append(res_kog2p_advanced)

        jamo_ans = j2hcj(h2j(pron))
        jamo_pred = j2hcj(h2j(res_kog2p_advanced))
        per_ans_list.append(jamo_ans)
        per_pred_list.append(jamo_pred)

        if res_kog2p_advanced == pron:
            correct_list.append(item)
        else:
            in_correct_list.append(item)
    print(f"[run_test_ko_g2p_advanced] total_cnt : {len(correct_list) + len(in_correct_list)}")
    print(f"[run_test_ko_g2p_advanced] result: correct_cnt: {len(correct_list)}, in_correct_cnt: {len(in_correct_list)}")

    wer_score = wer_metric.compute(predictions=wer_pred_list, references=wer_ans_list)
    per_score = per_metric.compute(predictions=per_ans_list, references=per_pred_list)
    print(f"[run_test_ko_g2p_advanced] wer: {wer_score}, per: {per_score}")

    return {"wer": wer_score, "per": per_score}


#===================================
def run_test_smart_g2p(target_dataset: Dataset):
#===================================
    print(f"[run_test_smart_g2p] dataset.size: {len(target_dataset)}")
    print(f"[run_test_smart_g2p] {target_dataset[:5]}")

    correct_list = []
    in_correct_list = []
    wer_ans_list = []
    wer_pred_list = []
    per_ans_list = []
    per_pred_list = []
    for idx, item in enumerate(target_dataset):
        word = item["word"]
        ipa = item["ipa"]
        pron = item["pron"]

        res_smart_g2p = trans(word)
        print(f"[run_test_smart_g2p] {idx}, {res_smart_g2p}, {ipa}, {pron}")

        wer_ans_list.append(pron)
        wer_pred_list.append(res_smart_g2p)

        jamo_ans = j2hcj(h2j(pron))
        jamo_pred = j2hcj(h2j(res_smart_g2p))
        per_ans_list.append(jamo_ans)
        per_pred_list.append(jamo_pred)

        if res_smart_g2p == pron:
            correct_list.append(item)
        else:
            in_correct_list.append(item)
    print(f"[run_test_smart_g2p] total_cnt : {len(correct_list) + len(in_correct_list)}")
    print(f"[run_test_smart_g2p] result: correct_cnt: {len(correct_list)}, in_correct_cnt: {len(in_correct_list)}")

    wer_score = wer_metric.compute(predictions=wer_pred_list, references=wer_ans_list)
    per_score = per_metric.compute(predictions=per_ans_list, references=per_pred_list)
    print(f"[run_test_smart_g2p] wer: {wer_score}, per: {per_score}")

    return {"wer": wer_score, "per": per_score}

#===================================
def load_g2p_jamo_dict():
#===================================
    g2p_jamo_dict = {}
    with open("./data/kr/g2p_dictionary.txt", mode="r", encoding="utf-8") as f:
        lines = f.readlines()
    for line in lines:
        han_sym, g2p_sym = line.replace("\n", "").split("|")
        han_sym = han_sym.strip()
        g2p_sym = g2p_sym.strip()
        g2p_jamo_dict[g2p_sym] = han_sym

    return g2p_jamo_dict

#===================================
def run_test_g2p(target_dataset: Dataset, rule_book_path: str):
#===================================
    print(f"[run_test_g2p] dataset.size: {len(target_dataset)}")
    print(f"[run_test_g2p] {target_dataset[:5]}")

    sym_jamo_dict = load_g2p_jamo_dict()

    correct_list = []
    in_correct_list = []
    wer_ans_list = []
    wer_pred_list = []
    per_ans_list = []
    per_pred_list = []
    for idx, item in enumerate(target_dataset):
        word = item["word"]
        ipa = item["ipa"]
        pron = item["pron"]

        res_smart_g2p = runKoG2P(word, rule_book_path)
        res_smart_g2p = res_smart_g2p.split(" ")
        res_smart_g2p = "".join([sym_jamo_dict[x] for x in res_smart_g2p])
        res_smart_g2p = join_jamos(res_smart_g2p)
        print(f"[run_test_g2p] {idx}, {res_smart_g2p}, {ipa}, {pron}")

        wer_ans_list.append(pron)
        wer_pred_list.append(res_smart_g2p)

        jamo_ans = j2hcj(h2j(pron))
        jamo_pred = j2hcj(h2j(res_smart_g2p))
        per_ans_list.append(jamo_ans)
        per_pred_list.append(jamo_pred)

        if res_smart_g2p == pron:
            correct_list.append(item)
        else:
            in_correct_list.append(item)
    print(f"[run_test_g2p] total_cnt : {len(correct_list) + len(in_correct_list)}")
    print(f"[run_test_g2p] result: correct_cnt: {len(correct_list)}, in_correct_cnt: {len(in_correct_list)}")

    wer_score = wer_metric.compute(predictions=wer_pred_list, references=wer_ans_list)
    per_score = per_metric.compute(predictions=per_ans_list, references=per_pred_list)
    print(f"[run_test_g2p] wer: {wer_score}, per: {per_score}")

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
    running_method = ["g2pk"]
    # Run g2pk
    if "g2pk" in running_method:
        g2pk_score = run_test_g2pk(target_dataset=test_dataset)
        results.update({"g2pk": g2pk_score})

    # Run KoG2Padvanced
    if "KoG2Padvanced" in running_method:
        kog2p_adv_score = run_test_ko_g2p_advanced(target_dataset=test_dataset)
        results.update({"koG2Padv": kog2p_adv_score})

    # Run SMART-G2P
    if "SMART-G2P" in running_method:
        smart_g2p_score = run_test_smart_g2p(target_dataset=test_dataset)
        results.update({"smart_g2p": smart_g2p_score})

    # Run G2P
    if "G2P" in running_method:
        g2p_score = run_test_g2p(target_dataset=test_dataset,
                                 rule_book_path="/home/ailab/바탕화면/KT_IPA/G2P-Test/prepare_proj/open_lib/KoG2P/rulebook.txt")
        results.update({"g2p": g2p_score})

    print("---------------------------------")
    print("[run_kr_g2p_test][__main__] Total Results: ")
    print(f"[run_kr_g2p_test][__main__] results:")
    for k, v in results.items():
        print(k, ":", v)
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
def run_test_g2pk(target_dataset: Dataset, debug_mode: bool = False):
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
            in_correct_list.append((str(idx), word, ipa, pron, res_g2pk))

    print(f"[run_test_g2pk] total_cnt : {len(correct_list) + len(in_correct_list)}")
    print(f"[run_test_g2pk] result: correct_cnt: {len(correct_list)}, in_correct_cnt: {len(in_correct_list)}")

    wer_score = wer_metric.compute(predictions=wer_pred_list, references=wer_ans_list)
    per_score = per_metric.compute(predictions=per_pred_list, references=per_ans_list)
    print(f"[run_test_kr_g2pk] wer: {wer_score}, per: {per_score}")

    # Debug mode
    if debug_mode:
        with open("./g2pk_debug.txt", mode="w", encoding="utf-8") as f:
            f.write("Index\tword\tipa\tpron\tpred\n")
            for item in in_correct_list:
                f.write(item[0]+"\t"+item[1]+"\t"+item[2]+"\t"+item[3]+"\t"+item[4]+"\n")
        print(f"[run_Test_kr_g2pk] Debug mode complete!")

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

        res_smart_g2p = g2pk(trans(word))
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
    per_score = per_metric.compute(predictions=per_pred_list, references=per_ans_list)
    print(f"[run_test_g2p] wer: {wer_score}, per: {per_score}")

    return {"wer": wer_score, "per": per_score}

#===================================
def run_pnu_pron(target_dataset: Dataset, debug_mode: bool = False):
#===================================
    print(f"[run_pnu_pron] dataset.size: {len(test_dataset)}")

    # open preds
    all_words = []
    with open("data/kr/save_pnu_preds_1.txt", mode="r", encoding="utf-8") as f:
        read_words = f.readlines()
        read_words = [x.replace("\n", "").split("\t")[-1] for x in read_words]
        print(f"[run_pnu_pron] preds_1.size {len(read_words)}")
        all_words.extend(read_words)
    with open("data/kr/save_pnu_preds_2.txt", mode="r", encoding="utf-8") as f:
        read_words = f.readlines()
        read_words = [x.replace("\n", "").split("\t")[-1] for x in read_words]
        print(f"[run_pnu_pron] preds_2.size: {len(read_words)}")
        all_words.extend(read_words)
    print(f"[run_pnu_pron] all_words.size: {len(all_words)}")

    # remove space
    all_words = [x.replace(" ", "") for x in all_words]

    # make ans
    wer_ans_list = []
    per_ans_list = []

    in_correct_word = []
    for idx, (ans, pred) in enumerate(zip(target_dataset, all_words)):
        word = ans["word"]
        ipa = ans["ipa"]
        pron = ans["pron"]

        wer_ans_list.append(pron)

        jamo_ans = j2hcj(h2j(pron))
        per_ans_list.append(jamo_ans)

        if pron != pred:
            in_correct_word.append((str(idx), word, ipa, pron, pred))

    per_pred_list = []
    for pred in all_words:
        jamo_pred = j2hcj(h2j(pred))
        per_pred_list.append(jamo_pred)

    wer_score = wer_metric.compute(predictions=all_words, references=wer_ans_list)
    per_score = per_metric.compute(predictions=per_pred_list, references=per_ans_list)
    print(f"[run_test_g2p] wer: {wer_score}, per: {per_score}")

    # Debug mode
    if debug_mode:
        with open("./pnu_debug.txt", mode="w", encoding="utf-8") as f:
            f.write("Index\tword\tipa\tpron\tpred\n")
            for item in in_correct_word:
                f.write(item[0]+"\t"+item[1]+"\t"+item[2]+"\t"+item[3]+"\t"+item[4]+"\n")
        print(f"[run_test_g2p] Complete debug mode !")

    return {"wer": wer_score, "per": per_score}

#===================================
def compare_sentence_results(sentence: str, rule_book_path: str):
#===================================
    print(f"[compare_sentence_results] sentence: {sentence}")

    results = {}

    g2pk = G2p()
    res_g2pk = g2pk(sentence)
    res_kog2p_adv = KoG2Padvanced(sentence)
    res_smart_g2p = g2pk(trans(sentence))
    res_kog2p = runKoG2P(sentence, rule_book_path)
    sym_jamo_dict = load_g2p_jamo_dict()
    res_kog2p = "".join([sym_jamo_dict[x] for x in res_kog2p.split(" ")])
    res_kog2p = join_jamos(res_kog2p)

    # update results
    results.update({"g2pk": res_g2pk})
    results.update({"KoG2P_adv": res_kog2p_adv})
    results.update({"smart_g2p": res_smart_g2p})
    results.update({"koG2P": res_kog2p})

    # Print
    for k, v in results.items():
        print(f"[compare_sentence_results] {k} : {v}")

### MAIN ###
if "__main__" == __name__:
    print("[run_kr_g2p_test][__main__]")

    rule_book_path = "/home/ailab/바탕화면/KT_IPA/G2P-Test/prepare_proj/open_lib/KoG2P/rulebook.txt"

    sig_parser = SIG_parser(src_dir="./data/kr/pronunciation")
    train_dataset = sig_parser.sig_proun_data_load(target_lang="kor", mode="train")
    dev_dataset = sig_parser.sig_proun_data_load(target_lang="kor", mode="dev")
    test_dataset = sig_parser.sig_proun_data_load(target_lang="kor", mode="test")

    print(f"[run_kr_g2p_test][__main__] dataset.size - train: {len(train_dataset)}, "
          f"dev: {len(dev_dataset)}, test: {len(test_dataset)}")

    results = {}
    running_method = ["PNU"]

    compare_sentence_results("신을 신고 동사무소에서 혼인 신고를 하자", rule_book_path=rule_book_path)

    # Run g2pk
    if "g2pk" in running_method:
        g2pk_score = run_test_g2pk(target_dataset=test_dataset, debug_mode=True)
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
                                 rule_book_path=rule_book_path)
        results.update({"g2p": g2p_score})

    if "PNU" in running_method:
        pnu_score = run_pnu_pron(test_dataset, debug_mode=True)

    print("---------------------------------")
    print("[run_kr_g2p_test][__main__] Total Results: ")
    print(f"[run_kr_g2p_test][__main__] results:")
    for k, v in results.items():
        print(k, ":", v)
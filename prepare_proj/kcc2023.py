import pickle
import evaluate
import time
from prepare_proj.definition.data_def import *

from g2pk.g2pk import G2p
from open_lib.KoG2P.g2p import runKoG2P
from hangul_utils import join_jamos

# Metrics
wer_metric = evaluate.load("wer")
per_metric = evaluate.load("cer")


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

#========================================================
def run_test_g2pk(src_data_list: List[str], tgt_data_list: List[str]):
#========================================================
    pred_data_list = []
    correct_cnt = 0

    g2pk = G2p()

    start_time = time.time()
    for src_item, tgt_item in zip(src_data_list, tgt_data_list):
        res_g2pk = g2pk(src_item)
        # print(res_g2pk, "\n", tgt_item)
        # input()

        if res_g2pk == tgt_item:
            correct_cnt += 1

        pred_data_list.append(res_g2pk)
    end_time = time.time()

    ## PRINT
    wer_score = wer_metric.compute(predictions=pred_data_list, references=tgt_data_list)
    per_score = per_metric.compute(predictions=pred_data_list, references=tgt_data_list)

    print(f"WER : {wer_score * 100}")
    print(f"PER : {per_score * 100}")
    print(f"S-Acc. : {correct_cnt / len(tgt_data_list) * 100}")
    print(f"time: {end_time - start_time}")

    print("g2pk test END !")

#========================================================
def run_test_KoG2P(src_data_list: List[str], tgt_data_list: List[str]):
#========================================================
    pred_data_list = []
    correct_cnt = 0

    rule_book_path = "/home/ailab/바탕화면/Git/KT-IPA_G2P-Testing/prepare_proj/open_lib/KoG2P/rulebook.txt"
    sym_jamo_dict = load_g2p_jamo_dict()

    start_time = time.time()
    for src_item, tgt_item in zip(src_data_list, tgt_data_list):
        res_kog2p = runKoG2P(src_item, rule_book_path)
        res_kog2p = res_kog2p.split(" ")
        res_kog2p = "".join([sym_jamo_dict[x] for x in res_kog2p])
        res_kog2p = join_jamos(res_kog2p)
        print(res_kog2p)
        print(tgt_item)
        input()

        if res_kog2p == tgt_item:
            correct_cnt += 1
        pred_data_list.append(res_kog2p)
    end_time = time.time()

    ## PRINT
    wer_score = wer_metric.compute(predictions=pred_data_list, references=tgt_data_list)
    per_score = per_metric.compute(predictions=pred_data_list, references=tgt_data_list)

    print(f"WER : {wer_score * 100}")
    print(f"PER : {per_score * 100}")
    print(f"S-Acc. : {correct_cnt / len(tgt_data_list) * 100}")
    print(f"time: {end_time - start_time}")

    print("KoG2P test END !")


### MAIN ###
if "__main__" == __name__:

    # load test data
    src_data = []
    with open("./data/kcc/test_kor_src_data.pkl", mode="rb") as f:
        src_data = pickle.load(f)
        src_data = [x.sent for x in src_data]
    print(f"src_data.size: {len(src_data)}")

    tgt_data = []
    with open("./data/kcc/test_kor_tgt_data.pkl", mode="rb") as f:
        tgt_data = pickle.load(f)
        tgt_data = [x.sent for x in tgt_data]
    print(f"tgt_data.size: {len(tgt_data)}")

    # g2pk
    run_test_g2pk(src_data, tgt_data)

    # KoG2P
    # run_test_KoG2P(src_data, tgt_data)
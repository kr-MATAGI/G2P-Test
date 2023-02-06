import os
import pickle
import evaluate

# Metric
wer_metric = evaluate.load("wer")

def check_wer_score(pkl_path: str):
    results = None
    with open(pkl_path, mode="rb") as f:
        results = pickle.load(f)

    ans = []
    preds = []
    for item in results:
        if len(item[-3]) == len(item[-2]):
            ans.extend(item[-3])
            preds.extend(item[-2])

    wer_score = wer_metric.compute(predictions=preds, references=ans)
    print(wer_score, len(ans))

def compare_preds_sent_and_word(sent_pkl_path: str, word_pkl_path: str):
    sent_results, word_results = None, None
    with open(sent_pkl_path, mode="rb") as f:
        sent_results = pickle.load(f)
    with open(word_pkl_path, mode="rb") as f:
        word_results = pickle.load(f)
    print(len(sent_results), len(word_results))

    '''
        save file format
        word / ipa / word_ipa / sent_ipa / is_wrong
    '''
    for re_idx, (sent_item, word_item) in enumerate(zip(sent_results, word_results)):
        if not word_item[-1]:
            with open("./err_case/"+str(sent_item[0])+"_err.txt", mode="w", encoding="utf-8") as f:
                f.write("word\tipa\tword_pred\tsent_pred\tis_word_wrong\tis_sent_wrong\n")
                word = sent_item[1]
                ipa = sent_item[2]
                word_pred = word_item[3]
                sent_pred = sent_item[3]
                for p_i, (w, i, w_p, s_p) in enumerate(zip(word, ipa, word_pred, sent_pred)):
                    f.write(str(p_i)+"\t"+w+"\t"+i+"\t"+w_p+"\t"+s_p+"\t"+str(w_p==i)+"\t"+str(s_p==i)+"\n")

def print_err_word_wrong_case(err_dir_path: str):
    file_list = os.listdir(err_dir_path)
    print(file_list)

### MAIN ###
if "__main__" == __name__:
    print("byT5 결과 분석")

    # check_wer_score(pkl_path="../sents_unit_result.pkl")
    # check_wer_score(pkl_path="../word_unit_result.pkl")

    # compare_preds_sent_and_word(sent_pkl_path="../sent_unit_result.pkl",
    #                             word_pkl_path="../word_unit_result.pkl")
    print_err_word_wrong_case(err_dir_path="./err_case")
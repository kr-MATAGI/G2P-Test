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

    all_err = []
    for file_name in file_list:
        file_idx = file_name.split("_")[0]
        full_path = err_dir_path+"/"+file_name
        with open(full_path, mode="r", encoding="utf-8") as f:
            lines = f.readlines()[1:]
            lines = [x.replace("\n", "") for x in lines]
            sent = []

            for line in lines:
                sp_line = line.split("\t")
                sent.append(sp_line[1])

            for line in lines:
                sp_line = line.split("\t")
                if sp_line[3] != sp_line[4]:
                    all_err.append((file_idx, line, " ".join(sent)))
    # Write
    with open("diff_pred_case.txt", mode="w", encoding="utf-8") as f:
        f.write("file_index\n")
        f.write("idx, word, ans, word_pred, sent_pred, is_word_wrong, is_sent_wrong\n\n")

        for err in all_err:
            file_idx, content = err[0], "\t".join(err[1].split("\t"))
            f.write(str(file_idx)+"\n")
            f.write(err[-1]+"\n")
            f.write(content+"\n\n")

def eojoel_diff_ipa_checking(src_path: str):
    all_eojeols = []
    with open(src_path, mode="rb") as f:
        all_eojeols = pickle.load(f)
    print(len(all_eojeols[0]), all_eojeols[0])

    eojeol_dict = {}
    for idx, item in enumerate(all_eojeols):
        eojeol_list = item[1]
        for e_idx, eojeol in enumerate(eojeol_list):
            if eojeol not in eojeol_dict.keys():
                eojeol_dict[eojeol] = [item[3][e_idx]]
            else:
                if item[3][e_idx] not in eojeol_dict[eojeol]:
                    eojeol_dict[eojeol].append(item[3][e_idx])

    eojeol_count = len(eojeol_dict.keys())
    ipa_count = 0
    for k, v in eojeol_dict.items():
        ipa_count += len(v)
        if 2 <= len(v):
            print(k, ":", v)
    print("eojeol_cnt: ", eojeol_count, "ipa_cnt: ", ipa_count, "ipa/eojeol: ", ipa_count/eojeol_count)

def nikl_corpus_compare_word_and_ipa(src_path: str):
    all_nikl_data = []
    with open(src_path, mode="r", encoding="utf-8") as f:
        all_nikl_data = f.readlines()
        all_nikl_data = [x.replace("\n", "") for x in all_nikl_data]

    print(len(all_nikl_data))
    eojeol_dict = {}
    count = 0
    for nikl_data in all_nikl_data:
        sent, ipa_sent, kor_pron = nikl_data.split("\t")
        ipa_sent = ipa_sent.replace(" esʌ ", " ")
        sp_sent = sent.split(" ")
        sp_ipa = ipa_sent.split(" ")
        if len(sp_sent) != len(sp_ipa):
            # print(sp_sent)
            # print(sp_ipa)
            # input()
            count += 1
            continue

        for word, ipa in zip(sp_sent, sp_ipa):
            if word not in eojeol_dict.keys():
                eojeol_dict[word] = [ipa]
            else:
                if ipa not in eojeol_dict[word]:
                    eojeol_dict[word].append(ipa)

    eojeol_cnt = len(eojeol_dict.keys())
    ipa_cnt = 0
    for k, v in eojeol_dict.items():
        ipa_cnt += len(v)
        if 2 <= len(v):
            print(k, ":", v)
    print("eojeol_cnt: ", eojeol_cnt, "ipa_cnt: ", ipa_cnt, "ipa_cnt/eojeol_cnt:", ipa_cnt/eojeol_cnt)
    print(count)



### MAIN ###
if "__main__" == __name__:
    print("byT5 결과 분석")

    # check_wer_score(pkl_path="../sents_unit_result.pkl")
    # check_wer_score(pkl_path="../word_unit_result.pkl")

    # compare_preds_sent_and_word(sent_pkl_path="../sent_unit_result.pkl",
    #                             word_pkl_path="../word_unit_result.pkl")
    # print_err_word_wrong_case(err_dir_path="./err_case")

    # eojoel_diff_ipa_checking("../sent_unit_result.pkl")
    nikl_corpus_compare_word_and_ipa(src_path="../data/NIKL/for_byT5.txt")
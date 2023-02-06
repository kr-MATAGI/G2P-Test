import os.path
import pandas as pd
import json
import random

from datasets import Dataset
from typing import List

class SIG_parser:
    def __init__(self, src_dir: str):
        print(f"[SIGMORPHON_Parser][__init__] SIGMORPHON data Parser")

        self.data_list = []
        if not os.path.exists(src_dir):
            print(f"[SIGMORPHON_Parser][__init__] ERR - Not Existed: {src_dir}")
        else:
            self.src_dir = src_dir
            self.data_list = [x for x in os.listdir(src_dir) if ".tsv" in x]
            print(f"[SIGMORPHON_Parser][__init__] files:{self.data_list}")

    def tsv_to_txt(self, path: str):
        dataset = pd.read_csv(path, delimiter='\t', header=None)
        file_name = os.path.splitext(os.path.basename(path))[0]
        dir = os.path.dirname(path)
        dataset.to_csv(dir+"/parser_"+file_name+".txt", index=False, header=None, sep='\t')

    def sig_data_load(self, target_lang: str, mode: str):
        print(f"[SIGMORPHON_Parser][sig_data_load] target_lang: {target_lang}, mode: {mode}")

        target_file_name = target_lang + "_" + mode + ".tsv"
        if target_file_name not in self.data_list:
            raise Exception("Plz Check target_file_name: ", target_file_name)

        words = []
        ipa_list = []

        full_path = self.src_dir + "/" + target_file_name
        with open(full_path, mode="r", encoding="utf-8") as f:
            for line in f.readlines():
                word, pron = line.strip().split('\t')
                words.append(word)
                ipa_list.append(pron.replace(" ", ""))

        data = pd.DataFrame()
        data['word'] = words
        data['pron'] = ipa_list

        return Dataset.from_pandas(data)

    def sig_proun_data_load(self, target_lang: str, mode: str):
        print(f"[SIGMORPHON_Parser][sig_data_load] target_lang: {target_lang}, mode: {mode}")

        target_file_name = "pronunciation_" + target_lang + "_" + mode + ".tsv"
        if target_file_name not in self.data_list:
            raise Exception("Plz Check target_file_name: ", target_file_name)

        words = []
        ipa_list = []
        prons = []

        full_path = self.src_dir + "/" + target_file_name
        with open(full_path, mode="r", encoding="utf-8") as f:
            for line in f.readlines():
                word, ipa, pron = line.strip().split('\t')
                words.append(word)
                ipa_list.append(ipa.replace(" ", ""))
                prons.append(pron)

        data = pd.DataFrame()
        data['word'] = words
        data['ipa'] = ipa_list
        data['pron'] = prons

        return Dataset.from_pandas(data)


#### NIKL Parser
#============================================================
class NiklParser:
#============================================================
    def __init__(self, src_dir: str):
        print(f"[NiklParser][__init__] src_dir: {src_dir}")
        self.src_dir = src_dir
        if 0 < len(src_dir):
            self.src_file_list = os.listdir(src_dir)
            print(f"[NiklParser][__init__] src_dir - size: {len(self.src_file_list)}, list: {self.src_file_list}")

    def parse_text(self, data_split_size: int=20000):
        all_text = []
        for f_idx, file_name in enumerate(self.src_file_list):
            full_path = self.src_dir + "/" + file_name
            print(f"[NiklParser][parse_text] full_path: {full_path}")

            json_data = None
            with open(full_path, mode="r", encoding="utf-8") as json_f:
                json_data = json.load(json_f)
            print(f"[NIKLParser][parse_text] {file_name}.size: {len(json_data)}")

            file_text = []
            doc_obj = json_data["document"]
            for doc_item in doc_obj:
                sent_arr = doc_item["sentence"]
                for sent_obj in sent_arr:
                    form = sent_obj["form"]
                    if 15 >= len(form) :
                        continue
                    file_text.append(form)
            print(f"[NIKLParser][parse_text] all_text.size: {len(file_text)}")
            all_text.extend(file_text)
        print(f"[NIKLParser][parse_text] all_text.size: {len(all_text)}")

        if 0 < data_split_size:
            random.shuffle(all_text)
            all_text = all_text[:data_split_size]

        return all_text

    def save_text(self, src_data: List[str], save_path: str):
        print(f"[NIKLParser][save_text] save_path: {save_path}")

        with open(save_path, mode="w", encoding="utf-8") as f:
            for src_item in src_data:
                f.write(src_item + "\n")
            print(f"[NIKLParser][save_txt] Complete - Save.size: {len(src_data)}")

    def extract_data_from_converted_results(self, src_dir_path: str, save_path: str, target_size: int):
        '''
            모두의 말뭉치 -> 부산대 발음변환기에서 변환된 파일만을 가지고 일정 데이터 추출
        '''
        print(f"[extract_data_from_converted_results] src_dir_path: {src_dir_path}")

        # Load Results
        result_file_list = os.listdir(src_dir_path)
        print(f"[extract_data_from_converted_results] result_file_list size: {len(result_file_list)}\n{result_file_list}")

        all_result_data = []
        for file_name in result_file_list:
            with open(src_dir_path+"/"+file_name, mode="r", encoding="utf-8") as f:
                inner_file_data = f.readlines()
                all_result_data.extend(inner_file_data)
        print(f"[extract_data_from_converted_results] all_result_data size: {len(all_result_data)}\n{all_result_data[:5]}")
        all_result_data = random.choices(population=all_result_data, k=10000)
        print(f"[extract_data_from_converted_results] rand.choices.size: {target_size}\n{all_result_data[:5]}")

        # Save
        with open(save_path, mode="w", encoding="utf-8") as f:
            for shuffled_data in all_result_data:
                f.write(shuffled_data)
            print(f"[extract_data_from_converted_results] Complete Save ! : {save_path}")

    def load_nikl_data(self, target_path: str, lang: str="kor"):
        # Load
        all_dataset = None
        print(f"[NiklParser][load_nikl_data] target_path: {target_path}")
        with open(target_path, mode="r", encoding="utf-8") as f:
            all_dataset = f.readlines()
            all_dataset = [x.replace("\n", "") for x in all_dataset]
        print(f"[NiklParser][load_nikl_data] all_dataset.size: {len(all_dataset)}")

        all_word_ipa_pair = [] # [ (word, ipa) ]
        for nikl_data in all_dataset:
            sent, ipa, kor_pron = nikl_data.split("\t")
            # sent = sent.split(" ")
            # sent = ["<" + lang + ">: " + x for x in sent]
            # ipa = ipa.split(" ")
            # pron = kor_pron.split(" ")
            # for s, i, p in zip(sent, ipa, pron):
            #     all_word_ipa_pair.append((s, i, p))
            # sent, ipa, kor_pron = nikl_data.split("\t")
            all_word_ipa_pair.append((sent, ipa, kor_pron))

        print(f"[NiklParser][load_nikl_data] all_word_ipa_pair.size: {len(all_word_ipa_pair)}")

        split_size = 0.1
        dev_end_idx = int(len(all_word_ipa_pair) * (split_size * 8))
        train_pairs = all_word_ipa_pair[:dev_end_idx]
        dev_pairs = all_word_ipa_pair[dev_end_idx:int(dev_end_idx+len(all_word_ipa_pair)*split_size)]
        test_pairs = all_word_ipa_pair[int(dev_end_idx+len(all_word_ipa_pair)*split_size):]
        print(f"[NiklParser][load_nikl_data] train/dev/test.size: {len(train_pairs)}/{len(dev_pairs)}/{len(test_pairs)}")

        train_word, dev_word, test_word = [x[0] for x in train_pairs], [x[0] for x in dev_pairs], [x[0] for x in test_pairs]
        train_ipa, dev_ipa, test_ipa = [x[1] for x in train_pairs], [x[1] for x in dev_pairs], [x[1] for x in test_pairs]
        train_pron, dev_pron, test_pron = [x[2] for x in train_pairs], [x[2] for x in dev_pairs], [x[2] for x in test_pairs]
        print(f"[NiklParser][load_nikl_data] word - train/dev/test.size: {len(train_word)}/{len(dev_word)}/{len(test_word)}")
        print(f"[NiklParser][load_nikl_data] ipa - train/dev/test.size: {len(train_ipa)}/{len(dev_ipa)}/{len(test_ipa)}")
        print(f"[NiklParser][load_nikl_data] pron - train/dev/test.size: {len(train_pron)}/{len(dev_pron)}/{len(test_pron)}")

        train_df = pd.DataFrame()
        train_df["word"] = train_word
        train_df["ipa"] = train_ipa
        train_df["pron"] = train_pron

        dev_df = pd.DataFrame()
        dev_df["word"] = dev_word
        dev_df["ipa"] = dev_ipa
        dev_df["pron"] = dev_pron

        test_df = pd.DataFrame()
        test_df["word"] = test_word
        test_df["ipa"] = test_ipa
        test_df["pron"] = test_pron

        train_dataset = Dataset.from_pandas(train_df)
        dev_dataset = Dataset.from_pandas(dev_df)
        test_dataset = Dataset.from_pandas(test_df)
        return train_dataset, dev_dataset, test_dataset

### MAIN ###
if __name__ == '__main__':
    nikl_parser = NiklParser(src_dir="../data/corpus/NIKL/SXNE2102203310")
    # nikl_forms = nikl_parser.parse_text()
    # nikl_parser.save_text(src_data=nikl_forms, save_path="../data/corpus/NIKL/only_text/nikl_only_text.txt")
    # nikl_parser.extract_data_from_converted_results(src_dir_path="../data/corpus/NIKL/nikl_ipa_converted/results",
    #                                                 save_path="../data/corpus/NIKL/for_byT5.txt",
    #                                                 target_size=10000)

    train_dataset, dev_dataset, test_dataset = nikl_parser.load_nikl_data(target_path='../data/corpus/NIKL/for_byT5.txt')
    print(test_dataset[:10]["pron"])
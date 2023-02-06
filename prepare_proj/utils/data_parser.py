import os.path
import pandas as pd
import json
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
        if not os.path.exists(src_dir):
            raise Exception("Not Existed")
        self.src_dir = src_dir
        self.src_file_list = os.listdir(src_dir)
        print(f"[NiklParser][__init__] src_dir - size: {len(self.src_file_list)}, list: {self.src_file_list}")

    def parse_text(self):
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

        return all_text

    def save_text(self, src_data: List[str], save_path: str):
        print(f"[NIKLParser][save_text] save_path: {save_path}")

        with open(save_path, mode="w", encoding="utf-8") as f:
            for src_item in src_data:
                f.write(src_item + "\n")
            print(f"[NIKLParser][save_txt] Complete - Save.size: {len(src_data)}")

### MAIN ###
if __name__ == '__main__':
    nikl_parser = NiklParser(src_dir="../data/corpus/NIKL/SXNE2102203310")
    nikl_forms = nikl_parser.parse_text()
    nikl_parser.save_text(src_data=nikl_forms, save_path="../data/corpus/NIKL/only_text/nikl_only_text.txt")
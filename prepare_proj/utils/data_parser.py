import os.path
import pandas as pd
from datasets import Dataset

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
        prons = []

        full_path = self.src_dir + "/" + target_file_name
        with open(full_path, mode="r", encoding="utf-8") as f:
            for line in f.readlines():
                word, pron = line.strip().split('\t')
                words.append(word)
                prons.append(pron)

        data = pd.DataFrame()
        data['word'] = words
        data['pron'] = prons

        return Dataset.from_pandas(data)

### MAIN ###
if __name__ == '__main__':
    sig_parser = SIG_parser(src_dir='../data/en/sigmorphon')

    # tsv_to_txt 변환
    for path in sig_parser.data_list:
        txt_file = sig_parser.tsv_to_txt(path=sig_parser.src_dir+"/"+path)
    print("[SIGMORPHON_Parser][__init__] finish")



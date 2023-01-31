import pandas as pd
import csv
import os
class Processing:
    def __init__(self, path: str):
        print(f"[data_preprocessing][__init__]  data preprocessing")

        self.sig_data_list = []
        if not os.path.exists(path):
            print(f"[data_preprocessing][__init__] ERR - Not Existed: {path}")
        else:
            self.src_dir = path
            self.sig_data_list = [x for x in os.listdir(path) if "parser" in x]
            print(f"[data_preprocessing][__init__] files:{self.sig_data_list}")
            self.sig_dict = {}

    # Store SIGMORPHON train, dev, test to dict
    def store_sig(self, path: str):
        data = pd.read_csv(path, header=None, delimiter="\t")

        # save to dict
        for i in range(len(data)):
            if data[0][i] not in self.sig_dict:
                self.sig_dict[data[0][i]] = data[1][i]

    # Read Kor CMUDict and delete duplicate
    def ko_cmu(self, path: str):
        data = pd.read_csv(path, header=None, delimiter="\t")
        for i in range(len(data)):
            if data[0][i] in self.sig_dict:
                data.drop([i], axis=0, inplace=True)
            else:
                self.sig_dict[data[0][i]] = data[1][i]
        # save
        data.to_csv("../data/kr/sigmorphon/edit_ko_CMUDict.txt", header=None, index=False, sep="\t")

    # Read Eng CMUDict and delete duplicate
    def en_cmu(self, path: str):
        data = pd.read_csv(path, header=None, delimiter="\t", quoting=csv.QUOTE_NONE)
        data[0] = data[0].str.lower()

        for i in range(len(data)):
            if data[0][i] in self.sig_dict:
                data.drop([i], axis=0, inplace=True)

        # save
        data.to_csv("../data/en/CMUDict/edit_en_CMUDict.txt", header=None, index=False, sep="\t")


### Main ###
if __name__ == "__main__":
    """KR"""
    ko_processing = Processing(path="../data/kr/sigmorphon")

    # save sigmorphon data
    for file in ko_processing.sig_data_list:
        ko_processing.store_sig(path=ko_processing.src_dir+"/"+file)

    # Read CMUDict data and remove duplicate
    ko_processing.ko_cmu(path="../data/kr/sigmorphon/kor_hang_narrow_filtered.txt")

    """En"""
    en_processing = Processing(path="../data/en/sigmorphon")

    # save sigmorphon data
    for file in en_processing.sig_data_list:
        en_processing.store_sig(path=en_processing.src_dir+"/"+file)

    # Read CMUDict data and remove duplicate
    en_processing.en_cmu(path="../data/en/CMUDict/cmudict-0.7b-ipa.txt")
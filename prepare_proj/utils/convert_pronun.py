import os.path

import pandas as pd
import re
from hangul_utils import join_jamos, split_syllables

class ConvertPronun():
    def __init__(self, src_dir: str):
        print(f"[convert_pronun][__init__]")

        self.data_list = []
        if not os.path.exists(src_dir):
            print(f"Not exist {src_dir}")
        else:
            self.src_dir = src_dir
            self.data_list = [x for x in os.listdir(src_dir) if "ko" in x]
            print(f"file list {self.data_list}")

    # 파일 읽기
    def read_file(self, file: str):
        self.df = pd.read_csv(self.src_dir+"/"+file, header=None, delimiter="\t")
        mapping = pd.read_csv("../data/kr/dictionary.txt", header=None, delimiter="\t")
        self.dic = {}

        # mapping dicttionary to dict
        for i in range(len(mapping)):
            if mapping[0][i] not in self.dic:
                self.dic[mapping[0][i]] = mapping[1][i]

        # delete speicial char
        self.df['pronun'] = self.df[1]
        self.df['pronun'] = self.df['pronun'].str.replace(r"[ ːˈˌ]", r'', regex=True)

        # ipa -> 발음대로
        for ph, gr in self.dic.items():
            self.df['pronun'] = self.df['pronun'].str.replace(ph, gr)

    # ㅚ, ㅞ 구분
    def handle_exp(self, origin: list, pronun: list):
        # ipa가 w e̞일 경우 e로 변경
        exp = "e"

        for i in range(len(pronun)):
            origin_we_list = []
            if exp in pronun[i]:
                # 원래 단어 자모로 분해
                origin_jamo = split_syllables(origin[i])
                for j in range(len(origin_jamo)):
                    if 'ㅚ' in origin_jamo[j]:
                        origin_we_list.append('ㅚ')
                    elif 'ㅞ' in origin_jamo[j]:
                        origin_we_list.append('ㅞ')
                    else:
                        continue
                # e -> ㅚ or ㅞ
                for we in origin_we_list:
                    pronun[i] = pronun[i].replace(exp, we, 1)

        return pronun

    # 이응 추가, 자모 합치기기
    def concat_jamo(self, words: list):
        vowel = ["ㅏ", "ㅓ", "ㅗ", "ㅜ", "ㅡ", "ㅐ", "ㅒ", "ㅘ", "ㅚ", "ㅙ", "ㅢ", "ㅑ", "ㅕ", "ㅛ", "ㅠ", "ㅣ", "ㅔ", "ㅖ", "ㅝ", "ㅟ",
                 "ㅞ"]
        result_list = []

        # 모음만 있는 경우 처리 ex) ㅏㅣ->아이
        for word in words:
            word_list = list(word)  # 한 글자씩 분해
            index = 0
            for i in range(len(word_list)):
                # 첫 글자가 모음일 경우
                if i == 0 and word[i] in vowel:
                    word_list.insert(0, "ㅇ")
                    index += 1
                else:
                # 전 글자가 이응으로 시작하거나 모음만 있는 경우 이응 추가
                    if (word[i] in vowel and word[i-1] == "ㅇ") or (word[i] in vowel and word[i-1] in vowel):
                        word_list.insert(index, "ㅇ")
                        index += 1
                index += 1
            result = "".join(word_list)

            # 자모 합치기
            result_list.append(join_jamos(result))
        return result_list



### Main ###
if __name__ == "__main__":
    pronun = ConvertPronun(src_dir="../data/kr/sigmorphon")

    for file in pronun.data_list:
        pronun.read_file(file=file)
        # ㅚ, ㅞ 처리
        pronun.df['pronun'] = pronun.handle_exp(pronun.df[0], pronun.df['pronun'])
        # 자음만 있는 경우 이응 추가와 분리된 자모 합치기
        pronun.df['pronun'] = pronun.concat_jamo(pronun.df['pronun'])

        # save
        pronun.df.to_csv("../data/kr/pronunciation/pronunciation_"+file, header=None, index=False, sep="\t")

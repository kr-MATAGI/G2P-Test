import os

from typing import List

#================================================
class SigMorphonConveter:
#================================================
    chosung = {
        "ㄱ": "k", "ㄲ": "k⁼"
    }

    def __init__(self):
        print(f"[SigMorphonConveter][__init__]")

    def convert_ipa2hangul(self, src_path: str, save_path: str):
        print(f"[SigMorphonConveter][convert_ipa2hangul] src_path: {src_path}")
        if not os.path.exists(src_path):
            raise Exception("Plz Check src_path, not existed", src_path)

        word_pron_pairs = self._read_tsv(src_path)
        print(f"[SigMorphonConveter][convert_ipa2hangul] word_pron_pairs.len: {len(word_pron_pairs)}")

        for word, pron in word_pron_pairs:
            conv_pron = self._conv_ipx(pron)


    def _read_tsv(self, src_path: str):
        word_pron_pair_list = []
        with open(src_path, mode="r") as f:
            line = f.readlines()
            for l in line:
                word, pron = l.strip().split("\t")
                pron = pron.replace(" ", "")
                word_pron_pair_list.append((word, pron))

        return word_pron_pair_list

    def _conv_ipx(self, pron: str):
        ret_hangul = None



        return ret_hangul


#================================================
def modify_pnu_err_case(index_list: List[int], fixed_label: List[str]):
#================================================
    print(f"[modify_pnu_err_case] index_list: {len(index_list)}, fix_label: {len(fixed_label)}")
    assert len(index_list) == len(fixed_label), "ERR - plz check length"

### MAIN ###
if "__main__" == __name__:
    print("[data_utils][__main__]")

    sig_convert = SigMorphonConveter()
    sig_convert.convert_ipa2hangul(src_path="../data/kr/sigmorphon/kor_dev.tsv", save_path="")
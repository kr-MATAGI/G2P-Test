import torch
import torch.nn as nn
from run_def import EN_G2P_Model
from run_utils import load_en_g2p_model

#========================================================================
def main():
#========================================================================
    print("Select:\n")
    for k, v in EN_G2P_Model.items():
        print(f"->{v}. {k}")
    user_select = int(input())

    model, tokenizer = load_en_g2p_model(user_select)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

### MAIN ###
if "__main__" == __name__:
    main()
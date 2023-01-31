from run_def import EN_G2P_Model

from transformers import T5ForConditionalGeneration, AutoTokenizer  # byT5

#========================================================================
def load_en_g2p_model(user_select: int):
#========================================================================
    model, tokenizer = None, None
    if EN_G2P_Model["byT5"] == user_select:
        model = T5ForConditionalGeneration.from_pretrained('charsiu/g2p_multilingual_byT5_tiny_16_layers_100')
        tokenizer = AutoTokenizer.from_pretrained('google/byt5-small')

    return model, tokenizer
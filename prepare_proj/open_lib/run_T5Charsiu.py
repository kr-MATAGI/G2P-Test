from transformers import T5ForConditionalGeneration, AutoTokenizer

### Main ###
if __name__ == '__main__':
    model = T5ForConditionalGeneration.from_pretrained('charsiu/g2p_multilingual_byT5_tiny_16_layers_100')
    tokenizer = AutoTokenizer.from_pretrained('google/byt5-small')

    # tokenized English words
    words = ['abe', 'siu', 'is', 'a', 'Cantonese', 'style', 'of', 'barbecued', 'pork']
    words = ['<eng-us>: ' + i for i in words]

    out = tokenizer(words, padding=True, add_special_tokens=False, return_tensors='pt')

    preds = model.generate(**out, num_beams=1) # We do not find beam search helpful. Greedy decoding is enough
    phones = tokenizer.batch_decode(preds.tolist(), skip_special_tokens=True)

    print(phones)
from transformers import T5ForConditionalGeneration, AutoTokenizer
from utils.data_parser import SIG_parser, NiklParser

import argparse
import torch
import os
import json

import pickle

from dataclasses import dataclass
from attrdict import AttrDict

from datasets import load_metric
from typing import Union, Dict, List

from transformers import (
    Seq2SeqTrainer,
    Seq2SeqTrainingArguments
)

#==========================================
def prepare_pron_dataset(batch):
#==========================================
    batch['input_ids'] = batch['word']
    batch['labels'] = batch['pron']

    return batch

#==========================================
def prepare_ipa_dataset(batch):
#==========================================
    batch['input_ids'] = batch['word']
    batch['labels'] = batch['ipa']

    return batch

@dataclass
#==========================================
class DataCollatorWithPadding:
#==========================================
    tokenizer: AutoTokenizer
    padding: Union[bool, str] = True

    def __call__(self, features: List[Dict[str, Union[List[int], torch.Tensor]]]) -> Dict[str, torch.Tensor]:
        # split inputs and labels since they have to be of different lenghts and need
        # different padding methods
        words = [feature["input_ids"] for feature in features]
        prons = [feature["labels"] for feature in features]

        batch = self.tokenizer(words, padding=self.padding, add_special_tokens=False,
                               return_attention_mask=True, return_tensors='pt')
        pron_batch = self.tokenizer(prons, padding=self.padding, add_special_tokens=True,
                                    return_attention_mask=True, return_tensors='pt')

        # replace padding with -100 to ignore loss correctly
        batch['labels'] = pron_batch['input_ids'].masked_fill(pron_batch.attention_mask.ne(1), -100)

        return batch

#==========================================
def compute_metrics(pred):
#==========================================
    labels_ids = pred.label_ids
    pred_ids = pred.predictions

    pred_str = tokenizer.batch_decode(pred_ids, skip_special_tokens=True)
    labels_ids[labels_ids == -100] = tokenizer.pad_token_id
    label_str = tokenizer.batch_decode(labels_ids, skip_special_tokens=True)

    cer = cer_metric.compute(predictions=pred_str, references=label_str)
    wer = wer_metric.compute(predictions=pred_str, references=label_str)
    return {"cer": cer, 'wer': wer}

### Main ###
if __name__ == '__main__':
    with open("./config/t5_config.json") as config_file:
        args = AttrDict(json.load(config_file))
        for k, v in args.items():
            print(f"[run_T5Charsiu] {k} - {v}")

    # setting the evaluation metrics
    cer_metric = load_metric("cer") # character error rate
    wer_metric = load_metric("wer")

    # 단어와 문장에서 오류 비교 하기 위해 모델
    is_compare_word_and_sent = False
    if is_compare_word_and_sent:
        model = T5ForConditionalGeneration.from_pretrained(args.checkpoint)

        training_args = Seq2SeqTrainingArguments(
            predict_with_generate=True,
            generation_num_beams=5,
            evaluation_strategy="steps",
            per_device_train_batch_size=args.train_batch_size,
            per_device_eval_batch_size=args.eval_batch_size,
            output_dir=args.output_dir,
            logging_steps=args.logging_steps,
            save_steps=args.save_steps,
            eval_steps=args.eval_steps,
            save_total_limit=2
        )

        trainer = Seq2SeqTrainer(
            model=model,
            tokenizer=tokenizer,
            args=training_args,
            compute_metrics=compute_metrics,
            data_collator=data_collator
        )

        eval_results = trainer.evaluate(eval_dataset=test_dataset, num_beams=5)
        print(eval_results)
        with open(os.path.join(args.output_dir, 'results'), 'w') as out:
            out.write('%s\t%s\t%s\n'%(args.language,eval_results['eval_cer'], eval_results['eval_wer']))
from transformers import T5ForConditionalGeneration, AutoTokenizer
from utils.data_parser import SIG_parser, NiklParser

import argparse
import torch
import os
import json

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

    is_nikl = True
    if args.train:
        if not is_nikl:
            sig_parser = SIG_parser(src_dir='./data/en/sigmorphon')
            train_data = sig_parser.sig_data_load(target_lang="eng_us", mode="train")
            train_dataset = train_data.map(prepare_pron_dataset)

            dev_data = sig_parser.sig_data_load(target_lang="eng_us", mode="dev")
            dev_dataset = dev_data.map(prepare_pron_dataset)
        else:
            nikl_parser = NiklParser(src_dir="") # For Load Dataset
            train_data, dev_data, test_data = nikl_parser.load_nikl_data(target_path="data/NIKL/for_byT5.txt")
            train_dataset = train_data.map(prepare_ipa_dataset)
            dev_dataset = dev_data.map(prepare_ipa_dataset)
            test_dataset = test_data.map(prepare_ipa_dataset)

        tokenizer = AutoTokenizer.from_pretrained("google/byt5-small")
        data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

        # intitalizing the model
        print('Loading pretrained model...')
        model = T5ForConditionalGeneration.from_pretrained(args.model_name)

        training_args = Seq2SeqTrainingArguments(
            predict_with_generate=True,
            generation_num_beams=5,
            evaluation_strategy="steps",
            per_device_train_batch_size=args.train_batch_size,
            per_device_eval_batch_size=args.eval_batch_size,
            num_train_epochs=args.epochs,
            gradient_accumulation_steps=args.gradient_accumulation,
            learning_rate=args.learning_rate,
            warmup_steps=args.warmup_steps,
            lr_scheduler_type="cosine",
            fp16=args.fp16,
            output_dir=args.output_dir,
            logging_steps=args.logging_steps,
            save_steps=args.save_steps,
            eval_steps=args.eval_steps,
            save_total_limit=2,
            load_best_model_at_end=True
        )

        trainer = Seq2SeqTrainer(
            model=model,
            tokenizer=tokenizer,
            args=training_args,
            compute_metrics=compute_metrics,
            train_dataset=train_dataset,
            eval_dataset=dev_dataset,
            data_collator=data_collator,
        )

        trainer.train()
        trainer.save_model(args.output_dir)

    if args.evaluate:
        if not is_nikl:
            sig_parser = SIG_parser(src_dir='./data/en/sigmorphon')
            test_data = sig_parser.sig_data_load(target_lang="eng_us", mode="test")
            test_dataset = test_data.map(prepare_pron_dataset)
        else:
            nikl_parser = NiklParser(src_dir="")  # For Load Dataset
            train_data, dev_data, test_data = nikl_parser.load_nikl_data(target_path="data/NIKL/for_byT5.txt")
            train_dataset = train_data.map(prepare_ipa_dataset)
            dev_dataset = dev_data.map(prepare_ipa_dataset)
            test_dataset = test_data.map(prepare_ipa_dataset)
        tokenizer = AutoTokenizer.from_pretrained("google/byt5-small")
        data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

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
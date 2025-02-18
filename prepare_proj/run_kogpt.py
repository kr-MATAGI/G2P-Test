from transformers import AutoModelForCausalLM, AutoTokenizer
from utils.data_parser import SIG_parser

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
    Seq2SeqTrainingArguments,
    TrainingArguments,
    Trainer
)


#==========================================
def prepare_dataset(batch):
#==========================================
    batch['input_ids'] = batch['word']
    batch['labels'] = batch['pron']

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
        # batch['labels'].shape : (32, 35)
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

### MAIN ##
if __name__ == "__main__":
    with open("./config/kogpt_config.json") as config_file:
        args = AttrDict(json.load(config_file))
        for k, v in args.items():
            print(f"[run_kogpt] {k} - {v}")

    # setting the evaluation metrics
    cer_metric = load_metric("cer")  # character error rate
    wer_metric = load_metric("wer")

    if args.train:
        sig_parser = SIG_parser(src_dir='./data/kr/sigmorphon')
        train_data = sig_parser.sig_data_load(target_lang="kor", mode="train")
        train_dataset = train_data.map(prepare_dataset)

        dev_data = sig_parser.sig_data_load(target_lang="kor", mode="dev")
        dev_dataset = dev_data.map(prepare_dataset)

        tokenizer = AutoTokenizer.from_pretrained(
            args.model_name, revision=args.revision,
            bos_token='[BOS]', eos_token='[EOS]', unk_token='[UNK]', pad_token='[PAD]', mask_token='[MASK]'
        )
        data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

        # intitalizing the model
        print('Loading pretrained model...')
        model = AutoModelForCausalLM.from_pretrained(
            args.model_name, revision=args.revision,
            pad_token_id=tokenizer.eos_token_id,
            torch_dtype='auto', low_cpu_mem_usage=True
        ).to(device='cuda', non_blocking=True)
        prompt = 'youtube ipa:'
        with torch.no_grad():
            tokens = tokenizer.encode(prompt, return_tensors='pt').to(device='cuda', non_blocking=True)
            gen_tokens = model.generate(tokens, do_sample=True, temperature=0.8, max_length=64)
            generated = tokenizer.batch_decode(gen_tokens)[0]
            print(generated)

        training_args = TrainingArguments(
            # predict_with_generate=True,
            # generation_num_beams=5,
            evaluation_strategy="steps",
            per_device_train_batch_size=args.train_batch_size,
            per_device_eval_batch_size=args.eval_batch_size,
            num_train_epochs=args.epochs,
            gradient_accumulation_steps=args.gradient_accumulation,
            learning_rate=args.learning_rate,
            warmup_steps=args.warmup_steps,
            # lr_scheduler_type="cosine",
            fp16=args.fp16,
            output_dir=args.output_dir,
            logging_steps=args.logging_steps,
            save_steps=args.save_steps,
            eval_steps=args.eval_steps,
            save_total_limit=2,
            load_best_model_at_end=True
        )

        trainer = Trainer(
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
        sig_parser = SIG_parser(src_dir='./data/kr/sigmorphon')
        test_data = sig_parser.sig_data_load(target_lang="kor", mode="test")
        test_dataset = test_data.map(prepare_dataset)

        tokenizer = AutoTokenizer.from_pretrained(
            args.model_name, revision=args.revision,
            bos_token='[BOS]', eos_token='[EOS]', unk_token='[UNK]', pad_token='[PAD]', mask_token='[MASK]'
        )
        data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

        model = AutoModelForCausalLM.from_pretrained(args.checkpoint)

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
            out.write('%s\t%s\t%s\n' % (args.language, eval_results['eval_cer'], eval_results['eval_wer']))
# LazyReview: A Dataset for Uncovering Lazy Thinking in NLP Peer Reviews 
>  **Abstract**
>
> Peer review is a cornerstone of quality control in scientific publishing. With the increasing workload, the unintended use of `quick' heuristics, referred to as \emph{lazy thinking}, has emerged as a recurring issue compromising review quality. Automated methods to detect such heuristics can help improve the peer-reviewing process. However, there is limited NLP research on this issue, and no real-world dataset exists to support the development of detection tools. This work introduces LazyReview, a dataset of peer-review sentences annotated with fine-grained lazy thinking categories. Our analysis reveals that Large Language Models (LLMs) struggle to detect these instances in a zero-shot setting. However, instruction-based fine-tuning on our dataset significantly boosts performance by 10-20 performance points, highlighting the importance of high-quality training data. Furthermore, a controlled experiment demonstrates that reviews revised with \emph{lazy thinking} feedback are more comprehensive and actionable than those written without such feedback. We will release our dataset and the enhanced guidelines that can be used to train junior reviewers in the community.
>

<p align="center">
<img src="assets/logo.png" width="500">
</p>


Contact person: [Sukannya Purkayastha](mailto:sukannya.purkayastha@tu-darmstadt.de)

[UKP Lab](https://www.ukp.tu-darmstadt.de/) | [TU Darmstadt](https://www.tu-darmstadt.de/
)

Don't hesitate to send us an e-mail or report an issue, if something is broken (and it shouldn't be) or if you have further questions.

> This repository contains experimental software and is published for the sole purpose of giving additional background details on the respective publication.

## Setup and WorkFlow
For running the experiments, one needs to install necessary packages that we provide in the ``requirements.txt`` file as below:
>
```bash
conda create -n lazyreview python=3.10
pip install -r requirements.txt
```

>
>

## Data download
One needs to first download the data for these experiments available in this [link](). The directory has the following structure:
```
├── instruction_tuned
│   ├── coarse_grained
│   │   ├── lazy_thinking_coarse_grained_test.jsonl
│   │   ├── lazy_thinking_coarse_grained_test_with_eg.jsonl
│   │   ├── lazy_thinking_coarse_grained_train.jsonl
│   │   └── lazy_thinking_coarse_grained_train_with_eg.jsonl
│   ├── fine_grained
│   │   ├── lazy_thinking_fine_grained_test.jsonl
│   │   ├── lazy_thinking_fine_grained_test_with_eg.jsonl
│   │   ├── lazy_thinking_fine_grained_train.jsonl
│   │   └── lazy_thinking_fine_grained_train_with_eg.jsonl
└── zero_shot
    ├── Round 2_data .tsv
    ├── Round1_data .tsv
    └── Round3_data .tsv
```
To reproduce our zero-shot experiments in RQ1 and RQ2 from sec 3 of our paper, use the roundwise data in the folder ```zero_shot```. To perfrom instruction tuning with only ```LazyReview``` data, use the data contained in the folder ```instruction_tuned``` (**coarse_grained**, **fine_grained**). The extension ```with_eg``` for the files (e.g., ```lazy_thinking_coarse_grained_test_with_eg.jsonl```) specifies the setup where we donot use the review but only the target segment to do the prediction. 

## Zero-Shot Experiments
For inference, here's an example that uses LLaMa 7B-chat for the fine-grained evaluation:
```
export $round=1
export $output_dir=output
for model_name in meta-llama/Llama-2-7b-chat-hf
do
    python /storage/ukp/work/purkayastha/jupyter_test/vllm_codes/coarse_grained/classify_problematic_only_eg.py \
    --round $round \
    --model $model_name \
    --output_path $output_dir \
    --data_path data/zero_shot/Round1_data .tsv
done
```
For the coarse-grained evaluation, pass in the argument ```--problematic```. For the in-context learning results, you additionally neeed the flags ```--icl``` and ```--method $method_name```. The $method_name neeeds to be one of the follwoing: `random`, `mdl`, `top_k`, `bm25`, `vote_k`.

For evaluation, heres' the command:
```
export $model_name=Llama-2-7b-chat-hf
python evaluation/gpt3_evaluation.py \
--model_path gpt-35-turbo-0613-16k \
--data_path $output_dir/$model_name/zero_shot.csv
```
For accuracy calculation:
```
python evaluation/acc_gpt_eval.py \
--output_path $output_dir/$model_name
```

## Instruction Tuning Experiments:
We use the [open-instruct](https://github.com/allenai/open-instruct) framework from allenai to perform instruction-tuning. We need one directory to save the model ```$output_dir``` and another to save the merged-lora model, ```$new_output_dir```. The training script is a s follows:
```
for model_name in "meta-llama/Llama-2-7b-chat-hf"
    do
        accelerate launch \
            --mixed_precision bf16 \
            --num_machines 1 \
            --num_processes 4 \
            --use_deepspeed \
            --main_process_port=12547 \
            --deepspeed_config_file open-instruct/ds_configs/stage3_no_offloading_accelerate.conf \
            open-instruct/open_instruct/finetune.py \
            --model_name_or_path $model_name \
            --gradient_checkpointing \
            --use_lora \
            --lora_rank 64 \
            --trust_remote_code \
            --lora_alpha 16 \
            --lora_dropout 0.1 \
            --tokenizer_name $model_name \
            --use_slow_tokenizer \
            --train_file data instruction_tuned/percentage_data/without_review/sciriff_lazy_thinking_fg_cg.jsonl \
            --preprocessing_num_workers 128 \
            --per_device_train_batch_size 1 \
            --gradient_accumulation_steps 16 \
            --learning_rate 1e-4 \
            --lr_scheduler_type linear \
            --warmup_ratio 0.03 \
            --seed 42 \
            --weight_decay 0. \
            --num_train_epochs 2 \
            --output_dir $output_dir &&

        python open-instruct/open_instruct/merge_lora.py \
            --base_model_name_or_path $model_name \
            --lora_model_name_or_path $output_dir \
            --output_dir $new_output_dir$ \
            --save_tokenizer
```
For the evaluation, one needs to pass the folder name, ```$model_path``` where the merged_lora model is saved and a save_path ```$save_path``` where the inferences are stored. The evaluation script for a LoRa-based LLaMa 7B model is as follows:
```
for model_name in 'lora_merged_meta-llama/Llama-2-7b-chat-hf'
do
    python open-instruct/eval/lazy_thinking/eval.py \
    --dataset  data/instruction_tuned/lazy_thinking_fine_grained_test_with_eg.jsonl\
    --model_path $model_path/$model_name \
    --merged_lora \
    --output_dir $save_path/
done
```

## Citation

```bib
@article{tbd,
  title = {LazyReview: A Datset for uncovering lazy thinking in Peer Reviews},
  author = {Purkayastha, Sukannya and Li, Zhaung and Lauscher, Anne and Qu, Lizhen  and Gurevych, Iryna},
  year = 2025,
  month = apr,
  journal = {arXiv preprint},
  url = {},
  eprint = {},
  archiveprefix = {arXiv},
  primaryclass = {cs.AI},
}
```
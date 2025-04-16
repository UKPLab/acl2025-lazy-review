# LazyReview: A Dataset for Uncovering Lazy Thinking in NLP Peer Reviews
[![License](https://img.shields.io/github/license/UKPLab/ukp-project-template)](https://opensource.org/licenses/Apache-2.0)
[![Python Versions](https://img.shields.io/badge/Python-3.10-blue.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![arXiv](https://img.shields.io/badge/arXiv-2504.11042-b31b1b.svg)](https://arxiv.org/abs/2504.11042)
>  **Abstract**
>
> Peer review is a cornerstone of quality control in scientific publishing. With the increasing workload, the unintended use of `quick' heuristics, referred to as *lazy thinking*, has emerged as a recurring issue compromising review quality. Automated methods to detect such heuristics can help improve the peer-reviewing process. However, there is limited NLP research on this issue, and no real-world dataset exists to support the development of detection tools. This work introduces LazyReview, a dataset of peer-review sentences annotated with fine-grained lazy thinking categories. Our analysis reveals that Large Language Models (LLMs) struggle to detect these instances in a zero-shot setting. However, instruction-based fine-tuning on our dataset significantly boosts performance by 10-20 performance points, highlighting the importance of high-quality training data. Furthermore, a controlled experiment demonstrates that reviews revised with *lazy thinking* feedback are more comprehensive and actionable than those written without such feedback. We will release our dataset and the enhanced guidelines that can be used to train junior reviewers in the community.
>
The repository contains codes to reproduce the zero-shot experiments for the paper along with instruction-tuning LLMs on our newly released dataset, ```LazyReview```. We support chat versions of the LLaMa, Gemma, Qwen, Yi, Mistral and SciTulu family of models.

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
$ conda create -n lazyreview python=3.10
$ conda activate lazyreview
$ pip install -r requirements.txt
```

>
>

## Data download
One needs to first download the data for these experiments available in this [link]() and put that within the   ```dataset``` folder. The directory has the following structure:
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
    ├── Round2_data.tsv
    ├── Round1_data.tsv
    └── Round3_data.tsv
```
To reproduce our zero-shot experiments in RQ1 and RQ2 from sec 3 of our paper, use the roundwise data in the folder ```zero_shot```. To perfrom instruction tuning with only ```LazyReview``` data, use the data contained in the folder ```instruction_tuned``` (**coarse_grained**, **fine_grained**). The extension ```with_eg``` for the files (e.g., ```lazy_thinking_coarse_grained_test_with_eg.jsonl```) specifies the setup where we donot use the review but only the target segment to do the prediction. 

## Zero-Shot Experiments
For inference, here's an example that uses LLaMa 7B-chat for the fine-grained evaluation:
```
export $round=1
export $output_dir=output
for model_name in meta-llama/Llama-2-7b-chat-hf
do
    python src/zero_shot/classification.py \
    --round $round \
    --model $model_name \
    --output_path $output_dir \
    --data_path dataset/zero_shot/Round1_data.tsv
done
```
For the coarse-grained evaluation, pass in the argument ```--problematic```. For the in-context learning results, you additionally neeed the flags ```--icl``` and ```--method```. The ```--method``` expects one of the follwoing: `random`, `mdl`, `top_k`, `bm25`, `vote_k`. The ``--round`` argument specifies which round of annotation data you want to do inference on (options are: 1,2,3). The ```--output_path``` needs the path where the outputs will be stored. The ```--data_path``` should point to the dataset path where a particular round's data is stored (e.g., For round 1, pass ```dataset/zero_shot/Round1_data.tsv```). This code would store the output in a ```zero_shot.csv```. For the above example, the file path would be ```output/Llama-2-7b-chat-hf/zero_shot.csv```. The ``--model`` argument takes the huggingface model name (e.g., [meta-llama/Llama-2-7b-chat-hf](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf)). In our paper, we use the following models:

| Name     | Sizes | 🤗 model links   |
| :---: | :---: | :---: |
| LLaMa 2 chat    |  7B, 13B | [meta-llama/Llama-2-7b-chat-hf](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf), [meta-llama/Llama-2-13b-chat-hf](https://huggingface.co/meta-llama/Llama-2-13b-chat-hf) |
| Qwen chat  | 7B | [Qwen/Qwen-7B-Chat](https://huggingface.co/Qwen/Qwen-7B-Chat) |
| Yi chat | 6B | [01-ai/Yi-1.5-6B-Chat](https://huggingface.co/01-ai/Yi-1.5-6B-Chat) |
| Mistral Instruct    | 7B   | [mistralai/Mistral-7B-Instruct-v0.1](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1)  |
| Gemma instruction-tuned| 7B | [google/gemma-2-2b-it](https://huggingface.co/google/gemma-2-2b-it)  |
| SciTulu | 7B | [allenai/scitulu-7b](https://huggingface.co/allenai/scitulu-7b) |



For **evaluation**, here is an example command:
```
export $model_name=Llama-2-7b-chat-hf
python evaluation/gpt3_evaluation.py \
--model_path gpt-35-turbo-0613-16k \
--data_path $output_dir/$model_name/zero_shot.csv
```
```--model_path``` accepts the GPT-based model deployment name (e.g., ```gpt-35-turbo-0613-16k```). ```--data_path``` needs the location where the inference outputs from the different models are stored after running the ```src/zero_shot/classification.py``` code. As per our convention, if the default ```$output_dir``` is ```output``` then data_dir would look something like: ```output/Llama-2-7b-chat-hf/zero_shot.csv```.

For accuracy calculation:
```
python evaluation/acc_gpt_eval.py \
--output_path $output_dir/$model_name
```
```--output_path``` needs the path to the ```zero_shot.csv``` file generated for the LLM models. For the running example, this would be ```output/Llama-2-7b-chat-hf```.

## Instruction Tuning Experiments:
We use the [open-instruct](https://github.com/allenai/open-instruct) framework from allenai to perform instruction-tuning. We need one directory to save the model ```$output_dir``` and another to save the merged-lora model, ```$new_output_dir```. For details on the training arguments, please refer to open-instruct arguments explained [here](https://github.com/allenai/open-instruct/tree/main/scripts). The **training script** is as follows:
```
for model_name in "meta-llama/Llama-2-7b-chat-hf"
    do
        accelerate launch \
            --mixed_precision bf16 \
            --num_machines 1 \
            --num_processes 4 \
            --use_deepspeed \
            --main_process_port=12547 \
            --deepspeed_config_file src/instruction_tuned/open-instruct/ds_configs/stage3_no_offloading.conf \
            src/instruction_tuned/open-instruct/open_instruct/finetune.py \
            --model_name_or_path $model_name \
            --gradient_checkpointing \
            --use_lora \
            --lora_rank 64 \
            --trust_remote_code \
            --lora_alpha 16 \
            --lora_dropout 0.1 \
            --tokenizer_name $model_name \
            --use_slow_tokenizer \
            --train_file dataset/instruction_tuned/percentage_data/without_review/sciriff_lazy_thinking_fg_cg.jsonl \
            --preprocessing_num_workers 128 \
            --per_device_train_batch_size 1 \
            --gradient_accumulation_steps 16 \
            --learning_rate 1e-4 \
            --lr_scheduler_type linear \
            --warmup_ratio 0.03 \
            --seed 42 \
            --weight_decay 0. \
            --num_train_epochs 3 \
            --output_dir $output_dir &&

        python src/instruction_tuned/open-instruct/open_instruct/merge_lora.py \
            --base_model_name_or_path $model_name \
            --lora_model_name_or_path $output_dir \
            --lora_output_dir $new_output_dir$ \
            --save_tokenizer
```
The main arguments are ```--train_file``` which accepts the instruction-tuning files from the ```dataset/instruction_tuned``` folder (e.g., ```dataset/instruction_tuned/percentage_data/without_review/sciriff_lazy_thinking_fg_cg.jsonl```). ```--model_name_or_path``` accepts the model name as in huggingface hub (e.g., ```meta-llama/Llama-2-7b-chat-hf```). The ```--output_dir``` and ```--lora_model_name_or_path``` expects the same output directory where the trained models are saved. The ```--lora_output_dir``` should point to a new directory where the LoRa merged modules will be saved.


The **evaluation script** for a LoRa-tuned LLaMa 7B model is as follows:
```
for model_name in 'lora_merged_meta-llama/Llama-2-7b-chat-hf'
do
    python src/instruction_tuned/open-instruct/eval/lazy_thinking/eval.py \
    --dataset  dataset/instruction_tuned/lazy_thinking_fine_grained_test_with_eg.jsonl\
    --model_path $new_output_dir/$model_name \
    --merged_lora \
    --output_dir $save_path/
done
```
```--dataset``` takes in the test set for any setup (e.g., ```dataset/instruction_tuned/lazy_thinking_fine_grained_test_with_eg.jsonl```). ``--model_path`` takes the path to the merged lora model that we trained before. ``--output_dir`` takes in the path where the evaluation results should be saved.

## Citation

```bib
@misc{purkayastha2025lazyreviewdatasetuncoveringlazy,
      title={LazyReview A Dataset for Uncovering Lazy Thinking in NLP Peer Reviews}, 
      author={Sukannya Purkayastha and Zhuang Li and Anne Lauscher and Lizhen Qu and Iryna Gurevych},
      year={2025},
      eprint={2504.11042},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2504.11042}, 
}
```

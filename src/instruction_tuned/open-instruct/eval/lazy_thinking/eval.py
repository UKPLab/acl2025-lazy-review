import vllm, os
from datasets import load_dataset
from dotenv import load_dotenv, find_dotenv
from transformers import AutoModelForCausalLM, AutoTokenizer
from vllm import LLM, SamplingParams
import torch
import argparse
import pandas as pd

    

def post_process_test_set(dataset, tokenizer):
    #messages= dataset["messages"]
    prompts, completions, ids, titles = [], [], [], []
    for item in dataset:
        id = item['dataset']
        title = item['id']
        for m in item["messages"]:
            if m['role']=='user':
                prompt = m["content"]
                prompts.append(prompt)
            if m['role']=='assistant':
                completion = m['content']
                completions.append(completion)
        ids.append(id)
        titles.append(title)
    return prompts, completions, ids, titles
    
def format_prompts(tokenizer, prompts):
    all_messages = []
    for prompt in prompts:
        sample_dict = [{"role": "user", "content": prompt}]
        all_messages.append(sample_dict)
    
    formatted_prompts = [tokenizer.apply_chat_template(x, tokenize=False, add_generation_prompt=True) for x in all_messages]
    return formatted_prompts



def main(args):
    _ = load_dotenv(find_dotenv())
    access_token = os.getenv("HF_ACCESS_TOKEN_WRITE")
    if '.jsonl' in args.dataset:
        dataset = load_dataset("json", data_files=args.dataset, split="train")
    else:
        dataset = load_dataset(args.dataset, token = access_token, split="test")

    tokenizer = AutoTokenizer.from_pretrained(args.model_path, trust_remote_code=True)
    #model = AutoModelForCausalLM(args.model_path)


    all_prompts, completions, ids, titles = post_process_test_set(dataset, tokenizer)

    
    rev, weakness = [], []
    for pt in all_prompts:
        splits = pt.split('\nTarget')
        rev.append(splits[0].replace('\n',''))
        weakness.append('Target'+ splits[1].replace('\n',''))

    prompts = format_prompts(tokenizer, all_prompts)
    
    llm = LLM(model= args.model_path, dtype = torch.float16, tensor_parallel_size=1,trust_remote_code=True)
    sampling_params = SamplingParams(temperature=0, seed = 123, max_tokens=100)
    all_outputs = []
    outputs = llm.generate(prompts, sampling_params)
    
    for out in outputs:
        all_outputs.append(out.outputs[0].text.strip().replace('\n',''))
    
    print(all_outputs)
    
    df = pd.DataFrame({'id': ids, 'title': titles,'review': rev, 'weakness': weakness, 'mapping': completions, 'outputs': all_outputs})

    #df['outputs'] = all_outputs
    df['model'] = args.model_path

    if '.jsonl' in args.dataset:
        dataset_name = args.dataset.rsplit('.jsonl',1)[0]
        dataset_name = dataset_name.split('/')[-1]
    else:
        dataset_name = args.dataset.rsplit('/',1)[1]
    if args.merged_lora:
        model_name = args.model_path.rsplit('/', 2)
        model_name = '/'.join(x for x in model_name[1:])
    else:
        model_name = args.model_path.split('/')[1]
    print(args.output_dir)
    print(dataset_name)
    print(model_name)
    dataset_path = os.path.join(args.output_dir, dataset_name, model_name)
    print(dataset_path)
    os.makedirs(dataset_path, exist_ok=True)

    df.to_csv(f'{dataset_path}/zero_shot.csv', sep='\t', index=None)


    


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, default=None, help ='Put instruction tuned fine-grained and coarse-grained data')
    parser.add_argument('--model_path', type=str, help = 'Path to instruction tuned models')
    parser.add_argument('--output_dir',type=str, help = 'Path to output directory')
    parser.add_argument('--merged_lora', action='store_true', help='If using lora merged models')
    args = parser.parse_args()
    main(args)


    



from vllm import LLM, SamplingParams
import pandas as pd
from prompt_fine_grained.prompt_round1 import round1_prompt, round1_prompt2, round1_prompt3, round1_prompt_only_eg, round1_prompt2_only_eg, round1_prompt3_only_eg
from prompt_fine_grained.prompt_round2 import round2_prompt, round2_prompt2, round2_prompt3, round2_prompt_only_eg, round2_prompt2_only_eg, round2_prompt3_only_eg
from prompt_fine_grained.prompt_round3 import round3_prompt1, round3_prompt2, round3_prompt3, round3_prompt1_only_eg, round3_prompt2_only_eg, round3_prompt3_only_eg, round3_prompt_icl, round3_prompt2_icl, round3_prompt3_icl, round3_prompt_icl_only_example, round3_prompt2_icl_only_example, round3_prompt3_icl_only_example
from prompt_coarse_grained.problem_round1 import round1_prompt_problematic_only_eg, round1_prompt2_problematic_only_eg, round1_prompt3_problematic_only_eg, round1_prompt_problematic, round1_prompt2_problematic, round1_prompt3_problematic
from prompt_coarse_grained.problem_round2 import round2_prompt_problematic_only_eg, round2_prompt2_problematic_only_eg, round2_prompt3_problematic_only_eg, round2_prompt_problematic, round2_prompt2_problematic, round2_prompt3_problematic
from prompt_coarse_grained.problem_round3 import round3_prompt_problematic_only_eg, round3_prompt2_problematic_only_eg, round3_prompt3_problematic_only_eg, round3_prompt_problematic, round3_prompt2_problematic, round3_prompt3_problematic, round3_prompt_problematic_icl, round3_prompt2_problematic_icl, round3_prompt2_problematic_icl, round3_prompt_problematic_icl_only_eg, round3_prompt2_problematic_icl_only_eg, round3_prompt3_problematic_icl_only_eg

from icl_selection import Retriever
import argparse
import os
import torch
from transformers import AutoTokenizer

def replace_nan(item):
    if type(item)==float:
        return 'NONE'    
    return item


def create_prompt_and_review_format(tokenizer, prompt, icl, train_df, test_df, method, num_eg):
    all_prompts = []
    weakness = test_df['weakness'].tolist()
    review = test_df['review'].tolist()
    
    if icl:
        retrieved_demos = retrieve_examples(train_df, test_df, method, num_eg)
    else:
        retrieved_demos = []
    for wk, rv, demo in zip(weakness, review, retrieved_demos):
        prompt = format_icl(icl, demo, prompt)
        new_prompt  = prompt.replace('{{review}}', rv).replace('{{weakness}}', wk)
        all_prompts.append(new_prompt)
    
    formatted_prompts = format_prompt(tokenizer, all_prompts)
    return formatted_prompts


def get_prompt(args):
    if args.round == '1':
        return [round1_prompt, round1_prompt2, round1_prompt3]
    if args.round =='2':
        return [round2_prompt, round2_prompt2, round2_prompt3]
    if args.round =='3':
        return [round3_prompt1, round3_prompt2, round3_prompt3]
    if args.icl:
        return [round3_prompt_icl, round3_prompt2_icl, round3_prompt3_icl]
    
    elif args.problematic:
        if args.round == '1':
            return [round1_prompt_problematic, round1_prompt2_problematic, round1_prompt3_problematic]
        if args.round =='2':
            return [round2_prompt_problematic, round2_prompt2_problematic, round2_prompt3_problematic]
        if args.round =='3':
            return [round3_prompt_problematic, round3_prompt2_problematic, round3_prompt3_problematic]
        if args.icl:
            return [round3_prompt_problematic_icl, round3_prompt2_problematic_icl, round3_prompt2_problematic_icl]
        if args.only_eg:
            if args.round == '1':
                return [round1_prompt_only_eg, round1_prompt2_only_eg, round1_prompt3_only_eg]
            if args.round =='2':
                return [round2_prompt_only_eg, round2_prompt2_only_eg, round2_prompt3_only_eg]
            if args.round =='3':
                return [round3_prompt1_only_eg, round3_prompt2_only_eg, round3_prompt3_only_eg]
            if args.icl:
                return [round3_prompt_problematic_icl_only_eg, round3_prompt2_problematic_icl_only_eg, round3_prompt3_problematic_icl_only_eg]

    else:
        if args.only_eg:
            if args.round == '1':
                return [round1_prompt_problematic_only_eg, round1_prompt2_problematic_only_eg, round1_prompt3_problematic_only_eg]
            if args.round =='2':
                return [round2_prompt_problematic_only_eg, round2_prompt2_problematic_only_eg, round2_prompt3_problematic_only_eg]
            if args.round =='3':
                return [round3_prompt1_only_eg, round3_prompt2_only_eg, round3_prompt3_only_eg]
            if args.icl:
                return [round3_prompt_problematic_only_eg, round3_prompt2_problematic_only_eg, round3_prompt3_problematic_only_eg]


def retrieve_examples(train_df, test_df, method, num_eg):
    retriever = Retriever(train_df, test_df, num_eg)

    if method =='mdl':
        retrieved_demos = retriever.mdl()
    elif method =='vote_k':
        retrieved_demos = retriever.vote_k()
    elif method =='top_k':
        retrieved_demos = retriever.top_k()
    elif method =='bm25':
        retrieved_demos = retriever.bm25()
    else:
        retrieved_demos = retriever.random()

    return retrieved_demos    

def format_icl(icl, icl_list, prompt):
    string = ''
    if not icl:
        return prompt
    for elem in icl_list:
        weakness, review, mapping = elem
        string+= f'Full Review: {review}\nTarget Sentence: {weakness}\nThe lazy thinking class is: {mapping}\n\n'
    print(string)
    prompt = prompt.replace ('{{insert_example}}', string)
    print(prompt)
    return prompt


def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


def format_prompt(tokenizer, all_prompts):
    
    all_messages = []
    for prompt in all_prompts:
        sample_dict = [{"role": "user", "content": prompt}]
        all_messages.append(sample_dict)
    
    print(all_messages[0])
    formatted_prompts = [tokenizer.apply_chat_template(x, tokenize=False, add_generation_prompt=True) for x in all_messages]
    formatted_prompts = [f'{x}. The lazy thinking class is : ' for x in formatted_prompts]
        
    return formatted_prompts

def main(args):
    if args.sheet:
        data_path = f"https://docs.google.com/spreadsheets/d/{args.sheet_id}/export?format=csv"
        df = pd.read_csv(data_path)
    else:
        data_path = args.data_path
        df = pd.read_csv(data_path,sep='\t')
    if args.icl:
        train_df = pd.read_csv(args.train_data_path)
        train_df['mapping'] = train_df['mapping'].map(replace_nan)
        print(train_df)
    if args.problematic:
        all_vals = []
        for _, rows in df.iterrows():
            val = replace_nan(rows['mapping'])
            all_vals.append(val)
        df['mapping'] = all_vals 
    
    tokenizer = AutoTokenizer.from_pretrained(args.model, trust_remote_code=True)
    
    tensor_parallel_size=1
    if any(ext in args.model for ext in ['Mixtral', '70B']):
        quantization = 'awq'
        llm = LLM(model=args.model, dtype = 'auto', tensor_parallel_size=tensor_parallel_size,trust_remote_code=True, quantization = quantization)
    else:
        llm = LLM(model=args.model, dtype = torch.float16, tensor_parallel_size=tensor_parallel_size,trust_remote_code=True)
    print('Model loaded')



    prompts = get_prompt(args)
    i=0

    for prompt in prompts:
        all_prompts = create_prompt_and_review_format(tokenizer, prompt, args.icl, train_df, df, args.method, args.num_eg)
        print(all_prompts)
    
        sampling_params = SamplingParams(temperature=0, seed = 123, max_tokens=50)
    
    
        all_outputs = []
        outputs = llm.generate(all_prompts, sampling_params)
    
        for out in outputs:
            all_outputs.append(out.outputs[0].text.strip().replace('\n',''))
    

    
        df['outputs'] = all_outputs
        df['model'] = args.model

        parent_path, model_name = args.output_path.rsplit('/',1)
        parent_path = parent_path.rsplit('/',1)[0]
        if args.only_eg:
            full_out_path = os.path.join(parent_path,'only_eg', f'prompt_{i}', model_name)
        else:
            full_out_path = os.path.join(parent_path,f'prompt_{i}', model_name)
        os.makedirs(full_out_path, exist_ok=True)
    
    
        df.to_csv(os.path.join(full_out_path, 'zero_shot.csv'), sep='\t', index=False)
        i+=1


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--round', type=str, default=None)
    parser.add_argument('--sheet', action='store_true', help='If the data is in google sheets')
    parser.add_argument('--data_path', type=str, default=None)
    parser.add_argument('--model', type=str, default=None)
    parser.add_argument('--output_path', type=str, default=None)
    parser.add_argument('--sheet_id',type=str, default=None)
    parser.add_argument('--train_data_path',type=str, default=None)
    parser.add_argument('--icl', action='store_true', help='If using incontext learning')
    parser.add_argument('--problematic', action='store_true', help='If doing fine_grained classification')
    parser.add_argument('--method', type=str, default=None, help = 'Choose from: random/ mdl/ top_k/ bm25/ vote_k')
    parser.add_argument('--num_eg', type=str, default=None, help='Number of examples')

    args = parser.parse_args()
    main(args)

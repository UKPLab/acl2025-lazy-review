from gpt3_utils import cost_calculation, load_gpt
from gpt_eval_message import task_def, task_def_problematic
import pandas as pd
import argparse
import os

def main(args):
    client = load_gpt()
    models = ['gemma-1.1-7b-it', 'Llama-2-7b-chat-hf', 'Llama-2-13b-chat-hf', 'Mistral-7B-Instruct-v0.1', 'Qwen-7B-Chat', 'Yi-1.5-9B-Chat', 'scitulu-7B']
    rounds = [1,2,3]
    total=0
    if args.icl:
        rounds = ['bm25', 'random', 'top_k', 'vote_k']

    num_egs = [1,2,3]
    if args.problematic:
        task_def = task_def_problematic

    for round in rounds:
        for prompt in ['prompt_0', 'prompt_1', 'prompt_2']:
            for model in models:
                cost_m=0  
                for eg in num_egs:
                    output_preds = []
                    if os.path.exists(f'{args.data_path}/{round}/{eg}/{prompt}/{model}/zero_shot.csv'):
                        df = pd.read_csv(f'{args.data_path}/{round}/{eg}/{prompt}/{model}/zero_shot.csv', sep='\t')
                        print(f'{args.data_path}/{round}/{eg}/{prompt}/{model}/zero_shot.csv')
                
                        for _, rows in df.iterrows():
                            mapping = rows['mapping']
                            outputs = rows['outputs']

                            if type(mapping)==float:
                                mapping="not problematic"

                            if type(outputs)==float:
                                outputs="not problematic"

                            task_def_mod = task_def.replace('{{label}}', outputs).replace('{{gold_label}}', mapping)
                            new_message = [{'role': 'system', 'content': task_def_mod}]
    
                            deployment_name = args.model_path
                            response = client.chat.completions.create(model=deployment_name, messages=new_message, max_tokens=args.max_new_tokens, seed=args.seed)
                            cost = cost_calculation(prompt_price=0.0028,
                                      completion_price=0.0037,
                                      prompt_tokens=response.usage.prompt_tokens,
                                      completion_tokens=response.usage.completion_tokens)
                            total+=cost
                            cost_m+=cost
                            output_preds.append(response.choices[0].message.content)
                        df['gpt_predict'] = output_preds
                        print(cost_m)
                        f = open(f'{args.data_path}/{round}/{eg}/{prompt}/{model}/cost.txt','w')
                        f.write(f'Cost for this model:{str(cost_m)}')
                        f.close()

                        df.to_csv(f'{args.data_path}/{round}/{eg}/{prompt}/{model}/gpt_predict.csv', sep='\t')
    print(f'Total cost:{total}')


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--max_new_tokens', type=str, default=100)
    parser.add_argument('--seed', type=str, default=None)
    parser.add_argument('--model_path', type=str, default="gpt-35-turbo-0613-16k")
    parser.add_argument('--only_eg',action='store_true', help='with only eg')
    parser.add_argument('--icl', action='store_true', help='icl')
    parser.add_argument('--problematic', action='store_true', help='problematic')
    parser.add_argument('--data_path', type=str, default=None )
    args = parser.parse_args()
    main(args)

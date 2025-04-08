import pandas as pd
import os
import re
from collections import Counter
import argparse

def normalize(row):
    print(row['gpt_predict'])
    return_value = 'incorrect'
    
    if type(row['gpt_predict'])==float:
        return_value= 'incorrect'
    elif bool(re.search('^No|no', row['gpt_predict'])):
        return_value =  'incorrect'
    elif bool(re.search('^Yes|yes', row['gpt_predict'])):
        return_value =  'correct'
    elif bool(re.search('correct or incorrect', row['gpt_predict'])):
        return_value =  'incorrect'
    elif bool(re.search('is incorrect', row['gpt_predict'])):
        return_value =  'incorrect'
    elif bool(re.search('is correct', row['gpt_predict'])):
        return_value =  'correct'
    
    else:
        return_value =  'incorrect'
    return return_value



def main(args):
    df = pd.read_csv(os.path.join(args.output_path,'gpt_predict.csv'), sep='\t')
    #print(df)
    df['gpt_predict']= df.apply(normalize, axis=1)
    all_counts = Counter(df['gpt_predict'].tolist())
    f= open(os.path.join(args.output_path, 'gpt_results.txt'), 'w')
    for count in all_counts:
        f.write(f'{count}:{all_counts[count]}\n')
    acc = all_counts["correct"]/len(df)
    f.write(f'Accuracy:{acc*100}\n')
    f.close()


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_path', type=str)
    args = parser.parse_args()
    main(args)

    
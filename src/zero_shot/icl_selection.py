from openicl import DatasetReader, RandomRetriever, BM25Retriever, TopkRetriever, VotekRetriever, MDLRetriever
from datasets import Dataset, DatasetDict


class Retriever:
    def __init__(self, train_df, test_df, n):
        self.train_df = train_df
        self.test_df = test_df
        train_ds = Dataset.from_pandas(self.train_df)
        test_ds = Dataset.from_pandas(self.test_df)
        ds = DatasetDict({'train': train_ds, 'test': test_ds})
        self.num_eg = int(n)
        self.full_ds = DatasetReader(ds, input_columns=['weakness'], output_column='mapping')

    def idx_2_eg(self, idx_list):
        sample_list = self.train_df['weakness'].tolist()
        mapping_list = self.train_df['mapping'].tolist()
        review_list = self.train_df['review'].tolist()
        id_2_examples=  []
        for indices in idx_list:
            ins_list=[]
            for item in indices:
                ins_list.append((sample_list[item], review_list[item], mapping_list[item])) #weakness, review, mapping
            id_2_examples.append(ins_list) 
        return id_2_examples


    def random(self):
        retriever = RandomRetriever(self.full_ds, index_split='train', test_split='test', ice_num=self.num_eg)
        retrieved_idxs = retriever.retrieve()
        retrieved_examples = self.idx_2_eg(retrieved_idxs)
        return retrieved_examples


    def vote_k(self):
        retriever = VotekRetriever(self.full_ds, index_split='train', test_split='test', ice_num=self.num_eg)
        retrieved_idxs = retriever.retrieve()
        retrieved_examples = self.idx_2_eg(retrieved_idxs)
        return retrieved_examples
         


    def top_k(self):
        retriever = TopkRetriever(self.full_ds, index_split='train', test_split='test', ice_num=self.num_eg)
        retrieved_idxs = retriever.retrieve()
        retrieved_examples = self.idx_2_eg(retrieved_idxs)
        return retrieved_examples


    def bm25(self):
        retriever = BM25Retriever(self.full_ds, index_split='train', test_split='test', ice_num=self.num_eg)
        retrieved_idxs = retriever.retrieve()
        retrieved_examples = self.idx_2_eg(retrieved_idxs)
        return retrieved_examples


    def mdl(self):
        retriever = MDLRetriever(self.full_ds, index_split='train', test_split='test', ice_num=self.num_eg) # by default uses 'gpt-xl'
        retrieved_idxs = retriever.retrieve()
        retrieved_examples = self.idx_2_eg(retrieved_idxs)
        return retrieved_examples

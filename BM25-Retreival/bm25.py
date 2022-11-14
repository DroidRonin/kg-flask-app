import pandas as pd
from nltk.tokenize import word_tokenize
from rank_bm25 import *

def search_hits(query,data):
    data_list = data['tokenized_sents'].tolist()    #converting dataframe to list
    tokenized_query = [word_tokenize(i) for i in query]    #tokenizing elements of input list
    bm25 = BM25Okapi(data_list)    #creating bm25 indexing
    docs = bm25.get_top_n(tokenized_query, data_list, n=5)     #finding top 5 relevant hits from the index
    df_search = data[data['tokenized_sents'].isin(docs)]       #mapping hits back to the main file
    return df_search



if __name__ == '__main__':
    data = pd.read_csv("preprocessed.csv")    
    query = ["reinforcement learning", "svm", "cnn", "convolutional neural network"]   #list of words to query
    search = search_hits(query, data)                
    search.to_csv("relevant_finds.csv")    



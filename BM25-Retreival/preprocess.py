import pandas as pd
import nltk
from nltk.corpus import stopwords



def preprocess(df):

    stop = stopwords.words('english') 
    df['summary_clean'] = df['summary'].replace('[^a-zA-Z]', '', regex=True)  #removing non alphabet characters
    df['summary_clean'] = df['summary'].str.lower()    #lowercasing the letters
    df['summary_clean'] = df['summary_clean'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))  #removing stop words
    df['tokenized_sents'] = df.apply(lambda row: nltk.word_tokenize(row['summary_clean']), axis=1)  #tokenizing the rows of dataframe
    return df



if __name__ == '__main__':
    data = pd.read_csv("...")      #Reading the csv file
    processed_data = preprocess(data)             #preprocessing the data   
    processed_data.to_csv("preprocessed.csv")    #Writing the new csv file (BM25 compatible)

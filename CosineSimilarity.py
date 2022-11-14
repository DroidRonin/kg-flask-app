import pandas as pd
from gensim.models import Word2Vec
 

class CosineSimilarity():
    def __init__(self, dataframe, concepts):
        self.dataframe = dataframe
        self.concepts = concepts
    

    def measure_similarity(self):
        dataframe_min = pd.DataFrame(columns = ['source','edge','target'])   #Creating new dataframe which will contain the new results
        model = Word2Vec.load("word2vec.model")  #Load pre-trained model here
        threshold = 0.50
        for i in self.dataframe['source']:
            for j in concepts:
                try:
                        score = self.model.wv.similarity(i, j)   
                        if score > threshold:
                            self.concepts = i
                            dataframe_min = self.dataframe[self.dataframe['source'] == self.concepts]  #Appending the entries with highest score to the new dataframe
                except:
                        None
        return dataframe_min


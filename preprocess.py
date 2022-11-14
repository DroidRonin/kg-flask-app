import nltk
import regex as re


class preprocess(): 

    def __init__(self, query):
        self.query = query
    def process(query):
        sent = [each_string.lower() for each_string in query] 
        sent  = [re.sub('[^a-zA-Z0-9\d\s]+', '', _) for _ in sent]
        return sent




 

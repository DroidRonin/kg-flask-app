# kg-flask-app
Application to process input query, and display the knowledge graph

1. bm25.py in BM25-Retreival directory is for retrieving relevant documents based on given terms; preprocess.py creates tokenised tokens of the original dataset to be used for BM-25 search. 
2. flask.py processes the user query and projects a knowledge graph using networkx library.
3. get_triples.py returns the processed triples form input query. It uses the berkley neural parser to consider the whole noun-phrase and verb-phrase instead of the bottom-most node of the tree (overcoming the limitation offered by the package 'nlptriples').  It applies a brute-force method to get all the triples (good and bad) from the input text, also solving the inadequacy of triples problem by 'nlptriples'. 
4. CosineSimilarity.py finds the most relevant triples using an embeddings model (word2vec trained, not included here) and returns a dataframe of final triples 
5. preprocess.py removes special characters and lowercases the data. It does not tokenise it, since that is handled by the get_triples.py file.  

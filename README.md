# kg-flask-app
Application to process input query, and display the knowledge graph

1. bm25.py in BM25-Retreival directory is for retrieving relevant documents based on given terms. 
2. flask.py processes the user query and projects a knowledge graph using networkx library.
3. get_triples.py returns the processed triples form input query. It modifies the existing benepar neural parser to consider the whole noun-phrase and verb-phrase instead of the right-most node of the tree. It applies a brute-force method to get all the triples (good and bad) within the input text.
4. CosineSimilarity.py finds the most relevant triples using an embeddings model and returns a dataframe of final triples 

# kg-flask-app
Application to process input query, and display the knowledge graph

1. bm25.py in BM25-Retreival directory is for retrieving relevant documents based on key-words 
2. flask.py takes the user query and projects a knowledge graph. 
3. get_triples.py returns the processed triples form input query needed for flask.py
4. CosineSimilarity.py finds the most relevant triples using an embeddings model and returns a dataframe of final triples 

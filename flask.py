from flask import Flask, render_template, request, send_file, jsonify
import pandas as pd
from py2neo import Graph, Node, Relationship
from gettriples import *
from preprocess import *
from spellchecker import spellCheck
from CosineSimilarity import *
import pickle
from io import BytesIO
import requests
import warnings
import matplotlib.pyplot as plt
import networkx as nx
import socket
import nltk
from Neo4J_API import *



HOST = ''  # Standard loopback interface address (localhost)
PORT = ''        # Port to listen on (non-privileged ports are > 1023)


app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/query/')

 
def query():                                 #Calls the elasticsearch API
    global var_1
    global articles
    global sent
    api_url = ""
    requestive = { "user_input": sent}
    response = requests.post(api_url, json=requestive)
    dict_ = response.json()
    topics_dict = dict_['Topic']
    papers_dict = dict_['URL/PDF']

    topics = []
    urls = [] 
    for i in topics_dict.items():
        topics.append(i[1])
    for i in papers_dict.items():
        urls.append(i[1])
    
    df = pd.DataFrame(list(zip(topics, urls)), columns =['Topics', 'URLs'])
    df['Index'] = df.index
    first_column = df.pop('Index')
    df.insert(0, 'Index', first_column)

  
    return render_template('query.html', topics_dict = topics_dict, papers_dict = papers_dict, variable_val = response.json(), column_names=df.columns.values, row_data=list(df.values.tolist()),
                           link_column="Articles", zip=zip, concepts = list(kg_df), relations = relations, targets = list(targets))

@app.route('/')
def welcome():
    return render_template('form_changes.html')


@app.route('/result', methods=['POST', 'GET'])
def result():
    kg_df1 = pd.read_csv('')
    global var_1
    global search
    global concepts
    global relations
    global targets
    global img
    global sent
    global key


    searchspace = list()  #Creating an empty searchspace
    var_1 = request.form.get("var_1", type=str)
    #print("Var 1 at line 60: ", var_1, request.form)
    var_3 = var_1
    sent = nltk.word_tokenize(var_1)
    sent = [w.replace('-', ' ') for w in sent]
    sent = [each_string.lower() for each_string in sent]
    print(sent, "from line 64")
    test =  ['contact lense production', 'complexity level', 'personalization']   #Default inputs
    sent2 = nlp(var_1)
    sent2 = list(sent2.sents)[0]


    triples = BNP(sent2)            #Get all the relevant triples
 
    if 'contact lense production' in sent:
        sent = sent + test
    
    approach = request.form.get("approach")
    deep_learning = ['convolutional nn', 'feed forward nn', 'deep learning', 'classification nonlinear', 'deep boltzmann machine']
    statistical_learning = ['linear regression', 'non linear regression', 'statistical learning']
    machine_learning = ['machine learning', 'knn', 'kmeans', 'decision tree']
    empty = []
    if(approach == 'Deep Learning'):
        sent = sent + deep_learning
    elif(approach == 'Machine Learning'):
        sent = sent + machine_learning
    elif(approach == 'Statistical Learning'):
        sent = sent + statistical_learning
    elif(approach == 'None'):
        sent = sent + empty

    operation = request.form.get("operation")
    classifications = ['convolutional nn', 'feed forward nn', 'clustering nonlinear', 'classification nonlinear', 'decision tree']
    regressions = ['feed forward nn', 'linear regression', 'non linear regression']
    empty = []
    if(operation == 'Classification'):
        sent = sent + classifications
    elif(operation == 'Regression'):
        sent = sent + regressions
    elif(operation == 'None'):
        sent = sent + empty


    orientation = request.form.get("orientation")
    decen = ['decentralized', 'decentralized architectural pattern']
    cen = ['centralized' , 'centralized architectural pattern', 'pi']
    
    if(orientation == 'Decentralized'):
        sent = sent + decen
    elif(orientation == 'Centralized'):
        sent = sent + cen
    elif(orientation == 'None'):
        sent = sent + empty


    searchspace_df = pd.DataFrame(triples, columns = ['source', 'edge', 'target'])
    concepts = searchspace_df.source.tolist()
    relations = searchspace_df.edge.tolist()
    targets = searchspace_df.target.tolist()

   
    concepts = set(concepts) 
    relations = set(relations)
    targets = set(targets)        #find unique concepts, relations and targets

    #invalid = {'source': ['None'], 'target': ['None'], 'edge': ['None']}   #Default KG
    conn = Neo4jConnection(uri="", user="", pwd="")  #Enter uri, username and password here
    query1 = '''MATCH (n:Resource)-[r]-() 
    WITH type(r) AS rel, startnode(r) AS sn, n AS target
    RETURN rel, sn.uri, target.uri;'''    #Query to get all the triples from neo4j KG
    total_kg = pd.DataFrame([dict(_) for _ in conn.query(query1, db='neo4j')]) #parse fetched triples into the dataframe format
    total_kg = total_kg.rename(columns={"sn.uri": "source", "rel": "edge", "target.uri": "target", "node.target_label": "label"}) #standardize column names

    w2v = CosineSimilarity()
    result_graph= w2v.measure_similarity(concepts, total_kg)   #find the most relevant triples that match concepts from the user query


    
    miniG = nx.from_pandas_edgelist(result_graph,'source', 'target', create_using=nx.MultiDiGraph())
    pos = nx.spring_layout(miniG)
    e_labels = {(result_graph.source[i], result_graph.target[i]):result_graph.edge[i] for i in range(len(result_graph['edge']))}
    plt.figure(figsize=(20,20))

    nx.draw_networkx_edge_labels(miniG, pos, edge_labels= e_labels, )
    nx.draw(miniG, with_labels=True, node_color='orange', node_size=1500, edge_cmap=plt.cm.Blues, pos = pos, arrows=True,
        arrowstyle="-",)
    
    print("Line number 89")
    img = BytesIO() # file-like object for the image
    plt.savefig(img) # save the image to the stream
    img.seek(0) # writing moved the cursor to the end of the file, reset
    plt.clf() # clear pyplot
    
    
    # return render_template('form2.html', query = var_1)
    return send_file(img, mimetype='image/png', as_attachment=True,attachment_filename='%s.jpg' % key )
   

@app.route('/graph', methods=['POST','GET'])
def graph_plot():
    global key
    file = "%s.jpg" % key
    #return send_file(img, mimetype='image/png')
    return send_file(file, mimetype='image/jpg')


if __name__ == '__main__':
    app.run(debug=True)
    app.run('0.0.0.0', port=PORT)

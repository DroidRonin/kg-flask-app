
import benepar
import spacy
import regex


def get_subject_phrase(doc):
    
    for token in doc:
        if ("subj" in token.dep_):
            subtree = list(token.subtree)
            start = subtree[0].i
            end = subtree[-1].i + 1
            subj = doc[start:end].text
            subj = regex.sub(r'\b[A-Z]+\b', '', subj)
            subj = regex.sub(r'\W+', ' ', subj)
            return subj

def get_object_phrase(doc):
    for token in doc:
        if ("dobj" in token.dep_):
            subtree = list(token.subtree)
            start = subtree[0].i
            end = subtree[-1].i + 1
            obj = doc[start:end].text
            obj = regex.sub(r'\W+', ' ', obj)
            obj = regex.sub(r'\b[A-Z]+\b', '', obj)
            return obj

def BNP(sent):
    nlp = spacy.load('en_core_web_md')
    nlp.add_pipe('benepar', config={'model': 'benepar_en3'})
    doc = nlp(sent)
    sent = list(doc.sents)[0]
    constituents = sent._.parse_string
    REGEX_FILTER_NP = regex.compile(r"(?<=\NP)(.*?)(?=\)\))")           #match entire NP phrase in the tree
    REGEX_FILTER_VP = regex.compile(r"(?<=\(VP)(.*?)(?=\))")            #match entire VP phrase in the tree      

    NP = list()
    VP = list()
    for group in regex.findall(REGEX_FILTER_NP, constituents):
        NP.append(group)
  
    clean_NP = list()
    clean_VP = list()

    for i in NP:
        m = regex.sub(r'\b[A-Z]+\b', '', i)
        clean_NP.append(regex.sub(r'\W+', ' ', m))                      #takes only valid NP tokens from the syntax tree 
    
    for group in regex.findall(REGEX_FILTER_VP, constituents):
        VP.append(group)

    for i in VP:
        m = regex.sub(r'\b[A-Z]+\b', '', i)
        clean_VP.append(regex.sub(r'\W+', ' ', m))
    if len(clean_VP) <= 0:
        return False
    clean_VP = clean_VP[0]                                              #takes only valid VP tokens from the syntax tree 
    
    subj_list = str(get_subject_phrase(doc))
    obj_list = str(get_object_phrase(doc))

    subj = []
    obj =[]
    # print("Subject: ", subj_list)
    # print("Object: ",obj_list)
    for np_item in clean_NP:
        np_item = str(np_item)
        try:
            # print(np_item)
            
            ######### Comment if and elif if you dont want to check subject and object of sentences before appending to list
            if (np_item in subj_list or subj_list in np_item) and np_item != " ":
                subj.append(np_item)
            elif (np_item in obj_list or obj_list in np_item)  and np_item != " ":
                obj.append(np_item)

            ######## Comment append statement below if you do want to perform subject object check
            # subj.append(np_item)
            # obj.append(np_item)
        except TypeError:
            continue
        
    
    triple = triples.append(clean_VP)
    subj = set(subj)
    obj = set(obj)
    return([subj,obj], clean_VP) 



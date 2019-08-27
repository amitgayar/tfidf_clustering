import pickle 
import os
from os.path import isfile, isdir, join, isdir, dirname
import math
import pandas as pd

def word_count(doc):
    doc_set_all = []
    for docc in doc:
        doc_set = sorted(set().union(docc))
        doc_dict = dict.fromkeys(doc_set, 0)
        for word in docc:
            doc_dict[word] += 1 
        doc_set_all.append(doc_dict.copy())
    return doc_set_all

# print ("wordSet  :   "," ".join(sorted(wordSet)))

def computeTF(doc_set_all,doc):
    tfidf_all = []
    for i in range(len(doc)):
        tfidf = {}
        doc_count = len(doc[i])
        for word, count in doc_set_all[i].items():
            tfidf[word] = round((count+1)/doc_count,4)
    #     print(str(tfDict),'\n'
        tfidf_all.append(tfidf.copy())
    return tfidf_all


def computeIDF(doc_set_all,wordSet):
#     import math
    idfDict = dict.fromkeys(wordSet, 0)
    N = len(doc_set_all)
    for word in wordSet:
        for i in range(N):
            if word in doc_set_all[i].keys():
                idfDict[word] += 1
    for word, val in idfDict.items():
        idfDict[word] = math.log10(N / val)
                        
    return idfDict        




def computeTFIDF(tfs, idfs, threshold=0.0001):
    tfidfs = []
    new_wordSet = []
    for t in tfs:
        tfidf = {}
        for word, val in t.items():
            ti = round(val*idfs[word],4)
            if ti > threshold:
                tfidf[word] = ti #------rounded for error handeling of data(float64)
                new_wordSet.append(word)
        tfidfs.append(tfidf.copy())
#     print(str(tfidf),'\n')
#     print(str(new_wordset),'\n')
    return tfidfs, new_wordSet


def computeTFIDF_matrix(wordSet, tfidf, l_doc):
    tfidf_wordSet = [dict.fromkeys(wordSet, 0)]*l_doc
    i=0 
    tfidf_matrix = [] 
    for wrdF in tfidf_wordSet:
        tfidf_matrix.append(dict(wrdF, **tfidf[i])) 
        i += 1
    return tfidf_matrix
    
    
def run_TFIDF(keywords, all_doc_list=None, filesave=True):
    
    if not all_doc_list:
        file = join(dirname(__file__),'data/{}/spacy_tf.pkl'.format(keywords))
        if not isfile(file):
            print('\nFILE DOES NOT EXIST\nGO TO THE PREVIOUS WORKFLOW STEPS\n')
            return None
        all_doc_list = pickle.load(open(file, 'rb'))
    if 'tfidf' in all_doc_list[0]:
        print('\nTFIDF ALREADY CALCULATED\n')
        return all_doc_list
    print(all_doc_list[0].keys())
    doc = [v['spacy_cleaned_article'][0] for v in all_doc_list]
    wordSet = sorted(set().union(*doc))
    
    doc_set_all = word_count(doc)
    tfs = computeTF(doc_set_all, doc)
    idfs = computeIDF(doc_set_all, wordSet)
    tfidf, new_wordSet = computeTFIDF(tfs, idfs)
    
    wordSet = sorted(set().union(new_wordSet))
    tfidf_matrix = computeTFIDF_matrix(wordSet, tfidf, len(doc))
    for i in range(len(tfidf_matrix)):
        all_doc_list[i]['tfidf'] = tfidf_matrix[i]
    
    if filesave :
        file = join(dirname(__file__),'data/{}/spacy_tf.pkl'.format(keywords))
        pickle.dump(all_doc_list, open(file, 'wb'))
        file = join(dirname(__file__),'data/{}/tfidf.csv'.format(keywords))
        df = pd.DataFrame(all_doc_list)
        df.to_csv(file)
        print('\n FILE SAVED FOR TFIDF\n')
    
    return all_doc_list



if __name__ == "__main__":
    keywords = input("Enter the keywords :  ")
    all_doc_list = run_TFIDF(keywords)
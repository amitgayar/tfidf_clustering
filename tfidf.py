import pickle 
import os
from os.path import isfile, isdir, join, isdir, dirname
import math
import pandas as pd
import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)-8s [%(filename)s:%(lineno)d] : %(message)s')

def word_count(doc):
    if isinstance(doc, str):
        doc = [doc]
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
        for word, count in doc_set_all[i].items():
            tfidf[word] = round((count+1)/len(doc[i]),4)
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
    
    
def run_TFIDF(keywords, level='articles', no_of_doc=None, all_doc_list=None, compute_again=False, filesave=True):
    
    if not all_doc_list:
        file = join(dirname(__file__),'data/{}/spacy_tf.pkl'.format(keywords))
        if not isfile(file):
            logging.info('FILE DOES NOT EXIST')
            if not compute_again:
                return None
        all_doc_list = pickle.load(open(file, 'rb'))
    if 'tfidf' in all_doc_list[0]:
        logging.info('TFIDF ALREADY CALCULATED')
        if not compute_again:
            file = join(dirname(__file__),'data/{}/tfidf.csv'.format(keywords))
            if not isfile(file):
                logging.info("tfidf_matrix csv file has not been processed yet")
                return None
            tfidf_matrix =  pd.read_csv(file)
            return all_doc_list, tfidf_matrix
    logging.info('Keys of the Story Dictionary:{}\n'.format(all_doc_list[0].keys()))

    if no_of_doc:
        all_doc_list = all_doc_list[:no_of_doc]
        logging.info("[{}] articles in the pipeline for processing".format(no_of_doc))
    else:
        logging.info("[ALL] {} in the pipeline for processing".format(level))
    if level in ['articles' , 'article']:
        logging.info("Level == {}".format(level))
        doc = [v['spacy_cleaned_article'] for v in all_doc_list]
    else:
        logging.info("Level == {}".format(level))
        doc=[]
        for v in all_doc_list:
            doc += [i for i in v['spacy_cleaned_para']]
        logging.info("Number of paragraphs in first {} articles : {}".format(no_of_doc, len(doc)))
    
    wordSet = sorted(set().union(*doc))
    
    doc_set_all = word_count(doc)
    tfs = computeTF(doc_set_all, doc)
    idfs = computeIDF(doc_set_all, wordSet)
    tfidf, new_wordSet = computeTFIDF(tfs, idfs)
    
    wordSet = sorted(set().union(new_wordSet))
    tfidf_matrix = computeTFIDF_matrix(wordSet, tfidf, len(doc))
    # for i in range(len(tfidf_matrix)):
    #     all_doc_list[i]['tfidf'] = tfidf_matrix[i]
    df = pd.DataFrame(tfidf_matrix)
    if filesave:
        file = join(dirname(__file__),'data/{}/spacy_tf.pkl'.format(keywords))
        pickle.dump(all_doc_list, open(file, 'wb'))
        file = join(dirname(__file__),'data/{}/tfidf.csv'.format(keywords))
        
        df.to_csv(file)
        logging.debug(' FILE SAVED FOR TFIDF\n')

    return all_doc_list, df



if __name__ == "__main__":
    keywords = input("Enter the keywords :  ")
    all_doc_list = run_TFIDF(keywords)
import pickle  
import os 
from os import listdir
from os.path import isfile, join, isdir
import spacy
nlp = spacy.load('en_core_web_sm')
# HERE SPACY.LOAD CAN BE MEDIUM AS WELL AS LARGE LIKE SHOWN BELOW:
# nlp = spacy.load('en_core_web_md')
# nlp = spacy.load('en_core_web_lg')
import math
import sys

import logging
logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d:%H:%M:%S', format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s')


def spacy_cleansing(doc):
    # Example : 
    # for token in doc:
    #     logging.info(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
    #             token.shape_, token.is_alpha, token.is_stop)
    doc = nlp(doc)
    lemmatized = []
    rejected = []
    for token in doc:
        # if token.is_ascii:
        #     logging.info(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
        #     token.shape_, token.is_oov)
        con = token.is_bracket or token.is_stop or token.is_quote or token.is_punct or not token.is_ascii
        if not con and token.pos_ not in ['SYM','PART','X','NUM','VERB','SPACE','-']:
            lemmatized.append(token.lemma_)
        else:
            rejected.append(token.lemma_)
    logging.info("Accepted Tokens: {}\n".format(str(sorted(set().union(lemmatized)))))
    logging.info("Rejected Tokens: {}\n".format(str(sorted(set().union(rejected)))))
    return (lemmatized, rejected)


def art_to_para(article,threshold=200):
    #     For fragmentation of article text into paragraphs of word-count >= threshold
    #         Parameters :
    #         -------------
    #         article : str
    #         threshold : int, optional, default 50
    para_list = article.split('\n\n')
    if len(para_list) == 1 and len(para_list[0].split()) > 2*threshold :
        logging.info("Article with single paragraph encountered: {}".format(para_list[0][:50]))
        temp = para_list[0].split('. ')
        para_list = [". ".join(temp[:math.floor(len(temp)/2)]), ". ".join(temp[math.floor(len(temp)/2):])]
    l = len(para_list)
    logging.info("Total number of paragraphs:{}".format(l))
    def para_thresholding(i=0, clustered_para=[]):
        temp = para_list[i]
        # logging.info("paragraph number:{}".format(i))
        while len(temp.split(" ")) < threshold and i < l - 1:
            temp = temp + " " + para_list[i+1]
            i+=1
        clustered_para.append(temp) 
        if i == l-1:
            cluster_len = len(clustered_para[-1])
            if cluster_len < threshold and cluster_len > 1:
                try:    
                    clustered_para[-2] = clustered_para[-2] + " " + clustered_para[-1]
                    del clustered_para[-1]
                except:
                    logging.info("Error in last paragraph")
                    pass
            return clustered_para
        else:
            return para_thresholding(i+1,clustered_para)
    return para_thresholding()

def run_spacy_cleansing(keywords, compute_again=False):
    mypath = join(os.path.dirname(__file__), 'data/{}/news/'.format(keywords))
    if not isdir(mypath):
        logging.info("Story [{}] News files don't exist yet")
        return None
    
    news_text_file = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]
    store_file = []

    if not news_text_file:
        logging.info("NO SUCH FILES FOUND")
        return None
    file = join(os.path.dirname(__file__), 'data/{}/spacy.pkl'.format(keywords))
    
    if isfile(file):
        if not compute_again:
            logging.info("ALREADY SPACY_CLEANED")
            temp = pickle.load(open(file, 'rb'))
            return temp
    logging.info("\nSPACY CLEANSING IN PROCESS....")
    for f in news_text_file:    
        store_dict = pickle.load(open(f, 'rb'))
        print()
        logging.info("Link of the Article:{}".format(store_dict['link']))
        store_dict['spacy_cleaned_article'] = spacy_cleansing(store_dict['content'])[0]
        store_dict['para_text'] = art_to_para(store_dict['content'])
        store_dict['spacy_cleaned_para'] = []
        for t in store_dict['para_text']:
            store_dict['spacy_cleaned_para'].append(spacy_cleansing(t)[0])        
        store_file.append(store_dict.copy())


    return store_file


if __name__ == '__main__':
    keywords = input("Enter the keywords (for example 'article 370 scrapped'):  ")  
    all_doc_list = run_spacy_cleansing(keywords)
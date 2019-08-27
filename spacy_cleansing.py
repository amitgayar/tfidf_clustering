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


def spacy_cleansing(doc):
    # Example : 
    # for token in doc:
    #     print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
    #             token.shape_, token.is_alpha, token.is_stop)
    doc = nlp(doc)
    lemmatized = []
    rejected = []
    for token in doc:
        # if token.is_ascii:
        #     print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
        #     token.shape_, token.is_oov)
        con = token.is_bracket or token.is_stop or token.is_quote or token.is_punct or not token.is_ascii
        if not con and token.pos_ not in ['SYM','PART','X','NUM','VERB','SPACE','-']:
            lemmatized.append(token.lemma_)
        else:
            rejected.append(token.lemma_)

    return (lemmatized, rejected)


def art_to_para(article,threshold=50):
    #     For fragmentation of article text into paragraphs of word-count >= threshold
    #         Parameters :
    #         -------------
    #         article : str
    #         threshold : int, optional, default 50
    para_list = article.split('\n\n')
    if len(para_list) == 1 and len(para_list[0]) > 4*threshold :
        temp = para_list[0].split('. ')
        para_list = [". ".join(temp[:math.floor(len(temp)/2)]), ". ".join(temp[math.floor(len(temp)/2):])]
    l = len(para_list)
    def para_thresholding(i=0, clustered_para=[]):
        temp = para_list[i]
        while len(temp.split(" ")) < threshold and i < l - 1:
            temp = temp + " " + para_list[i+1]
            i+=1
        clustered_para.append(temp) 
        if i == l-1:
            cluster_len = len(clustered_para[-1])
            if cluster_len < threshold and cluster_len > 1:
                clustered_para[-2] = clustered_para[-2] + " " + clustered_para[-1]
                del clustered_para[-1]
            return clustered_para
        else:
            return para_thresholding(i+1,clustered_para)
    return para_thresholding()

def run_spacy_cleansing(keywords, filesave=True):
    mypath = join(os.path.dirname(__file__), 'data/{}/news/'.format(keywords))
    if not isdir(mypath):
        print("\nNO SUCH FILES FOUND\nGO TO PREVIOUS FLOW STEPS\n ")
        return None
    
    news_text_file = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]
    store_file = []

    if not news_text_file:
        print("\nNO SUCH FILES FOUND\nGO TO PREVIOUS FLOW STEPS\n ")
        return None
    file = join(os.path.dirname(__file__), 'data/{}/spacy_tf.pkl'.format(keywords))
    
    if isfile(file):
        print("\nALREADY SPACY_CLEANED \n")
        temp = pickle.load(open(file, 'rb'))
        return temp
    print("\nSPACY CLEANSING IN PROCESS....")
    for f in news_text_file:    
        store_dict = pickle.load(open(f, 'rb'))
        store_dict['spacy_cleaned_article'] = spacy_cleansing(store_dict['content'])
        store_dict['para_text'] = art_to_para(store_dict['content'])
        store_dict['spacy_cleaned_para'] = []
        for t in store_dict['para_text']:
            store_dict['spacy_cleaned_para'].append(spacy_cleansing(t))        
        store_file.append(store_dict.copy())
        # print('link: {} processed '.format(news_text_file.index(f)))
        
        string = "\r{}{} {}%" 
        i = math.floor((news_text_file.index(f)+1)/len(news_text_file)*100)
        sys.stdout.write(string.format("#"*i, "."*(100-i), i))


    if filesave:    
        file = 'data/{}/spacy_tf.pkl'.format(keywords)
        pickle.dump(store_file,open(file,'wb'))
        print('\nFILE SAVED FOR SPACY_CLEANED')

    return store_file


if __name__ == '__main__':
    keywords = input("Enter the keywords :  ")  
    all_doc_list = run_spacy_cleansing(keywords)
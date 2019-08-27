from get_news_links import *



# keywords = 'mauritius route tax haven'
keywords = input("Enter keywords :\n")
get_news_links(keywords)


from extract_data import *
from spacy_cleansing import *
from tfidf import *

print('\n\nEXTRACTION OF DATA-----------------------------------------------------------------------------------------------------------\n')
extract_data(keywords)
print('\nSPACY -----------------------------------------------------------------------------------------------------------\n')
all_doc_list = run_spacy_cleansing(keywords)
print('\n\nTFIDF_MATRIX-----------------------------------------------------------------------------------------------------------')
all_doc_list = run_TFIDF(keywords, None)

print('\n\nWORKFLOW COMPLETED\n')
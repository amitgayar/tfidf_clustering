from __future__ import absolute_import
# from .celery import app
import time
# from celery import Celery
# from datetime import timedelta

# from extract_data import *
# from spacy_cleansing import *
# from tfidf import *


# Set Up Tor with HashedPassword = 'linux'
# get_news_links.py ....> start_year and end_year, continuation issue for queuing
# extract_data.py .... > Number_Threads = 8, 
# spacy_cleansing,py....> para, whole_article, filesave, apply collections.Counter
# tfidf.py.....>
# clustering.py

# keywords = input("Enter the keywords :  ")
# get_news_links(keywords)
# extract_data(keywords)
# all_doc_list = load_and_break(keywords)
# all_doc_list = run_TFIDF(keywords, all_doc_list)


# celery = Celery(__name__)
# celery.config_from_object(__name__)

# @celery.task
# def say_hello():
#     print('Hello, World!')

# CELERYBEAT_SCHEDULE = {
#     'every-second': {
#         'task': 'tf-idf.tasks',
#         'schedule': timedelta(seconds=5),
#     },
# }


# @app.task
# def longtime_add(x, y):
#     print('long time task begins')
#     # sleep 5 seconds
#     time.sleep(2)
#     print ('long time task finished')
#     return x + y


from .get_news_links import *
# from .extract_data import *

@app.task
def getgoo(keywords):
	get_news_links(keywords)
	return "success from getgoo_func"

# @app.task
# def extractgoo(keywords):
# 	extract_data(keywords)
# 	return "success from extractgoo_func"


# if __name__ == '__main__':
# keywords = 'arun jaitley demise'
keywords = 'sitharaman economic reforms'
# result = r.delay(group(getgoo.s('sitharaman economic reforms'), extractgoo.s('arun jaitley demise')))
result_link = getgoo.delay('sitharaman economic reforms')
# result_ex = extractgoo.delay('arun jaitley demise')
# while not result_link.ready():
# 	time.sleep(3)
# 	print('in a while!!')

while not result_link.ready():
	time.sleep(2)
	print('in a while', end=' ')
print('\ndone all')
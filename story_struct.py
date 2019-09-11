# celery, queue, task, generator_iter()
import pickle, pandas, os
import logging

from tfidf import *
from spacy_cleansing import *	
logging.basicConfig(level=logging.INFO, format='%(levelname)s [%(filename)s:%(lineno)d] : %(message)s')

# ['link', 'title', 'content', 'meta_description', 'meta-keywords', 'datetime', 'spacy_cleaned_article', 'para_text', 'spacy_cleaned_para', 'tfidf']
class Story_Struct(object):

	def __init__(self, keywords ):
		self.keywords = keywords
		self.dir = os.path.join(os.path.dirname(__file__),'data', keywords)
		logging.info("Story [{}] Object Created".format(self.keywords))
		
		if not os.path.isdir(self.dir):
			logging.info("But Story [{}] doesn't exist yet".format(self.keywords))
		

	def load(self, keyvalue = None):
		if not os.path.isdir(self.dir):
			logging.info("Story [{}] doesn't exist yet".format(self.keywords))
			return None
			
		file = os.path.join(self.dir, 'spacy_tf.pkl')
		data = pickle.load(open(file, 'rb')) if os.path.isfile(file) else None
		if keyvalue:
			data = [d[keyvalue] for d in data]
			logging.info("keyvalue {} loaded".format(keyvalue))
		return data
		

	def process(self, step, level='articles', no_of_doc=None, compute_again=False , filesave=False):
		if step =='spacy':
			_ = run_spacy_cleansing(self.keywords, compute_again=compute_again)

		if step == 'tfidf':
			data, tfidf_matrix = run_TFIDF(self.keywords, level=level, no_of_doc=no_of_doc,  all_doc_list=None, compute_again=compute_again, filesave=filesave)
			return data, tfidf_matrix
		else:
			_ = run_spacy_cleansing(self.keywords, compute_again=compute_again)
			_ = run_TFIDF(self.keywords, all_doc_list=None, compute_again=compute_again)
		logging.info("Process Done")


	def save(self, data, filetype ):
		if filetype == '.pkl' or 'spacy':
			filename = 'spacy_tf.pkl'
			file = os.path.join(self.dir, filename)
			pickle.dump(data, open(file, 'wb'))
		elif filetype == 'tfidf':
			filename = 'tfidf.pkl'
			file = os.path.join(self.dir, filename)
			pickle.dump(data, open(file, 'wb'))
		else:
			filename = 'cluster.csv'
			df = pandas.DataFrame(data)
			file = os.path.join(self.dir, filename)
			df.to_csv(file)

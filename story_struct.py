# celery, queue, task, generator_iter()
import pickle, pandas, os


# ['link', 'title', 'content', 'meta_description', 'meta-keywords', 'datetime', 'spacy_cleaned_article', 'para_text', 'spacy_cleaned_para', 'tfidf']
class Story_Struct(object):

	def __init__(self, keywords ):
		self.keywords = keywords
		self.dir = os.path.join(os.path.dirname(__file__),'data', keywords)

	def load(self, keyvalue = None):
		# if not os.path.isdir(self.dir):
		# 	return None

		# file = os.path.join(self.dir, 'spacy_tf.pkl')		
		# if not os.path.isfile(file):
		# 	return None
		data = pickle.load(open(file, 'rb'))	
		if keyvalue:
			data = [d[keyvalue] for d in data]
		return data

	def save(self, data, **kwargs):
		file = os.path.join(self.dir, 'spacy_tf.pkl')
		pickle.dump(data, open(file, 'wb'))


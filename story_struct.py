# celery, queue, task, generator_iter()
import pickle, pandas, os

class Story_Struct(object):

	def __init__(self, keywords ):
		self.keywords = keywords
		self.dir = os.path.join(os.getcwd(),'data', keywords)
		self.story_file = keywords + '.pkl'

	def load(self, keyvalue = None):
		file = os.path.join(self.dir, 'tfidf.pkl')		
		if not keyvalue:
			data = pickle.load(open(file, 'rb'))
		else:
			data = pickel.load(open(file, 'rb'))
			data = data[keyvalue]
		return data

	def save(self, data, **kwargs):
		file = os.path.join(self.dir, self.story_file)
		pickle.dump(data, open(file, 'wb'))


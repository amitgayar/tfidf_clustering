# celery, queue, task, generator_iter()
import pickle, pandas, os
import logging
import sys
from time import time
import numpy as np

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
			
		file = os.path.join(self.dir, 'spacy.pkl')
		data = pickle.load(open(file, 'rb')) if os.path.isfile(file) else None
		if keyvalue:
			data = [d[keyvalue] for d in data]
			logging.info("keyvalue {} loaded".format(keyvalue))
		return data
		

	def process(self, step, level='articles', no_of_doc=None, compute_again=False , filesave=False):
		
		if step =='spacy':
			data = run_spacy_cleansing(self.keywords, compute_again=compute_again)
			if filesave:
				self.save(data, 'spacy')
			return data

		if step == 'tfidf':
			tfidf = run_TFIDF(self.keywords, level=level, no_of_doc=no_of_doc,  all_doc_list=None, compute_again=compute_again)
			if filesave:
				self.save(tfidf, 'tfidf')
			return tfidf
		
		if step == 'cluster':
			data = self.cluster(dataset = None, n_clusters = 5,
								n_init = 20,
								init = 'k-means++',
								max_iter = 300,
								tol = .0001,
								copy_x = True,
								n_jobs = -1,
								random_state = 4200,
								precompute_distances = False,
								verbose = False)
			if filesave:
				self.save(data,'cluster')
		
		logging.info("Process Completed")

	def process_all(self):
		_ = self.process('spacy', level='articles', no_of_doc=None, compute_again=True , filesave=True)
		_ = self.process('tfidf', level='articles', no_of_doc=None, compute_again=True , filesave=True)
		_ = self.process('cluster', compute_again=True , filesave=True)
		logging.info('All Processes [spacy, tfidf, clustering] Completed for the story : "{}"'.format(self.keywords ))

	def save(self, data, filetype ):
		if filetype == 'spacy':
			filename = 'spacy.pkl'
			file = os.path.join(self.dir, filename)
			pickle.dump(data, open(file, 'wb'))
		elif filetype == 'tfidf':
			filename = 'tfidf.pkl'
			file = os.path.join(self.dir, filename)
			pickle.dump(data, open(file, 'wb'))
		# elif filetype == 'tfidf_matrix':
		# 	filename = 'tfidf.csv'
		# 	file = os.path.join(self.dir, filename)
		# 	df = pandas.DataFrame(data)
		# 	df.to_csv(file)
		else:
			filename = 'cluster.csv'
			df = pandas.DataFrame(data)
			file = os.path.join(self.dir, filename)
			df.to_csv(file)


	def cluster(self, dataset = None, n_clusters = 5,
				n_init = 20,
				init = 'k-means++',
				max_iter = 300,
				tol = .0001,
				copy_x = True,
				n_jobs = -1,
				random_state = 4200,
				precompute_distances = False,
				verbose = False):
		'''
				dataset must be a list of strings.
		'''

		from sklearn.datasets import fetch_20newsgroups
		from sklearn.decomposition import TruncatedSVD
		from sklearn.feature_extraction.text import TfidfVectorizer
		from sklearn.feature_extraction.text import HashingVectorizer
		from sklearn.feature_extraction.text import TfidfTransformer
		from sklearn.pipeline import make_pipeline
		from sklearn.preprocessing import Normalizer
		from sklearn import metrics
		from sklearn.cluster import KMeans, MiniBatchKMeans

	
		if not dataset:
			para_text = self.load('spacy_cleaned_para')
			paras = []

			for para in para_text:
			  paras += para
			
			dataset = [(' ').join(i) for i in paras]
		

		dataframe = pandas.DataFrame(dataset)
		t0 = time()
		vectorizer = TfidfVectorizer(max_df=0.5, max_features=10000,
		                             min_df=2, stop_words='english',
		                             use_idf=True)
		X = vectorizer.fit_transform(dataset)
		print("Vectorizer done in %fs" % (time() - t0))
		print("n_samples: %d, n_features: %d" % X.shape)


		km = KMeans(n_clusters=n_clusters, init=init, max_iter=max_iter,
					n_init=n_init, verbose=verbose, tol=tol, precompute_distances=precompute_distances,
					random_state=random_state, copy_x=copy_x, n_jobs=n_jobs
		            )

		# Of all the KMeans arguments, n_init=10 (or higher) and random_state = 4200 (or higher) shows the same  results  for our same dataset

		print("Clustering sparse data with %s" % km)
		t0 = time()
		km.fit(X)
		print("done in %0.3fs" % (time() - t0))
		print("Top terms per cluster:")
		order_centroids = km.cluster_centers_.argsort()[:, ::-1]
		terms = vectorizer.get_feature_names()
		for i in range(n_clusters):
		    print("Cluster %d:" % i, end='')
		    for ind in order_centroids[i, :50]:
		        print(' %s' % terms[ind], end='')
		    print('\n')
		km.fit_predict(X)
		cluster_list = km.fit_predict(X).tolist()
		i = 0
		cluster_tfidf = []
		for i in range(n_clusters):
		    cluster_tfidf.append([terms[ind] for ind in order_centroids[i, :]])
		i ,clust_result,temp = 0, [], {}
		for v in dataset:
		    temp['cluster'] = cluster_list[i]
		    temp['sorted_tfidf'] = cluster_tfidf[cluster_list[i]]
		    temp['content'] = v
		    i+=1
		    clust_result.append(temp.copy())

		return clust_result
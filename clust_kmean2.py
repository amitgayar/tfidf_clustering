from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn import metrics

from sklearn.cluster import KMeans, MiniBatchKMeans
import sys
from time import time
import pandas as pd
from pandas import DataFrame
import numpy as np
import os

#   Data                                            (((((((())))))))
import pickle
from story_struct import Story_Struct

keywords = input('Enter keywords for the Story or simply Enter for default story "article 370 scrapped":\n')
n_clusters = int(input('Enter number of clusters:\n'))
if not keywords:
  keywords = 'article 370 scrapped'
story = Story_Struct(keywords)
all_doc_list = story.load()
dataset = story.load('content')
dataframe = DataFrame(dataset)




t0 = time()
vectorizer = TfidfVectorizer(max_df=0.5, max_features=10000,
                                 min_df=2, stop_words='english',
                                 use_idf=True)
X = vectorizer.fit_transform(dataset)
print("Vectorizer done in %fs" % (time() - t0))
print("n_samples: %d, n_features: %d" % X.shape)



# ------------------------------------------------------First Clustering
n_clusters = n_clusters # number of clusters
n_init = 20
init = 'k-means++'
max_iter = 300
tol = .0001
copy_x = True
n_jobs = -1
random_state = 4200
precompute_distances = False
verbose = False
km = KMeans(n_clusters=n_clusters, init=init, max_iter=max_iter, n_init=n_init,
                verbose=verbose, tol=tol, 
                precompute_distances=precompute_distances, random_state=random_state, copy_x=copy_x, n_jobs=n_jobs
               )

# -------------------------------------------------------Second Clustering
# km = KMeans(n_clusters=n_clusters, max_iter=300, n_init=10,
#                tol=0.0001,precompute_distances=True, random_state=4200,
#                copy_x=True, n_jobs=-1)

# ------------------------------------------------------Third Clustering
# km = KMeans(n_clusters=n_clusters, max_iter=300, n_init=10,
#              tol=0.0001,precompute_distances=False, random_state=4200, 
#             copy_x=True, n_jobs=-1
#             )


# ------------------------------------------------------Fourth Clustering
# km = KMeans(n_clusters=n_clusters, max_iter=300, n_init=10,
#                tol=0.0001,precompute_distances=False, random_state=4200,
#                 copy_x=True, n_jobs=-1
#                 )


# Of all the KMeans arguments, n_init=10 (or higher) and random_state = 4200 (or higher) shows the same  results  for our same dataset

print("Clustering sparse data with %s" % km)
t0 = time()
km.fit(X)
print("done in %0.3fs" % (time() - t0))
print()

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

story.save(clust_result,'.csv')
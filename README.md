# tfidf + clustering
tfidf + clustering

### Installation guide
	1. make virtual env in "tfidf"(the project directory) in python3 
		cd tfidf
		virtualenv -p python3 venv_tfidf
	2. install requirements for the package and make sure pip is of python3 by "pip -V" command
		pip install --upgrade pip
		pip install -r requirements.txt
		python -m spacy download en-core-web-md
		
### Individual scripts
	- "get_news_links.py" loads the various links based on input keywords.
	- "extract.py" loads the various articles based on links downloaded by get_news_links.py
	   script in the "data/<keywords>" directory does the clustering of the text extracted while
	   accepting tuning parameters like min_tfidf value, para-segmentation.
	- "spacy_cleansing.py" does the paragraph segmentation of articles and cleans the redundant 
	    data using "spacy" library. "nltk" library results weren't so effective.
	- "tfidf.py" constructs the tfidf matrix for clustering and appends the results to the same 
	    file created by spacy_cleansing.py

### worflow.py 
	- It just combines the all scripts to work in one go.

### Clustering
	??

# tfidf + clustering


### Prerequisites: 
	Set Up Tor with HashedPassword = 'linux' (your choice)
### Installation guide
	1. make virtual env in "tfidf"(the project directory) in python3 
		cd tfidf
		virtualenv -p python3 venv_tfidf
	2. install requirements for the package and make sure pip is of python3 by "pip -V" command and
	   of latest version.
		pip install --upgrade pip
		pip install -r requirement.txt
		python -m spacy download en-core-web-md
		python -m spacy download en-core-web-sm (lightest)
		python -m spacy download en-core-web-lg (very heavy to load)
		
### Individual scripts
	- "get_news_links.py" loads the various links based on input keywords.
		(issues: start_year and end_year)
	- "extract.py" loads the various articles based on links downloaded by get_news_links.py
	   script in the "data/<keywords>" .
	   	(issues: number of threads for pooling = 1 but can be increased;
		  Need to check for links extracted in comparison to links got)
	- "spacy_cleansing.py" does the paragraph segmentation of articles and cleans the redundant 
	    data using "spacy" library. "nltk" library results weren't so effective.
	    	(issues: en-core-web-md, en-core-web-sm, en-core-web-lg)
	- "tfidf.py" constructs the tfidf matrix for clustering and appends the results to the same 
	    file created by spacy_cleansing.py

### worflow.py 
	- It just combines the all scripts to work in one go.

### Clustering
	??

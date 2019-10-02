# tfidf + clustering


### Prerequisites: 
	Set Up Tor with HashedPassword = 'linux' (your choice)
	Follow : https://gist.github.com/DusanMadar/8d11026b7ce0bce6a67f7dd87b999f6b
	
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
```
It employs the class Story_Struct to process the whole story. 
	Story_Struct class contains following methods:
			1. load(self, keyvalue = None)
			2. process(self, step, level='articles', no_of_doc=None, compute_again=False , filesave=False)
			3. process_all()
			4. save(self, data, filetype )
	parameters: 'no_of_doc' is number of articles to process at a time
				'compute_again' forces to recompute rather than to load from the processed files in directories.
				'filesave' saves or replaces the pre-processed files with the current computation.  
	Example:
			story = Story_Struct('article 370 scrapped')
			all_doc_list = story.process("spacy")
			tfidf = story.process("tfidf")
			cluster = story.process("cluster")
```
### Clustering
	clust_kmean2.py

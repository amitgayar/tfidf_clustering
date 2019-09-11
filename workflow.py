from get_news_links import *
keywords = input("Enter keywords :\n")
get_news_links(keywords)

from story_struct import Story_Struct
from extract_data import *

extract_data(keywords)

story.process(step='all', level='articles', no_of_doc=None, compute_again=True, filesave=True)

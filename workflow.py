from get_news_links import *
keywords = input("Enter keywords :\n")
get_news_links(keywords)


from extract_data import *
extract_data(keywords)

from story_struct import *
story = Story_Struct(keywords)
story.process(step='all', level='articles', no_of_doc=None, compute_again=True, filesave=True)

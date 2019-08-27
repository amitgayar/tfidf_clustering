import errno
import logging
import os
import pickle
import random
import re
import time
import requests
from torrequest import TorRequest
import sys

torpassword = 'linux'

from bs4 import BeautifulSoup
from fake_useragent import UserAgent


from constants import *

NUMBER_OF_CALLS_TO_GOOGLE_NEWS_ENDPOINT = 0

GOOGLE_NEWS_URL = 'https://www.google.co.jp/search?q={}&hl=eng&source=lnt&tbs=cdr%3A1%2Ccd_min%3A{}%2Ccd_max%3A{}&tbm=nws&start={}'

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# requests = TorRequest(proxy_port=9050, ctrl_port=9051, password=torpassword)




def forge_url(q, start, year_start, year_end):
    global NUMBER_OF_CALLS_TO_GOOGLE_NEWS_ENDPOINT
    NUMBER_OF_CALLS_TO_GOOGLE_NEWS_ENDPOINT += 1
    return GOOGLE_NEWS_URL.format(q.replace(' ', '+'), str(year_start), str(year_end), start)


def extract_links(content):
    soup = BeautifulSoup(content, 'html.parser')  # _sQb top _vQb _mnc
    links_list = [(v.attrs['href'], "".join([str(x) for x in v.contents]) ) \
	for v in soup.find_all('a', {'class': ['l lLrAF', 'RTNUJf']})]
    dates_list = [v.text for v in soup.find_all('span', {'class': ['f nsa fwzPFf', 'nsa fwzPFf f']})]
    output = []
    # logging.debug('Link List : {}'.format(str(links_list)))
    # logging.debug('Date List : {}'.format(str(dates_list)))
    for (link, date) in zip(links_list, dates_list):
        output.append((link[0], link[1], date))
    return output

def google_news_run(keyword, limit=10, year_start=2010, year_end=2019, debug=True, sleep_time_every_ten_articles=0):
    num_articles_index = 0
    ua = UserAgent()
    result = []
    while num_articles_index < limit:
        url = forge_url(keyword, num_articles_index, year_start, year_end)
        if debug:
            logging.debug('For Google -> {}'.format(url))
            logging.debug('Total number of calls to Google = {}'.format(NUMBER_OF_CALLS_TO_GOOGLE_NEWS_ENDPOINT))
        headers = {'User-Agent': ua.chrome}
        try:
            response = requests.get(url, headers=headers, timeout=20)
            links = extract_links(response.content)
            logging.debug('Extract Links : {}'.format(str(links)))

            nb_links = len(links)
            if nb_links == 0 and num_articles_index == 0:
                """raise Exception(
                    'No results fetched. Either the keyword is wrong '
                    'or you have been banned from Google. Retry tomorrow '
                    'or change of IP Address.')"""
                logging.debug('No results')
                requests.reset_identity()
                logging.debug('IP Changed. Retrying ....')
                response = requests.get(url, headers=headers, timeout=20)
                links = extract_links(response.content)
                logging.debug('{}'.format(links))
                nb_links = len(links)
                if nb_links == 0 and num_articles_index == 0:
                    logging.debug('No Links')

            if nb_links == 0:
                print('No more news to read for keyword {}.\nNOW...... Extraction Of Data From Each Link.\n\n\n'.format(keyword))
                break

            for i in range(nb_links):
                cur_link = links[i]
                # logging.debug('Links : {}'.format(str(cur_link)))
                logging.debug('TITLE = {},\nURL = {},\nDATE = {}\n'.format(cur_link[1], cur_link[0], cur_link[2]))
            result.extend(links)
        except:
            print('SYS.EXC_INFO :: {}-----------------------------------------------------------------------\n\n'.format(sys.exc_info()))
            logging.debug('Google news TimeOut. Maybe the connection is too slow. Skipping.')
            pass
        num_articles_index += 10
        if debug and sleep_time_every_ten_articles != 0:
            logging.debug('Program is going to sleep for {} seconds.'.format(sleep_time_every_ten_articles))
            time.sleep(sleep_time_every_ten_articles)
    return result

def mkdir_p(path):
    try:
        path = os.path.join(os.path.dirname(__file__),path)
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise





def google_news_links(keyword, year_start=2017, year_end=2019, limit=data.ARTICLE_COUNT_LIMIT_PER_KEYWORD):

    tmp_link_folder = 'data/{}/links'.format(keyword)
    mkdir_p(tmp_link_folder)

    pickle_file = os.path.join(os.path.dirname(__file__),'{}/{}_{}_{}_links.pkl'.format(tmp_link_folder, keyword, year_start, year_end))
    if os.path.isfile(pickle_file):
        logging.debug('Google news links for keyword [{}] have been fetched already.'.format(keyword))
        links = pickle.load(open(pickle_file, 'rb'))
        logging.debug('Found {} links.'.format(len(links)))
    else:
        links = google_news_run(keyword=keyword,
                                limit=limit,
                                year_start=year_start,
                                year_end=year_end,
                                debug=True,
                                sleep_time_every_ten_articles=data.SLEEP_TIME_EVERY_TEN_ARTICLES_IN_SECONDS)
        pickle.dump(links, open(pickle_file, 'wb'))

def run(keyword):
        logging.debug('KEYWORD = {}'.format(keyword))
        google_news_links(keyword)


def get_news_links(keywords):
    # fpath = os.path.join(os.path.dirname(__file__), 'data/{}/links/'.format(keywords))
    # if os.path.isdir(fpath):
    #     if os.listdir(fpath):
    #         print('\nALREADY FETCHED LINKS\n')
    #     return None
    while True:
        with TorRequest(proxy_port=9050, ctrl_port=9051, password=torpassword) as requests:
            requests.reset_identity()
            keyword = keywords
        try:
            run(keyword)
            # keyword = input("\nenter again another set of keywords to get links:\n")
            # if not keyword:
            break # POINT FOR CONTINUATION/BREAK; NEED TO BE HANDELED AT THE TIME OF QUEUING....
        except:
            print(sys.exc_info())
            print('EXCEPTION CAUGHT in __MAIN__')
            print('NEED TO CHANGE THE IP !')
            requests.reset_identity()    


        

if __name__ == '__main__':
    keywords = input("Enter searching keywords for news links:\n")
    get_news_links(keywords)
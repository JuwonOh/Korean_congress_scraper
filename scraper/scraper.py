import json
import time
import requests
import re

from dateutil.parser import parse
from .utils import get_soup
from .parser import parse_legislate

search_url = 'http://watch.peoplepower21.org/index.php?mid=Euian&show=&page={}&title={}&rec_num=1000&lname={}&sangim={}&bill_result={}'
request_url = 'http://watch.peoplepower21.org/opages/Lawinfo/_vote_table.php'
url_base = 'http://watch.peoplepower21.org/?mid=LawInfo&bill_no={}'


def yield_law(bill_result, max_page =10, end_date = '2018-12-01', begin_date= '2017-12-01', title = '', lname = '', sangim ='', sleep=1.0):
    """
    Artuments
    ---------
    law_status : str
        eg. 2018-01-01
    max_num : int
        Maximum number of news to be scraped
    sleep : float
        Sleep time. Default 1.0 sec

    It yields
    ---------
    news : json object
    """

    # prepare parameters

    d_begin = parse(begin_date)
    d_end = parse(end_date)
    end_page = 30
    n_news = 0
    outdate = False

    for page in range(1, max_page+1):

        # check number of scraped news
        if outdate:
            break

        links_all =[]
        url = search_url.format(page, title, lname, sangim, bill_result)
        soup = get_soup(url)
        sub_links = soup.find_all('tr')[1:]
        links = [i.find('a')['href'] for i in sub_links]
        links_all = ['http://watch.peoplepower21.org/?mid=LawInfo&'+url[29:] for url in links]

        dates = soup.find_all('tr')[1:]
        day = [d.find('td').text for d in dates]

        for i, url in enumerate(links_all):
            d_news = parse(day[i])
            if d_end < d_news:
                print('ignore scrapping. {} legistlation was scrapped'.format(d_news))
                print('The newest legistlation has been created after {}'.format(end_date))
                continue
            else:
                new_json = parse_legislate(url)
                new_json['date'] = day[i]
                # check date
                if new_json is not None:

                    if d_begin > d_news:
                        outdate = True
                        print('Stop scrapping. {} / {} legistlation was scrapped'.format(n_news, max_page*100))
                        print('The oldest legistlation has been created after {}'.format(begin_date))
                        break
                    else:
                        yield new_json

                else:
                    continue







def gather_url(bill_result, max_page =10,end_date = '2019-12-01',begin_date= '2016-04-01', title = '', lname = '', sangim ='', sleep=1.0):
    """
    Artuments
    ---------
    law_status : str
        eg. 2018-01-01
    max_num : int
        Maximum number of news to be scraped
    sleep : float
        Sleep time. Default 1.0 sec

    It yields
    ---------
    news : json object
    """

    # prepare parameters

    d_begin = parse(begin_date)
    d_end = parse(end_date)
    end_page = 30
    n_news = 0
    outdate = False

    for page in range(0, max_page+1):

        # check number of scraped news
        if outdate:
            break

        links_all =[]
        url = search_url.format(page, title, lname, sangim, bill_result)
        soup = get_soup(url)
        sub_links = soup.find_all('tr')[1:]
        links = [i.find('a')['href'] for i in sub_links]
        links_all = ['http://watch.peoplepower21.org/?mid=LawInfo&'+url[29:] for url in links if is_matched(url)]
    return links_all

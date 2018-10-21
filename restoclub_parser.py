from lxml import html
import json
from common import request_utility
import logging
import threading
from models import restaurant

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR,
                    filename=u'log.txt')

THREAD_COUNT = 1
HOST = 'https://www.restoclub.ru'
restaurants_list = []


def get_page_count():
    url = "https://www.restoclub.ru/spb/search"
    params = {
        "types[]": ["34", "6", "3", "30", "10", "23", "38", "16", "2", "33", "5", "7", "20", "14", "11", "4", "24",
                    "15", "39", "1", "8", "17", "37", "9", "22", "13", "25"]}

    response = request_utility.do_request(url, params=params)
    tree = html.fromstring(response.text)
    pages  = tree.xpath('//a[@class="pagination__item _page"]/text()')
    return int(pages[-1])


def get_restaurants_links(page_count):
    url = "https://www.restoclub.ru/spb/search-filter"
    headers = {
        'connection': "keep-alive",
        'content-type': "application/json",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        'cache-control': "no-cache",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
                      "69.0.3497.100 Safari/537.36",
    }
    restaurants_links = []
    page = 1
    while page <= page_count:
        data = '{\"page\":' + str(page) + ',\"types\":' \
               '[34,6,3,30,10,23,38,16,2,33,5,7,20,14,11,4,24,15,39,1,8,17,37,9,22,13,25]}'

        response = request_utility.do_request(url, type_request='POST', data=data, headers=headers)
        parsed_string = json.loads(response.content.decode('utf-8'))
        html_page = parsed_string.get('html')
        tree = html.fromstring(html_page)
        restaurants_links.extend(tree.xpath('//li[@class="page-search__item"]//div[@class="search-place-card"]/@data-href'))
        restaurants_links.extend(tree.xpath('//li[@class="page-search__item _premium"]//div[@class="search-place-card _premium"]/@data-href'))
        restaurants_links.extend(tree.xpath('//li[@class="page-search__item _premium _platinum"]//div[@class="search-place-card _premium _platinum"]/@data-href'))
        page += 1
    return restaurants_links


def get_restaurant_attributes(links):
    chunked_links = chunk_it(links, THREAD_COUNT)
    threads = []

    for links in chunked_links:
        # Подготавливаем потоки, складываем их в массив
        threads.append(threading.Thread(target=get_restaurant_attr, args=(links,)))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
    return restaurants_list


def get_restaurant_attr(links):
    for link in links:
        url = HOST + link
        response = request_utility.do_request(url)
        response.encoding = 'utf-8'
        tree = html.fromstring(response.text)
        name = get_list_item(tree.xpath('//div[@class="place-title__header"]/text()'))
        rest_type = get_list_item(tree.xpath('//div[@class="place-title__type"]/text()'))
        adress = get_list_item(tree.xpath('//div[@class="info"]//div[@class="info__content"]/span/text()'))
        rc_rating = get_list_item(tree.xpath('//div[@class="place"]//div[@class="place-rating__value"]/div/div/text()'))
        restaurants_list.append(restaurant.Restaurant(name, adress, url, rc_rating, rest_type))


def chunk_it(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0
    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out


def get_list_item(list):
    try:
        return str(list[0])
    except IndexError:
        return '-'

# page_count = get_page_count()
links = get_restaurants_links(1)
get_restaurant_attributes(links)
pass
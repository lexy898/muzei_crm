import requests
from time import sleep
import logging

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR,
                    filename=u'log.txt')

TIME_STEP = 10
FINAL = 6


def do_request(url, **kwargs):
    type_request = kwargs.get('type_request', 'GET')
    params = kwargs.get('params', None)
    headers = kwargs.get('headers', None)
    data = kwargs.get('data', None)
    print('__________')
    print('***Request: ' + type_request + '  ' + url)
    for arg in kwargs:
        print('**' + arg + ': ' + str(kwargs.get(arg)))
    counter = 0
    response = None
    while counter < FINAL:
        try:
            if type_request == 'GET':
                response = requests.get(url, params=params, headers=headers)
            elif type_request == 'POST':
                response = requests.post(url, params=params, data=data, headers=headers)
                pass
            else:
                logging.error(u'' + 'Неверный тип запроса: ' + str(type_request))
            return response
        except (requests.exceptions.ConnectTimeout,
                requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectionError,
                requests.exceptions.HTTPError) as err:
            logging.error(u'' + str(err))
            counter += 1
            interval = counter * TIME_STEP
            print('!Ошибка при выполнении запроса ' + url + '. Запрос будет выполнен повторно через ' + str(
                interval) + 'сек.')
            sleep(interval)

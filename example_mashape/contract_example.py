#coding=utf-8
from _ssl import SSLError

import threading
from urllib2 import URLError
import unirest

from local import auth_code

class TestThreadAPI(threading.Thread):
    '''
    Класс для тестирования API. Принимает адрес формата:
    https://clearspending.p.mashape.com/api/v1/contracts/search/?pricerange=10000000-50000000&page={0}
    Добробнее о API, можно посмотреть в документации clearspending.ru

    Из контракта пытается получить ИНН и КПП заказчика. Если это возможно, происходит запрос контрактов.

    Для начало работы создайте файл local.py, он должен быть такого формата:
    ---
    auth_code = "ZZZZ88881111RRRRaaaaSSSSBBBBAAAA"
    ---
    Код из профиля на Mashape.com
    '''

    def __init__(self, url_address):
        '''
        Блок инициализации начального состояния

        Задаются начальные состояния словоря для кодов ответа,
        количества элементов в ответе,
        адрес по которому будет происходить обращение через Mashape
        '''
        threading.Thread.__init__(self)

        self.request_code = {'200': 0, 'other': 0}
        self.prepage = 50
        self.url_address = url_address

    def run(self):
        try:
            #  забирает данные по https протоколу, необходим ключ с Mashape
            contracts = unirest.get(self.url_address.format(1), headers={"X-Mashape-Authorization": auth_code})
            #  данные будут полученые в dict
            contracts_dict = contracts.body
            amount_page = contracts_dict['contracts']['total'] / self.prepage + 1

            for page in xrange(2, amount_page + 1 if amount_page % self.prepage else amount_page + 2):
                print '{0}, page: {1}/{2}, data: {3}'.format(self.name, page, amount_page, contracts_dict)
                try:
                    self.request_code['200'] += 1
                    for customer in contracts_dict['contracts']['data']:
                        #  вызывает функцию для получения get_customer_by_inn
                        #  передаёт в ф-цию inn / customer['customer']['inn'] и kpp / customer['customer']['kpp']
                        self._get_customer_by_inn(customer['customer']['inn'], customer['customer']['kpp'])
                except KeyError as e:
                    self.request_code['other'] += 1
                #  загрузка новых данных, используя format получаем новую страницу с сервера
                contracts = unirest.get(self.url_address.format(page), headers={"X-Mashape-Authorization": auth_code})
                contracts_dict = contracts.body

        #  блок обработки ошибок
        except ValueError as e:
            print e
            self.request_code['other'] += 1
        except (KeyError, TypeError):
            print '{0}, address: {1}, data: {2}'.format(self.name, self.url_address, contracts_dict)
            self.request_code['other'] += 1
        except (URLError, SSLError) as e:
            print "Name or service not known"
            self.request_code['other'] += 1

        print(self.request_code)

    def _get_customer_by_inn(self, customer_inn, customer_kpp):
        '''
        Блок для получения контракта по ИНН и КПП заказчика.

        Создаётся url и с помощью format вставляется inn и kpp, но обработка ответа не происходит.
        '''
        customer_by_inn_url = r'https://clearspending.p.mashape.com/api/v1/' \
                                r'contracts/search/?customerinn={0}&customerkpp={1}'
        contracts = unirest.get(customer_by_inn_url.format(customer_inn, customer_kpp), headers={"X-Mashape-Authorization": auth_code})
        contracts_dict = contracts.body
        self.request_code['200'] += 1
        print 'Customer: {0}, inn: {1}, kpp: {2}, data: {3}'.format(self.name, customer_inn, customer_kpp, contracts_dict)



if __name__ == '__main__':
    '''
    Забирает все адреса из address_list. Для каждого элемента в address_list создаётся отдельный поток
    '''
    address_list = [r'https://clearspending.p.mashape.com/api/v1/contracts/select/?customerinn=5017018140&page={0}',
                    r'https://clearspending.p.mashape.com/api/v1/contracts/search/?pricerange=100000-500000&page={0}',
                    r'https://clearspending.p.mashape.com/api/v1/contracts/search/?pricerange=500000-1000000&page={0}',
                    r'https://clearspending.p.mashape.com/api/v1/contracts/search/?pricerange=1000000-5000000&page={0}',
                    r'https://clearspending.p.mashape.com/api/v1/contracts/search/?pricerange=5000000-10000000&page={0}',
                    r'https://clearspending.p.mashape.com/api/v1/contracts/search/?pricerange=10000000-50000000&page={0}',
                    r'https://clearspending.p.mashape.com/api/v1/contracts/search/?pricerange=50000000-100000000&page={0}',
                    r'https://clearspending.p.mashape.com/api/v1/contracts/search/?pricerange=100000000-100000000000&page={0}',
                    ]
    for url in address_list:
        t = TestThreadAPI(url)
        t.start()

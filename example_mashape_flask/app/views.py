#coding: utf-8
import datetime as dt
from local import auth_code
from flask import json, render_template, jsonify
from app import flask_app
import unirest

@flask_app.route('/')
@flask_app.route('/bar/')
def bar():
    """
    Построение столбчатой диаграммы на основание данных в регионах
    """
    #total количество контрактов
    contracts_count_dict = {}
    for year in xrange(1, 4):
        contract_str ='https://clearspending.p.mashape.com/v1/contracts/select/?daterange=01.01.201{0}-31.12.201{0}'.format(year)
        contracts = unirest.get(contract_str, headers={"X-Mashape-Authorization": auth_code})
        contracts_json = contracts.body
        contracts_count_dict[u'201{0}'.format(year)] = contracts_json[u'contracts'][u'total']

    #сумма контрактов в регионах
    regions_str = 'https://clearspending.p.mashape.com/v1/regionspending/statistics/?regioncode=all'
    regions = unirest.get(regions_str, headers={"X-Mashape-Authorization": auth_code})
    regions_json = regions.body
    sum_region_dict = {}
    for region in regions_json[u'regionspending'][u'data']:
        try:
            sum_region_dict[region[u'year']] += region[u'contractsSum']
        except KeyError:
            sum_region_dict[region[u'year']] = region[u'contractsSum']

    #JSON
    data = {}
    cvs_list = []
    for year in ('2011', '2012', '2013'):
        data[year] = {'contrats': contracts_count_dict[year],
                      'budget': sum_region_dict[year]
                      }
        cvs_list.append('{0}, {1}, {2:f}'.format(year, contracts_count_dict[year], sum_region_dict[year]))

    return render_template('base_bar_chart.html', sum_region=sum_region_dict, contracts_count=contracts_count_dict,
                           json=json.dumps(data), cvs=cvs_list)

@flask_app.route('/dict/placing/', methods=['GET', 'POST'])
def placing_json():
    """
    Возврящает JSON для построение по нему разлычных таблиц и графиков

    Формат:
    { 'year' :
       {'plicing = '1' :
           {month : price},
           ...
       }
       {'plicing = '2' :
           {month : price},
           {month : price},
           {month : price},
           ...
       }
       ...
       {'plicing = '6' :
           {month : price},
           ...
       }
       {'price_year'}: int
    }
    """
    request_str = "https://clearspending.p.mashape.com/v1/contracts/select/?customerregion=05&daterange=01.01.2012-31.12.2012&returnfields=[price,signDate,foundation]&page={0}"
    contracts = unirest.get(request_str.format(1), headers={"X-Mashape-Authorization": auth_code})
    contracts_dict = contracts.body

    not_placing = 0
    price_dict = {}
    prepage = 50

    amount_page = contracts_dict['contracts']['total'] / prepage + 1
    print contracts_dict['contracts']['total']

    for page in xrange(2, amount_page + 1 if amount_page % prepage else amount_page + 2):
        for contract in contracts_dict['contracts']['data']:
            date = dt.datetime.strptime(contract['signDate'][:7], "%Y-%m")
            if not date.year in price_dict:
                price_dict[date.year] = {}

            #денег в месяц
            try:
                if not contract['foundation']['order']['placing'] in price_dict[date.year]:
                    price_dict[date.year][contract['foundation']['order']['placing']] = {}

                #сбор информации за месяц
                try:
                    price_dict[date.year][contract['foundation']['order']['placing']][date.month] += contract['price']
                except KeyError:
                    price_dict[date.year][contract['foundation']['order']['placing']][date.month] = contract['price']

                # сумма всех денег за год
                try:
                    price_dict[date.year]['price_year'] += contract['price']
                except KeyError:
                    price_dict[date.year]['price_year'] = contract['price']
            # контракты без метки
            except KeyError:
                not_placing += 1

        contracts = unirest.get(request_str.format(page), headers={"X-Mashape-Authorization": auth_code})
        contracts_dict = contracts.body
        print (page, amount_page)

    return jsonify(price_dict)


@flask_app.route('/placing/')
def placing():
    return render_template('base_bar_placing_chart.html')


@flask_app.route('/table/')
def table():
    return render_template('table.html')

#! /usr/bin/env python
# -*- coding: utf-8 -*-
import re


def get_stockId(stockInfo_list, company_short_name):
    for stockInfo in stockInfo_list:
        if stockInfo['name'] == company_short_name:
            stockId = stockInfo['stockId']

            return stockId


def hongKongExtractData(response, uselessData, last_value_digit):
    response_text = response.text
    response_text = response_text.replace(uselessData, '')
    response_text = response_text[1:last_value_digit]

    return response_text

def HKEXGetToken(res):
    pattern = re.compile(r'return "Base64-AES-Encrypted-Token"(.*?)";', re.S)
    text_list = pattern.findall(res)
    text = text_list[0]
    token = text.replace('\r', '').replace('\n', '').replace(';', '').replace(' ', '').replace('"', '').replace(
        'return', '')

    return token


def hongKongExtractDataTest(response_text, uselessData, last_value_digit):
    response_text = response_text.replace(uselessData, '')
    response_text = response_text[1:last_value_digit]

    return response_text


def hongKongExtractFnYear(text):
    res = filter(lambda ch:ch in '0123456789/', text)
    res = ''.join(list(res))
    return res

def getReleaseYear(release_date):
    res_list = release_date.split(' ')
    release_date = res_list[0]
    release_year = release_date.split('/')[-1]
    return release_year

def judgeFiscalYear(fiscal_year):
    '''
    根据业务需求对文件title中获取的进行判断fiscal year
    :param fiscal_year:
    :return: fiscal year
    '''
    fiscal_year_list = fiscal_year.split('/')
    if len(fiscal_year_list) == 2:
        fiscal_year1 = fiscal_year_list[0]
        fiscal_year2 = fiscal_year_list[1]
        if fiscal_year2 == '' or fiscal_year2 is None:
            fiscal_year = fiscal_year1
        elif len(fiscal_year2) == 2:
            fiscal_year = '20' + str(fiscal_year2)
        else:
            fiscal_year = fiscal_year2

    return fiscal_year

def disclosureTimeFormat(releaseTime):
    res_result = releaseTime.split(' ')
    time = res_result[1] + ':00'
    day, month, year = res_result[0].split('/')
    date = str(year) + '-' + month + '-' + day
    datetime = date + ' ' + time
    return datetime


if __name__ == '__main__':
    text = '15/03/2018 16:30'
    datetime = disclosureTimeFormat(text)
    print(datetime)





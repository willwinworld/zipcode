# -*- coding: utf-8 -*-
import requests
from pyquery import PyQuery as pq


# def get_third_class_info(url):
#     r = requests.get(url)
#     r.encoding = 'gbk'
#     d = pq(r.text)
#     res = []
#     code = d('.success h1').text()
#     import ipdb;ipdb.set_trace()
#     three_info = d('td[width="649"]').text().split('-')
#     province = three_info[0].split()[0]
#     city = three_info[0].split()[1]
#     district = three_info[1]
#     print district
#     address_nodes = d('td[bgcolor="#f9f9f9"] .lh22 tr').remove('td[colspan]')
#     for item in pq(address_nodes)('td'):
#         addr = pq(item).text()
#         res.append({'code': code, 'province': province, 'city': city, 'district': district, 'addr': addr})
#     return res
#
# a = get_third_class_info('http://www.yb21.cn/post/code/573199.html')

def get_third_class_info(url):
    r = requests.get(url)
    r.encoding = 'gbk'
    d = pq(r.text)
    res = []
    code = d('.success h1').text()
    three_info = d('td[width="649"]').text().split('-')
    address_nodes = d('td[bgcolor="#f9f9f9"] .lh22 tr').remove('td[colspan]')
    if len(three_info) == 3:
        province = three_info[0]
        city = three_info[1]
        district = three_info[2]
        for item in pq(address_nodes)('td'):
            addr = pq(item).text()
            addr.replace(u'邮编', '').replace(u'邮政编码', '')
    elif len(three_info) == 2:
        province = three_info[0].split()[0]
        city = three_info[0].split()[1]
        district = three_info[1]
        for item in pq(address_nodes)('td'):
            addr = pq(item).text()
    res.append({'code': code, 'province': province, 'city': city, 'district': district, 'addr': addr})
    return res


a = get_third_class_info('http://www.yb21.cn/post/code/573199.html')
print a
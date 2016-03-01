# -*- coding: utf-8 -*-


import requests
from pyquery import PyQuery as pq
from utils.redisq import RedisQueue
import time


# proxies = {
#     'http': 'http://182.90.13.46:80',  # 代理，反爬虫的方式之一
# }
REDIS_IP = '127.0.0.1'
REDIS_PASS = ''
url_queue = RedisQueue('url', host=REDIS_IP, db=1, password=REDIS_PASS)
res_queue = RedisQueue('result', host=REDIS_IP, db=1, password=REDIS_PASS)


def get_first_url(url):
    r = requests.get(url)
    r.encoding = 'gbk'
    d = pq(r.text)
    first_class_url = []
    first_class_nodes = d('.lh22 .citysearch ul a')
    for node in first_class_nodes:
        dollar = pq(node)
        url = dollar.attr('href')
        first_class_url.append('http://www.yb21.cn' + url)  # 不加前缀的话，读出的URL会不全，最终会报错
    return first_class_url


def get_second_url(url):
    r = requests.get(url)
    d = pq(r.text)
    second_class_url = []
    second_class_nodes = d('tbody tr[align] td strong a')
    for node in second_class_nodes:
        dollar = pq(node)
        url = dollar.attr('href')
        second_class_url.append('http://www.yb21.cn' + url)  # 同上
    return second_class_url


def get_third_class_info(url):
    r = requests.get(url)  # 代理
    r.encoding = 'gbk'  # 编码解决方式，scrapy这个项目不能用的原因，不了解它内部的编码方式，所以采用pyquery方式写
    d = pq(r.text)
    res = []
    code = d('.success h1').text()
    three_info = d('td[width="649"]').text().split('-')
    province = three_info[0]
    city = three_info[1]
    district = three_info[2]
    address_nodes = d('td[bgcolor="#f9f9f9"] .lh22 tr').remove('td[colspan]')
    for item in pq(address_nodes)('td'):  # 读地址时，让它们一行行显示，方便去加入
        addr = pq(item).text()
        addr.replace(u'邮编', '').replace(u'邮政编码', '')  # 去掉字符串末尾的无用字符
        res.append({'code': code, 'province': province, 'city': city, 'district': district, 'addr': addr})  # 一次性加入列表中
    return res


# def run():
    # urls = []
    # first_class_url = get_first_url('http://www.yb21.cn/post')
    # for url in first_class_url:
    #     print 'now crawl: %s' % url  # 打log，方便调试
    #     second_class_url = get_second_url(url)
    #     urls.extend(second_class_url)
    # print 'first class complete!'
    # with open('urls.json', 'w') as f:  # 打开文件, 67,68行的操作是在存文件
    #     f.write(json.dumps(urls))  # 写文件，参数必须是字符串，dumps是把url变成了一个字符串
    # print len(urls)
    #
    # with open('urls.json', 'r') as f:
    #     data = f.read()
    #     urls = json.loads(data)
    # for url in urls:
    #     url_queue.put(url)
    # print 'insert OK!'

    while not url_queue.empty():  # 当url队列不为空
        link = url_queue.get()    # 获得url
        print 'now crawl detail: %s' % link  # 打log
        try:
            res = get_third_class_info(link)  # 获得结果
            for item in res:
                res_queue.put(item)   # 放到res队列
        except Exception, err:
            url_queue.put(link)   # 如果出错，将url放到url队列中
            print err   # 打印错误
            time.sleep(15*60)  # 睡15分钟
            continue  # 继续上面的循环



# run()




# -*- coding: utf-8 -*-
import json

from utils.redisq import RedisQueue

REDIS_IP = '127.0.0.1'
REDIS_PASS = ''
backup_queue = RedisQueue('backup', host=REDIS_IP, db=1, password=REDIS_PASS)  # redis是取一个少一个，弄个backup以防万一
res_queue = RedisQueue('result', host=REDIS_IP, db=1, password=REDIS_PASS)


def get_data():
    data = []
    idx = 1
    while not res_queue.empty():  # 当它不为空时
        item = res_queue.get()  # 取出一个字典，之前存什么结构，取出来就是什么结构
        backup_queue.put(item)  # 放入备份中
        data.append(item)
        idx += 1

        if idx % 2000 == 0:  # 打log
            print idx

        if idx % 10000 == 0:
            print 'now save files: %s' % idx
            with open('data_%s.json' % (idx / 10000), 'w') as f:  # 打开文件, 5,6两行在存文件
                f.write(json.dumps(data))  # 写文件，参数必须是字符串，dumps是把url变成了一个字符串
            data = []
    print 'save!'
    with open('data_last.json', 'w') as f:  # 保存不能被10000整除的文件
        f.write(json.dumps(data))  # 写文件，参数必须是字符串，dumps是把url变成了一个字符串
    print 'complete!'


get_data()






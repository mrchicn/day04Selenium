#@Time  : 2019/4/3 15:50
#@Author: www.mrchi.cn
#@File  : Data2Mongo.py
# -*- coding: UTF-8 -*-
import pymongo
from Authorized import *

#创建链接

def in2mongo(data):
    Conn = pymongo.MongoClient(URL)
    db = Conn[DB]
    # print(data)
    try:#判断插入是否成功
        if db[TableNames].insert_one(data):
            print("\t\tData  Insert MongoDB Successful! ")
    except Exception:
        print("Operation Failed!")
        Conn.close()

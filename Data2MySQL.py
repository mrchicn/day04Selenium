#@Time  : 2019/4/2 21:58
#@Author: www.mrchi.cn
#@File  : Data2MySQL.py
# -*- coding: UTF-8 -*-
import pymysql
import json
db = pymysql.connect("172.20.5.134", "root", "admin", "Python_db", charset="utf8")
def Insert(dicts):
    # print(dicts)
    cursor = db.cursor()
    # time.sleep(10)
    image="\""+json.loads(dicts)['image']+"\","  #用json.loads(json对象)['对应Key']  取出的是Key对应的Value值
    bookAddress="\""+json.loads(dicts)['bookAddress']+"\"," #拼接的字符串
    price="\""+json.loads(dicts)['price']+"\","
    counts="\""+json.loads(dicts)['counts']+"\","
    title="\""+json.loads(dicts)['title']+"\","
    shopAddress="\""+json.loads(dicts)['shopAddress']+"\","
    location="\""+json.loads(dicts)['location']+"\""        #这里不需要在加逗号了
    #查询语句
    Template = "INSERT INTO TB_Books(book_Url,book_Address,book_Price,book_Count,book_Title,book_Shop_Address,shop_locate) VALUES ("
    sql_exect=Template+image+bookAddress+price+counts+title+shopAddress+location+");"
    #测试拼接SQL语句
    # print(sql_exect)
    try:
        cursor.execute(sql_exect)
        db.commit()  # 没有提交数据库没有数据
        print("\t\tData Insert Success   .......")
    except:
        db.rollback()
        cursor.close()
        db.close()


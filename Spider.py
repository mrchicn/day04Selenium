# @Time  : 2019/4/2 21:15
# @Author: www.mrchi.cn
# @File  : Spider.py
# -*- coding: UTF-8 -*-
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from pyquery import PyQuery as pd
import json

from Data2Mongo import in2mongo
from Data2MySQL import in2MySQL


browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
def search_context():
    try:
        browser.get("https://www.taobao.com")  #请求
        #until等待直到located                        这里注意是双括号
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#q')))   #找到输入文本框
        # 等待找到可点击的元素
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
        input.clear()   #清楚文本框内容
        # 将文本框内容赋值
        input.send_keys("Python")
        # 点击搜索按钮
        submit.click()
        # 找到页面数,返回的是属性，要得到值需要.text
        countPage =wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.total')))
        # 用正则匹配找到countPage.text的值
        totail=int(re.search('(\d+)', countPage.text).group(1))
        # print(type(totail))
        return totail
    except TimeoutException:
        return search_context()

def next_page(page_number):
    try:
        # presence_of_element_located  查找选择器中的元素是否存在
        input=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.form > input')))
        submit=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        input.clear()   #清楚文本框内容
        input.send_keys(page_number)    # 将文本框内容赋值
        time.sleep(2)  # 等待2秒
        submit.click() # 点击搜索按钮
        #   text_to_be_present_in_element  确定内容是不是选择器中的内容,后面跟一个字符串类型的值
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(page_number)))
        #获取书的信息
        get_products(page_number)
    except TimeoutException:
        #失败则从新调用
        next_page(page_number)

def get_products(page_number):
    print("第 %s 页 数据"%(page_number))
    #等待 presence_of_element_located   选中器 选中的   列表加载完成
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-itemlist .items .item')))
    html=browser.page_source  #获取网页源码
    # print(html)
    content=pd(html)  #用PyQuery解析网站  返回的item是一个可以find 用选择器查找的属性集合
    items = content('#mainsrp-itemlist .items .item ').items()   #根据选择器  遍历每个 页面的样式属性
    # print(type(items))
    for item in items:
        # 将需要的信息遍历出来
        product={
            'image':item.find('.pic .J_ItemPic').attr('data-src'),  #书的图片
            'bookAddress':item.find('.pic .pic-link').attr('href'), #书的地址
            # 'price':item.find('.price ').text()[2:],        #书的价格 Mysql 取掉前面那个美元符号
            'price': item.find('.price ').text(),
            'counts':item.find('.deal-cnt').text(),         #销售的数量
            'title':item.find('.pic .img').attr('alt'),     #书的标题
            'shopAddress':item.find('.shopname ').attr('href'),     #店铺地址
            'location':item.find('.location').text()        #店铺的位置
        }
        #写入MongoDB
        in2mongo(product)
        #json.dumps 序列化时对中文默认使用的ascii编码
        # 想输出真正的中文需要指定ensure_ascii=False：
        #字典转JSON对象(str)
        # jsondoc=json.dumps(product, ensure_ascii=False)
        # print(type(jsondoc))
        # 写入MySQL数据库
        # in2MySQL(jsondoc)


def init_process():
        count = search_context()
        for i in range(2, count + 1):
            next_page(i)

if __name__ == '__main__':
    init_process()

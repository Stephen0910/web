#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2017/9/1 11:48
# @Author   : zhangjian
# @Site     : 
# @File     : baidu_login.py
# @Purpose  :
# @Software : PyCharm Community Edition
# @Copyright:   (c) zhangjian 2017
# @Licence  :     <your licence>

from selenium import webdriver
import time


def baidu_login(account, password):
    """
    通过改变本地cookie个人登录百度，可以绕过验证码
    :return: 登录成功
    """
    # 获取一个本地会话session
    driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
    # 进入百度一次
    driver.get("https://www.baidu.com")
    # 添加Cookie，可以通过其他方式获得，每个人的value不一样，更换时间和机器也不一样
    driver.add_cookie({'name': 'BAIDUID', 'value': account})
    driver.add_cookie({'name': 'BDUSS', 'value': password})
    print driver.get_cookies()
    # 刷新页面
    # driver.refresh()
    driver.get("https://www.baidu.com")

    time.sleep(10)
    # 关闭浏览器
    driver.close()


if __name__ == '__main__':
    name = "715972C83B393C2D2417F1D317094AEF:FG=1"
    password = "ZTRmVycTl1MUY3TWM0MW95VHR2UFlxSmhPZjljd2ZEUDFheEtGQzJncU5PYzlaSUFBQUFBJCQAAAAAAAAAAAEAAADNxnMvu-" \
               "rN7LjoXwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAI2sp1mNrKdZYW"
    baidu_login(name, password)

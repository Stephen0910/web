#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2017/6/21 14:34
# @Author   : zhangjian
# @Site     : 
# @File     : scrap.py
# @Purpose  :
# @Software : PyCharm Community Edition
# @Copyright:   (c) zhangjian 2017
# @Licence  :     <your licence>

"""
基本写法，建议改为插入request，因为在构建请求时还需要加入好多内容，通过构建一个request，服务器响应请求得到应答，这样显得逻辑上清晰明确
本文为：通过urllib2模块建立网络连接，获取页面信息，分析数据，获得需要的数据并存储在本地excel，写入使用为xlsxwriter，不支持重新打开
待改进：支持多进程，没有收集完无法保存
"""

import xlsxwriter
import logging
from datetime import datetime

print datetime.now().strftime('%Y-%m-%d %H:%M:%S')

file_name = u"09platform.xlsx"

def OnlyNum(s):
    """
    只显示数字
    :param s:
    :return:
    """
    fomart = '0123456789'
    for c in s:
        if not c in fomart:
            s = s.replace(c,'');
    return s;

def prn_obj(obj):
    """
    获取对象所有属性
    :param obj:
    :return:
    """
    print '\n'.join(['%s:%s' % item for item in obj.__dict__.items()])

def score(roleid=53890):
    """
    根据roleid爬取09平台战绩信息
    :param roleid:角色roleid
    :return:
    """
    import urllib2, re
    # 取id
    request_name = urllib2.Request("http://users.09game.com:8011/?roleid=%s"%roleid)
    response_name = urllib2.urlopen(request_name, timeout=5)
    name1 = response_name.read()
    # print name1
    name2 = re.findall("roleid=.*?<", name1)
    name3 = re.findall(">.*?<", str(name2[0]))
    name4 = str(name3).replace("&#", "\\")
    name5 = name4.replace(";", "")
    name6 = name5.replace("x", "u")
    name7 = name6[3:-4]
    print "第一个name7：", name7
    if "\\" not in name7: #短id
        pass

    elif name7[-5] == "\\":
        strin1 = name7[-3:]
        print "strin1:", strin1
        name7 = name7[:-3]+"0"+strin1

    elif "\\" not in name7[-9:0]:
        pass

    elif name7[-7] == "\\":
        name7 = name7
    # elif name7[-6] != "\\":

    else:
        pass
    # print name7
    role_name = name7.decode("unicode-escape").encode("utf-8")
    print "账号ID：", role_name

    # 取战绩数据
    request = urllib2.Request("http://users.09game.com:8011/home/GetUserTotalInfo?roleid=%s"%roleid)
    response = urllib2.urlopen(request, timeout=5)
    t = response.read()
    # print t

    print ("roleid:%s"%roleid)
    # total_times_middle = re.findall("totalTimes\":.*?,", t)
    # totalTimes = OnlyNum(total_times_middle[1])
    # print totalTimes
    # 总场次爬取
    middle = re.findall("totalTimes\":.*?,", t)
    total_times = int(OnlyNum(middle[1]))

    # 总胜利场次爬取
    if total_times == 0:
        print "无比赛记录"
        total_wins = 0
        winbet = 0
        level = 0
    else:
        print "总场次:", total_times
        middle = re.findall("totalWin\":.*?,", t)
        total_wins = int(OnlyNum(middle[1]))
        print "总胜利场次:", total_wins
        winbet = "%.2f" %(float(total_wins)/float(total_times))
        print "胜率：", winbet
        middle = str(t)
        level = middle[34:40]
        print "当前等级：", level
    list_return = []

    list_return.append(roleid)
    list_return.append(role_name)
    list_return.append(total_times)
    list_return.append(total_wins)
    list_return.append(winbet)
    list_return.append(level)
    return list_return

# 初始化 excel
workbook = xlsxwriter.Workbook(file_name)
worksheet = workbook.add_worksheet(u"所有数据")
worksheet.write("A1", u"账号ID")
worksheet.write('B1', u'账号名字')
worksheet.write('C1', u'总场次')
worksheet.write("D1", u"胜利场次")
worksheet.write('E1', u'胜率')
worksheet.write('F1', u'等级')


list_excel = ["A", "B", "C", "D", "E", "F"]

def get_score(starno, endno):
    j = 2
    for i in range(starno, endno):
        print ("第%s个数据"%(j-1))
        print datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            list_score = score(i)
        except:
            logging.error("score%s出错"%i)
            continue
        # print "list is :", list_score, type(list_score)
        for k in range(2, 8):
                # print "sheet is :", list_excel[k-2]+str(j)
                # print k, "list 元素是:", list_score[int(k-2)]
                try:
                    worksheet.write(list_excel[k-2]+str(j), str(list_score[int(k-2)]).decode("utf-8"))
                except:
                    logging.error("写入错误")
                    continue
        j += 1

try:
    get_score(0, 20)
except:
    logging.error("get_score未知错误，结束")

workbook.close()


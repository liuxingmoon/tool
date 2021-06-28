#!/usr/bin/env python
# -*- coding: utf-8 -*-
#**************************************************************************#
# File Name   : remind_write_weekreport.py
# Author      : rendq
# Funtion     :
# Usage       : python remind_write_weekreport.py arg1
# Description :
#
# History     :
#   rendq   2021/04/09  0.0.1  create new file
#
#**************************************************************************#

from urllib.parse import quote
import requests
from requests.auth import HTTPDigestAuth
import re
import string
import os, sys
import datetime
from clip_ctrl import clip


check_weekday = 3#检查日期为周四（从0开始）
x86_members = [
    '任德强', '刁强', '代云平', '张兴建', '王毅', '徐松', '周通', '刘兴','余超'
    ]
    
def get_weekreports():
    today_date = datetime.date.today()
    today_weekday = datetime.datetime.now().weekday()#查看今天星期几
    dif_days = datetime.timedelta(days=today_weekday - check_weekday)#差异时间
    check_date = (today_date - dif_days).strftime("%Y-%m-%d")#检查日（确认检查日的目录名）
    
    svn_urls = [   
        "http://10.16.8.57:8001/svn/scrcu/Public/01.AB组周报/云平台组周报",
        "http://10.16.8.57:8001/svn/scrcu/Public/01.AB组周报/传统架构组/2021年",
    ]
    weekreports = []
    for svn_url in svn_urls:
        f = requests.get(quote(svn_url + f"/{check_date}",safe=string.printable), auth=("17416", "123456"))
        svn_lines = f.text.split("\n")

        for line in svn_lines:
            if 'xls' in line:
                r = re.search(r'xlsx?"\>(.*xlsx?)\<', line)
                weekreports.append(r.groups()[0])
    return (weekreports,check_date)

def start():
    date_hour = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M:%S")
    weekreports = get_weekreports()[0]
    commit_dir = get_weekreports()[1]
    uncommit_users = []
    #sendsms_cmd = "/usr/bin/python /data/scrcu_x86/scrcu_tools/sendsms.py '18708112761' '{}'"
    for name in x86_members:
        weekreport = [ f for f in weekreports if name in f ]
        if not weekreport:
            uncommit_users.append(name)

    if uncommit_users:
        result = "%s 周报检查："%(date_hour) + "、".join(uncommit_users) + "未交周报，请尽快提交至SVN %s目录"%(commit_dir)
    else:
        result = "周报已全部提交，可以汇总了"
    clip(result)
    #sms_text = f"[周报检查]{result}"
    #os.system(sendsms_cmd.format(sms_text))
    print(result)
    return (result)
    


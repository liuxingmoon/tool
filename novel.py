# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup as bs
import re
import urllib.request
from get_html import Get_html as G
import subprocess as p
import time
import os
import easygui as g
import configparser
import random
from user import headers

# 参数获取
config = configparser.ConfigParser()
config.read("Config.ini", encoding="utf-8")
novelpath = config.get("download", "novelpath")
if novelpath == '':
    novelpath = r'E:\\'
hidstart = config.get("download", "hidstart")
hidstop = config.get("download", "hidstop")


# 下载单个视频
def download(url):
    html = G().get_html(url)  # 获取网页信息
    soup = bs(html, 'html.parser')
    content = soup.get_text()#全部信息
    content = content.replace('\n', '').split()
    title = content[-14]
    for n in range(36):#清空前面
        del content[0]
    for n in range(15):#清空后面
        del content[-1]
    filename = novelpath + os.sep + title + '.mp4'
    print(filename)
    with open(filename,'a') as f:
        for line in content:
            f.write(line)

# 迭代下载视频
def download_videos(url, start, stop):
    for video in range(start, stop + 1):
        '''
        下载连接 起始下载页面 终止页面
        '''
        # print(url + os.sep + str(video) + '.html')
        download(url + str(video) + '.html')
        # time.sleep(600)#下载间隔10分钟

def start():
    ids = g.multenterbox(msg='输入起始和结束的页面数字', title='小说下载', fields=['起始页面', '结束页面'], values=[hidstart, hidstop])
    config.set("download", "hidstart", ids[0])
    config.set("download", "hidstop", ids[1])
    config.write(open("Config.ini", "w"))  # 保存到Config.ini
    download_videos(r'http://www.n6xsw.com/view.asp?id=3579032', int(ids[0]), int(ids[1]))


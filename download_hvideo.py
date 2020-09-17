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

#参数获取
config = configparser.ConfigParser()
config.read("Config.ini", encoding="utf-8")
downloadpath = config.get("download", "hvideopath")
if downloadpath == '':
    downloadpath = r'E:\\'
hidstart = config.get("download","hidstart")
hidstop = config.get("download","hidstop")


#下载单个视频
def download_video(url):
    html = G().get_html(url)#获取网页信息
    soup = bs(html,'html.parser')
    video_info = str(soup.find_all('video'))#获取视频信息
    src = re.search("http.{1,100}m3u8",video_info)#获取视频下载地址
    downurl = src.group()#视频下载地址
    print(downurl)
    video_title = str(soup.find_all("font"))#获取视频标题
    title_info = re.search('(>.{1,1000}<)',video_title)#获取标题信息
    title = title_info.group()#获取标题
    title = title.strip('><[]')#标题
    for old in ['《','》','【','】','（','）','@',':',';','.','*','+','-','*','/','[',']','{','}']:
        title = title.replace(old,'')
        title = title.replace(' ', '')#去除空格
    filename = downloadpath + os.sep + title + '.mp4'
    print(filename)
    process = p.Popen(r'ffmpeg -i %s -vcodec copy -acodec copy -absf aac_adtstoasc %s' %(downurl , filename) ,shell=True)#下载
    #os.popen(r'ffmpeg -i %s -vcodec copy -acodec copy -absf aac_adtstoasc %s' %(downurl , filename))
    
#迭代下载视频
def download_videos(url,start,stop):
    for video in range(start,stop + 1):
        '''
        下载连接 起始下载页面 终止页面
        '''
        #print(url + os.sep + str(video) + '.html')
        download_video(url + str(video) + '.html')
        #time.sleep(600)#下载间隔10分钟
def close():
    shutdown_ff = "taskkill /f /IM ffmpeg.exe"
    process = p.Popen( shutdown_ff ,shell=True)#关闭

def start():
    ids = g.multenterbox(msg='输入起始和结束的页面数字',title='伊人AV',fields=['起始页面','结束页面'],values=[hidstart,hidstop])
    config.set("download", "hidstart", ids[0])
    config.set("download", "hidstop", ids[1])
    config.write(open("Config.ini", "w"))  # 保存到Config.ini
    download_videos(r'https://www.yrcr3.com/play-30-',int(ids[0]),int(ids[1]))


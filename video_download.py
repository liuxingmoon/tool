#用you-get下载网页视频
import easygui as g
import subprocess as p
from bs4 import BeautifulSoup as bs
import re
import urllib.request
from get_html import Get_html as G
import os
import ctypes
import configparser
import user

#隐藏控制台
whnd = ctypes.windll.kernel32.GetConsoleWindow()
if whnd != 0:
    ctypes.windll.user32.ShowWindow(whnd, 0)
    ctypes.windll.kernel32.CloseHandle(whnd)
#下载路径获取
config = configparser.ConfigParser()
config.read("Config.ini", encoding="utf-8")
downloadpath = config.get("download", "videopath")
if downloadpath == '':
    downloadpath = r'E:\\'
hdownloadpath = config.get("download", "hvideopath")

download_headers = user.user['header']

#下载单个视频
def download_video_ffmpeg(url):
    get = G()
    html = get.get_html(url,'utf-8')#获取网页信息
    soup = bs(html,'html.parser')
    video_info = str(soup.find_all('video'))#获取视频信息
    src = re.search("http.{1,100}m3u8",video_info)#获取视频下载地址
    downurl = src.group()#视频下载地址
    print(downurl)
    video_title = str(soup.find_all("font"))#获取视频标题
    title_info = re.search('(>.{1,1000}<)',video_title)#获取标题信息
    title = title_info.group()#获取标题
    title = title.strip('><[]')#标题
    for old in ['《','》','【','】','（','）','@',':',';','.','*','+','-','*','/','[',']','{','}',',','，','。']:
        title = title.replace(old,'')
        title = title.replace(' ', '')#去除空格
    filename = downloadpath + title + '.mp4'
    print(filename)
    process = p.Popen(r'ffmpeg -i %s -vcodec copy -acodec copy -absf aac_adtstoasc %s' %(downurl , filename) ,shell=True)#下载

def download_video_m3u8(url):
    downurl = url#视频下载地址
    print(downurl)
    os.chdir(hdownloadpath)  # 切换到存放目录
    name = []  # 用来存放文件名，比较存放最大的数字到哪里了
    for each_file in os.listdir(os.curdir):  # 遍历所有文件
        if os.path.isfile(each_file):  # 如果是文件
            try:
                filename = int(re.findall(r'\d+', each_file)[0]) # 取出每个文件名的数字
                name.append(filename)  # 添加文件名到列表
            except IndexError as reason:
                print(str(reason))

    if str(max(name)).isalnum() == False:#如果返回的不是数字
        newfilename = '1.mp4'
    else:
        newfilename = str(max(name) + 1) + '.mp4'  # 新文件名比最大的+1
    filename = hdownloadpath + os.sep + newfilename
    print(filename)
    process = p.Popen(r'ffmpeg -i %s -vcodec copy -acodec copy -absf aac_adtstoasc %s' %(downurl , filename) ,shell=True)#下载

#默认下载
def download_video_you_get(url):
    process = p.Popen(r'you-get -o %s %s' %(downloadpath , url) ,shell=True)

def start():
    global downloadpath
    result = g.buttonbox(msg='群号：643442437', title='逍遥红尘', choices=['单个视频下载', '合集视频下载', '存储目录'])
    if result == '单个视频下载':
        # 单个视频下载
        msg = '请在下方输入需要下载视频的网页网址\n现在存储路径: %s \n默认存储路径: D:\\Users\\Administrator\\Downloads\\video' % (downloadpath)
        url = g.textbox(msg=msg)
        if 'm3u8' in url:
            download_video_m3u8(url)
        else:
            try:
                download_video_you_get(url)
                download_video_ffmpeg(url)
            except urllib.error.HTTPError as reason:
                print(str(reason))
    elif result == '合集视频下载':
        # 合集视频下载
        msg = '请在下方输入需要下载合集视频的最后一个视频网页网址\n现在存储路径: %s \n默认存储路径: D:\\' % (
            downloadpath)
        urls = g.textbox(msg=msg)  # 合集的最后一个url
        last = re.findall(r'\d+', urls)[-1]  # 匹配字符串中的数字的最后一串
        baseurl = urls.rstrip(last)  # 去掉最后一个字符
        start = 1
        end = int(last) + 1
        for no in range(start, end):  # 循环从1到end下载
            url = baseurl + str(no)  # 下载链接
            print(url)
            try:
                download_video_you_get(url)
                download_video_ffmpeg(url)
            except urllib.error.HTTPError as reason:
                print(str(reason))
                continue
    elif result == '存储目录':
        downloadpath = g.diropenbox(msg='选择存储目录', title='逍遥红尘')
        config.set("download", "videopath", downloadpath)
        config.write(open("Config.ini", "w"))  # 保存到Config.ini
    elif result == '':
        g.textbox(msg='输入网页地址！')

'''
if __name__ == "__main__":
    while True:
        result = g.buttonbox(msg='群号：643442437',title='逍遥红尘',choices=['单个视频下载','合集视频下载','存储目录'])
        if result == '单个视频下载':
            #单个视频下载
            msg='请在下方输入需要下载视频的网页网址\n现在存储路径: %s \n默认存储路径: D:\\Users\\Administrator\\Downloads\\video'%(downloadpath)
            url = g.textbox(msg=msg)
            if 'm3u8' in url:
                download_video_m3u8(url)
            else:
                try:
                    download_video_you_get(url)
                    download_video_ffmpeg(url)
                except urllib.error.HTTPError as reason:
                    print (str(reason))
        elif result == '合集视频下载':
            #合集视频下载
            msg='请在下方输入需要下载合集视频的最后一个视频网页网址\n现在存储路径: %s \n默认存储路径: D:\\Users\\Administrator\\Downloads\\video'%(downloadpath)
            urls = g.textbox(msg=msg)#合集的最后一个url
            last = re.findall(r'\d+',urls)[-1]#匹配字符串中的数字的最后一串
            baseurl = urls.rstrip(last)#去掉最后一个字符
            start = 1
            end = int(last) + 1
            
            for no in range(start,end):#循环从1到end下载
                url = baseurl + str(no)#下载链接
                print(url)
                try:
                    download_video_you_get(url)
                    download_video_ffmpeg(url)
                except urllib.error.HTTPError as reason:
                    print (str(reason))
                    continue
        elif result == '存储目录':
            downloadpath = g.diropenbox(msg='选择存储目录',title='逍遥红尘')
        elif result == '':
            g. textbox(msg='输入网页地址！')
        elif result == None:
            sys.exit(0)
'''



import subprocess
import threading
import os
import easygui as g
import time
import click,requests,prettytable,Crypto

msg = []

def printout():
    global result,msg
    #msg.append('正在各个平台收集统计结果……稍等……')
    flag = 0
    while flag == 0:
        msg.append(result.stdout.readline().decode('utf-8'))
        time.sleep(15)
        print(msg[-1])
        if ('下载' in msg[-1]):
            flag = 1

def refresh():
    global msg
    return msg

def start():
    global result,msg
    song = g.textbox(msg='请在下方输入需要下载音乐名字')
    result = subprocess.Popen('python "E:\Program Files\Python\Python38\works\tools\music-dl\music-dl" -k %s -o "E:\System\Downloads"' % (song), shell = True, stdin=subprocess.PIPE, stderr=subprocess.PIPE,stdout=subprocess.PIPE)
    threading.Thread(target=printout).start()#开启线程读取返回信息
    while True:
        time.sleep(15)
        if ('下载' in msg[-1]):
            #msg.pop()
            msg = str(msg)#转换为字符串
            c = g.textbox(msg=msg,title='存储在下载目录',text='输入下载序号，如果没有返回信息，直接点击ok')
            if (c == '') | (c == '输入下载序号，如果没有返回信息，直接点击ok'):
                c = '0-10'
            c += os.linesep
            result.stdin.write(c.encode('utf-8'))
        #result.stdin.flush()刷新缓冲区
        #msg.clear()
import subprocess
import threading
import os
import easygui as g
import time
import click,requests,prettytable,Crypto



def songCmd(song):
    cmd = r'python "E:\Program Files\Python\Python38\works\tools\music-dl\music-dl" -o "E:\System\Downloads\music"'
    s = subprocess.Popen(cmd,stdin=subprocess.PIPE, stdout=subprocess.PIPE,universal_newlines=True, shell = True)
    s.stdin.write(song + '\n')#下载所有
    time.sleep(3)
    out, err = s.communicate(input='0-10 \n')#下载所有
    if err is not None: 
        return err
    #out = out.decode('GBK','ignore')#转换为字符串
    #out = out.split('|')
    return out
    
    
def start():
    song = g.textbox(msg='请在下方输入需要下载音乐名字')
    songCmd(song)

import codecs
import re
from bs4 import BeautifulSoup
import subprocess
from pynput.keyboard import Key, Listener
import keyboard as k
import time
import win32api
import win32con
import sys
import os
import threading
import inspect
import ctypes

filepath = r'C:\Users\Administrator\AppData\Local\Temp\text view.txt'

def parseFile(filepath):
    #先关闭弹出的notepad
    time.sleep(1)
    subprocess.Popen(r'taskkill /F /IM notepad.exe',shell=True)
    time.sleep(1)
    try:
        with open(filepath, 'r') as fp:
            encoding = 'utf-16-le'
            with codecs.open(filepath, 'r', encoding) as fp2:
                soup = BeautifulSoup(fp2,'lxml')
                lines = str(soup)
                line = re.split('[()]',lines)
                line1 = line[1].split(',')
                line2 = line[3].split(',')[1].strip(' ')
                line2 = int(float(line2))
                print(line2)
                with open(filepath,"w") as f:
                    f.write('(%s,%s,%s,0,stand01,%d,0,0)' %(line1[0].strip(' '),line1[1].strip(' '),line1[2].strip(' '),line2))
                    #打开已经修改好的notepad
                    subprocess.Popen(filepath,shell=True)
                print(line)
    except:
        print ('[ERROR]')

#分别定义a键的信号量对象
semaphore_flag = threading.Semaphore(0)

#定义全局变量作为监测线程介入的开关
s_flag = 0
#定义全局变量作为整个程序的开关
flag = 0

def on_press_s(key):#监听`键作为开始
    # 监听按键`
    global s_flag
    if str(key)=="'"+'`'+"'" and s_flag == 0:
        print('开始',s_flag)
        #s_flag信号量加一
        semaphore_flag.release()
    elif str(key)=="'"+'`'+"'" and s_flag == 1:
        print("结束",s_flag)
        s_flag = 0

def press_s():
    global s_flag
    while True:
        #消费一个s_flag信号量
        semaphore_flag.acquire()
        #全局变量s_flag赋值为1，阻断监控函数的介入
        s_flag = 1
        MapVirtualKey = ctypes.windll.user32.MapVirtualKeyA
        #time.sleep(0.1)
        try:
            parseFile(filepath)
        except KeyboardInterrupt:
            sys.exit()
        #全局变量s_flag赋值为0，监控函数又可以介入了
        s_flag = 0
        print('自动过滤位置')

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

def stop_thread(thread):
    _async_raise(thread.ident , SystemExit)



def start():
    global flag,flag_switch

    # 运行进程
    t1 = Listener(on_press=on_press_s)
    t1.daemon = True
    t2 = threading.Thread(target=press_s, name='sendThreads')
    t2.daemon = True
    if flag == 0:
        t1.start()
        t2.start()
        flag = 1
    elif flag == 1:
        stop_thread(t1)
        stop_thread(t2)
        flag = 0

    #os.system("pause")#暂停
    
    

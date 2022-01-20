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

#分别定义a键的信号量对象
semaphore_s_flag_1 = threading.Semaphore(0)
semaphore_s_flag_2 = threading.Semaphore(0)

#定义全局变量作为监测线程介入的开关
s_flag_1 = 0
s_flag_2 = 0
#定义全局变量作为整个程序的开关
flag_1 = 0
flag_2 = 0

def on_press_start_1(key):#监听scroll_lock键作为开始
    # 监听按键q
    global s_flag_1
    if key == Key.scroll_lock and s_flag_1 == 0:
        print('开始',s_flag_1)
        #s_flag_1信号量加一
        semaphore_s_flag_1.release()
    elif key == Key.scroll_lock and s_flag_1 == 1:
        print("结束",s_flag_1)
        s_flag_1 = 0
        
def on_press_start_2(key):#监听scroll_lock键作为开始
    # 监听按键q
    global s_flag_2
    if key == Key.pause and s_flag_2 == 0:
        print('开始',s_flag_2)
        #s_flag_1信号量加一
        semaphore_s_flag_2.release()
    elif key == Key.pause and s_flag_2 == 1:
        print("结束",s_flag_2)
        s_flag_2 = 0
        
def on_press_start_long(key):#监听`键作为开始
    # 监听按键q
    if str(key)=="'"+'~'+"'":
        k.mouse_click_long()
        
def press_stop_1():
    global s_flag_1
    while True:
    	#消费一个s_flag_1信号量
        semaphore_s_flag_1.acquire()
        #全局变量s_flag_1赋值为1，阻断监控函数的介入
        s_flag_1 = 1
        MapVirtualKey = ctypes.windll.user32.MapVirtualKeyA
        #time.sleep(0.1)
        try:
            while s_flag_1==1:
                k.mouse_click()
                time.sleep(0.02)#每秒点击50次
        except KeyboardInterrupt:
            sys.exit()
        #全局变量s_flag_1赋值为0，监控函数又可以介入了
        s_flag_1 = 0
        print('快速连续点击')
        
def press_stop_2():
    global s_flag_2
    while True:
    	#消费一个s_flag_1信号量
        semaphore_s_flag_2.acquire()
        #全局变量s_flag_1赋值为1，阻断监控函数的介入
        s_flag_2 = 1
        MapVirtualKey = ctypes.windll.user32.MapVirtualKeyA
        #time.sleep(0.1)
        try:
            while s_flag_2 == 1:
                k.mouse_click()
                time.sleep(0.5)#每秒点击2次
        except KeyboardInterrupt:
            sys.exit()
        #全局变量s_flag_1赋值为0，监控函数又可以介入了
        s_flag_2 = 0
        print('慢速连续点击')

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



def start_1():
    global flag_1,flag_2
    # 运行进程
    t1 = Listener(on_press=on_press_start_1)
    t1.daemon = True
    t2 = threading.Thread(target=press_stop_1, name='sendThreads_1')
    t2.daemon = True
    if flag_1 == 0:
        t1.start()
        t2.start()
        flag_1 = 1
    elif flag_1 == 1:
        stop_thread(t1)
        stop_thread(t2)
        flag_1 = 0
    # 运行进程
    t3 = Listener(on_press=on_press_start_2)
    t3.daemon = True
    t4 = threading.Thread(target=press_stop_2, name='sendThreads_1')
    t4.daemon = True
    if flag_2 == 0:
        t3.start()
        t4.start()
        flag_2 = 1
    elif flag_2 == 1:
        stop_thread(t3)
        stop_thread(t4)
        flag_2 = 0

def start_2():
    # 运行进程
    t3 = Listener(on_press=on_press_start_long)
    t3.daemon = True
    t3.start()


def start():
    start_1()
    start_2()

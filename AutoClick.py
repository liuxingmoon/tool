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
semaphore_s_flag = threading.Semaphore(0)

#定义全局变量作为监测线程介入的开关
s_flag = 0
#定义全局变量作为整个程序的开关
flag = 0

def on_press_s(key):#监听!键作为开始
    # 监听按键q
    global s_flag
    if str(key)=="'"+'!'+"'" and s_flag == 0:
        print('开始',s_flag)
        #s_flag信号量加一
        semaphore_s_flag.release()
    elif str(key)=="'"+'!'+"'" and s_flag == 1:
        print("结束",s_flag)
        s_flag = 0

def press_s():
    global s_flag
    while True:
    	#消费一个s_flag信号量
        semaphore_s_flag.acquire()
        #全局变量s_flag赋值为1，阻断监控函数的介入
        s_flag = 1
        MapVirtualKey = ctypes.windll.user32.MapVirtualKeyA
        #time.sleep(0.1)
        try:
            while s_flag==1:
                k.mouse_click()
                time.sleep(0.05)#每秒点击20次
        except KeyboardInterrupt:
            sys.exit()
        #全局变量s_flag赋值为0，监控函数又可以介入了
        s_flag = 0
        print('自动点击')

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
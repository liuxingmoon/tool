from pynput.keyboard import Key
import keyboard as k
import time
import win32api
import win32con
import sys
import os
import threading
from thread_ctrl import *

#分别定义a键的信号量对象
semaphore_s_flag_1 = threading.Semaphore(0)
semaphore_s_flag_2 = threading.Semaphore(0)

#定义全局变量作为监测线程介入的开关
s_flag_1 = 0
s_flag_2 = 0


def on_press_Listen(key):
    """'Caps Lock':连点;'tab':长按;
    """
    global s_flag_1,s_flag_2,thread_listen,thread_listen_caps
    if key == Key.caps_lock and s_flag_1 == 0:
        print('开始连点',s_flag_1)
        #s_flag_1信号量加一
        semaphore_s_flag_1.release()
    elif key == Key.caps_lock and s_flag_1 == 1:
        print("结束连点",s_flag_1)
        s_flag_1 = 0
    elif key == Key.tab and s_flag_2 == 0:
        print('开始长按',s_flag_2)
        #s_flag_2信号量加一
        semaphore_s_flag_2.release()
    elif key == Key.tab and s_flag_2 == 1:
        k.mouse_click_release()#释放左键
        print("结束长按",s_flag_2)
        s_flag_2 = 0
    elif key == Key.esc:#停止程序
        stop_thread(thread_listen)
        stop_thread(thread_listen_caps)
        stop_thread(thread_listen_tab)
        
def press_caps_lock():
    global s_flag_1
    while True:
    	#消费一个s_flag_1信号量
        semaphore_s_flag_1.acquire()
        #全局变量s_flag_1赋值为1，阻断监控函数的介入
        s_flag_1 = 1
        MapVirtualKey = ctypes.windll.user32.MapVirtualKeyA
        #time.sleep(0.1)
        try:
            while s_flag_1 == 1:
                k.mouse_click()
                time.sleep(0.02)#每秒点击50次
        except KeyboardInterrupt:
            sys.exit()
        #全局变量s_flag_1赋值为0，监控函数又可以介入了
        s_flag_1 = 0
        print('连点50t/s')
        
def press_tab():
    global s_flag_2
    while True:
        semaphore_s_flag_2.acquire()
        s_flag_2 = 1
        MapVirtualKey = ctypes.windll.user32.MapVirtualKeyA
        try:
            k.mouse_click_long()
        except KeyboardInterrupt:
            sys.exit()
        print('长按')

def start():
    global thread_listen,thread_listen_caps,thread_listen_tab
    thread_listen = start_listener("thread_listen",on_press_Listen)
    thread_listen_caps = start_thread("thread_listen_caps",press_caps_lock,'auto_click')
    thread_listen_tab = start_thread("thread_listen_tab",press_tab,'click_long')


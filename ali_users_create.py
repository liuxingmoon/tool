#阿里云创建辅助
from xlsx_ctrl import *
import win32gui,subprocess
from clip_ctrl import clip
import easygui as g
from pynput.keyboard import Key
from thread_ctrl import *

def get_info():#获取excel文档信息
    excel_path = g.fileopenbox(msg='打开创建用户excel文档',title='创建用户')
    data = readXlsx(excel_path,"ASCM用户权限")#data=[[],[],[]]
    data_new = []#过滤掉None['','','']
    for m in data:
        if m[1] not in [None,'工号']:#工号不为空
            data_new.append(m[1])
            data_new.append(m[2])
            data_new.append(m[3])
            data_new.append(m[4])
    return (data_new)
    

        
def on_press(key):#按下
    pass
    
def on_release_insert(key):#松开insert
    global data,thread_listener
    try:
        if key == Key.insert:
            if data == []:#如果data为空，直接关闭listener
                g.msgbox(msg='我是有底线的！',title="创建ASCM账号")
                stop_thread(thread_listener)
                return ("已结束创建账号")
            clip(data[0])
            data.pop(0)
    except IndexError:
        g.msgbox(msg='我是有底线的！',title="创建ASCM账号")
        stop_thread(thread_listener)
        return ("已结束创建账号")
           
def start():
    global data,thread_listener
    data = get_info()
    data = [str(x) for x in data]
    thread_listener = start_listener("thread_listener",on_release_insert)


        
        
#阿里云创建辅助
from xlsx_ctrl import *
import win32gui,subprocess
from clip_ctrl import clip
import easygui as g
from pynput.keyboard import Key, Listener


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
    

def on_press_start(key):#监听prt键作为开始
    global data
    if key == Key.print_screen:
        clip(data[0])
        #data.pop(0)#删掉第一个
        
def on_press(key):#按下
    pass
    
def on_release(key):#松开
    global data,text
    try:
        if key == Key.print_screen:
            text = data[0]
            clip(text)
            data.pop(0)
    except IndexError:
        g.msgbox(msg='我是有底线的！',title="创建ASCM账号")
        
def start_listen():
    with Listener(on_press=None, on_release=on_release) as listener:
        listener.join()

def start():
    global data
    data = get_info()
    data = [str(x) for x in data]
    start_listen()


        
        
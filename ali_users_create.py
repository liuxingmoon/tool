#阿里云创建辅助
from xlsx_ctrl import *
import win32gui,subprocess,threading
from clip_ctrl import clip
import easygui as g
from pynput.keyboard import Key, Listener

#分别定义a键的信号量对象
semaphore_s_flag_1 = threading.Semaphore(0)
#定义全局变量作为监测线程介入的开关
s_flag_1 = 0
#定义全局变量作为整个程序的开关
flag_1 = 0

def get_info():#获取excel文档信息
    excel_path = g.fileopenbox(msg='打开创建用户excel文档',title='创建用户')
    data = readXlsx(excel_path)#data=[[],[],[]]
    data_new = []#过滤掉None['','','']
    for m in data:
        if m[1] not in [None,'工号']:#工号不为空
            data_new.append(m[1])
            data_new.append(m[2])
            data_new.append(m[3])
            data_new.append(m[4])
    return (data_new)
    
data = get_info()

def on_press_start_1(key):#监听~键作为开始
    # 监听按键q
    global s_flag_1,data
    if str(key)=="'"+'~'+"'" and s_flag_1 == 0:
        try:
            clip(data[0])
            data_new.pop(0)#删掉第一个
        except IndexError as reason:
            pass
        semaphore_s_flag_1.release()
    elif str(key)=="'"+'~'+"'" and s_flag_1 == 1:
        print("结束",s_flag_1)
        s_flag_1 = 0
    
def press_stop_1():
    global s_flag_1
    while True:
    	#消费一个s_flag_1信号量
        semaphore_s_flag_1.acquire()
        #全局变量s_flag_1赋值为1，阻断监控函数的介入
        s_flag_1 = 1
        MapVirtualKey = ctypes.windll.user32.MapVirtualKeyA
        try:
            clip(data[0])
            data_new.pop(0)#删掉第一个
        except IndexError as reason:
            pass
        #全局变量s_flag_1赋值为0，监控函数又可以介入了
        s_flag_1 = 0

    
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
 
#def start_1():
if __name__ == "__main__":
    #global flag_1
    # 运行进程
    t1 = Listener(on_press=on_press_start_1)
    t1.daemon = True
    t2 = threading.Thread(target=press_stop_1, name='sendThreads_1')
    t2.daemon = True
    if flag_1 == 0:
        t1.start()
        flag_1 = 1
    elif flag_1 == 1:
        stop_thread(t1)
        flag_1 = 0
        
        
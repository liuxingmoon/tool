import tkinter as tk
import time
import os
import tkinter.messagebox as messagebox
import tkinter.filedialog
import tkinter.colorchooser as colorchooser
import AutoClick as ak
import video_download as vd
import music_download as music
import subprocess
import download_hvideo as avyrdl
import thunder_daily_task_v2 as tdtask
import lotteryDraw as lottery
import coc,coc_customer
import poweroff
import translate
import translate_url
from PIL import ImageGrab
from pynput.keyboard import Key, Listener
import thunder_sign_in
import netmask,stock
import novel
import wuxia_getpos as pos
import wifi
import threading
import inspect
import ctypes
import update_coc

root = tk.Tk()
root.title('流梦星璃')
title = tk.Label(root,text='小工具').grid(row=0,column=2)
#鼠标连点
'''
autoclick_text = tk.Label(root,#放在框架1里面
                text = '"`"为开关',
                justify='left',#左对齐
                padx=5,
                pady=20,
                compound='left',width=15)
autoclick_text.grid(row=1,column=1,padx=10,pady=10)
'''
#开启鼠标连点
autoclick_bt = tk.Button(root,text='连点"!"',command=ak.start,width=15)
autoclick_bt.grid(row=1,column=1,
              padx=10,pady=10)

#截屏~
class FreeCapture():
    """ 用来显示全屏幕截图并响应二次截图的窗口类
    """

    def __init__(self, root, img):
        # 变量X和Y用来记录鼠标左键按下的位置
        self.X = tkinter.IntVar(value=0)
        self.Y = tkinter.IntVar(value=0)
        # 屏幕尺寸
        screenWidth = root.winfo_screenwidth()
        screenHeight = root.winfo_screenheight()
        # 创建顶级组件容器
        self.top = tkinter.Toplevel(root, width=screenWidth, height=screenHeight)
        # 不显示最大化、最小化按钮
        self.top.overrideredirect(True)
        self.canvas = tkinter.Canvas(self.top, bg='white', width=screenWidth, height=screenHeight)
        # 显示全屏截图，在全屏截图上进行区域截图
        self.image = tkinter.PhotoImage(file=img)
        self.canvas.create_image(screenWidth // 2, screenHeight // 2, image=self.image)

        self.lastDraw = None

        # 鼠标左键按下的位置
        def onLeftButtonDown(event):
            self.X.set(event.x)
            self.Y.set(event.y)
            # 开始截图
            self.sel = True

        self.canvas.bind('<Button-1>', onLeftButtonDown)

        def onLeftButtonMove(event):
            # 鼠标左键移动，显示选取的区域
            if not self.sel:
                return
            try:  # 删除刚画完的图形，要不然鼠标移动的时候是黑乎乎的一片矩形
                self.canvas.delete(self.lastDraw)
            except Exception as e:
                pass
            self.lastDraw = self.canvas.create_rectangle(self.X.get(), self.Y.get(), event.x, event.y, outline='green')

        def onLeftButtonUp(event):
            # 获取鼠标左键抬起的位置，保存区域截图
            self.sel = False
            try:
                self.canvas.delete(self.lastDraw)
            except Exception as e:
                pass

            time.sleep(0.5)
            # 考虑鼠标左键从右下方按下而从左上方抬起的截图
            left, right = sorted([self.X.get(), event.x])
            top, bottom = sorted([self.Y.get(), event.y])
            pic = ImageGrab.grab((left + 1, top + 1, right, bottom))
            # 弹出保存截图对话框
            fileName = tkinter.filedialog.asksaveasfilename(title='保存截图', filetypes=[('image', '*.jpg *.png')],
                                                            defaultextension='.png')

            if fileName:
                pic.save(fileName)
            # 关闭当前窗口
            self.top.destroy()

        self.canvas.bind('<B1-Motion>', onLeftButtonMove)  # 按下左键
        self.canvas.bind('<ButtonRelease-1>', onLeftButtonUp)  # 抬起左键
        # 让canvas充满窗口，并随窗口自动适应大小
        self.canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)


def screenShot():
    """ 自由截屏的函数 (button按钮的事件)
    """
    #    print("test")
    root.state('icon')  # 最小化主窗体
    time.sleep(0.5)
    im = ImageGrab.grab()
    # 暂存全屏截图
    im.save('temp.png')
    im.close()
    # 进行自由截屏
    w = FreeCapture(root, 'temp.png')
    # 截图结束，恢复主窗口，并删除temp.png文件
    root.state('normal')
    os.remove('temp.png')

def on_press(key):
    pass

def on_release(key):
    global all_key
    all_key.append(str(key))
    print(all_key)
    if 'Key.ctrl_l' in all_key and "'s'" in all_key:  # ctrl+c
        print('截屏')
        all_key.clear()
        screenShot()
    try:
        if all_key[-1] == 'Key.ctrl_l':
            time1 = time.time()
            while True:
                if time.time() - time1 >= 1:
                    all_key.clear()
                    break
    except:
        pass
    # if key == Key.esc:  # 停止监听
    #     return Falseurn False

def start_listen():
    with Listener(on_press=None, on_release=on_release) as listener:
        listener.join()

def start():
    global all_key
    all_key = []
    start_listen()


#分别定义a键的信号量对象
semaphore_flag = threading.Semaphore(0)
#定义全局变量作为监测线程介入的开关
s_flag = 0
#定义全局变量作为整个程序的开关
flag = 0

def on_press_s(key):#监听`键作为开始
    # 监听按键`
    global s_flag
    if str(key)=="'"+'#'+"'" and s_flag == 0:
        print('开始',s_flag)
        #s_flag信号量加一
        semaphore_flag.release()
    elif str(key)=="'"+'#'+"'" and s_flag == 1:
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
            screenShot()
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



def startscreenShot():
    global flag,flag_switch
    # 运行进程
    t1 = Listener(on_press=on_press_s)
    t1.daemon = True
    t2 = threading.Thread(target=press_s, name='screenShot')
    t2.daemon = True
    if flag == 0:
        t1.start()
        t2.start()
        flag = 1
    elif flag == 1:
        stop_thread(t1)
        stop_thread(t2)
        flag = 0
    
screenShot_bt = tk.Button(root,text='截屏"#"',command=startscreenShot,width=15)
screenShot_bt.grid(row=2,column=1,
              padx=10,pady=10)
              
#开启过滤侠客风云传位置
pos_bt = tk.Button(root,text='侠客位置"·"',command=pos.start,width=15)
pos_bt.grid(row=3,column=1,
              padx=10,pady=10)

#迅雷、芯次元签到
thunderSign_bt = tk.Button(root,text='每日签到',command=thunder_sign_in.start,width=15)
thunderSign_bt.grid(row=4,column=1,
              padx=10,pady=10)
#迅雷任务
'''
thundertask_text = tk.Label(root,#放在框架1里面
                text = '迅雷任务',
                justify='left',#左对齐
                padx=5,
                pady=20,
                compound='left',width=15)
thundertask_text.grid(row=5,column=1,padx=10,pady=10)
'''
thundertask_bt = tk.Button(root,text='迅雷任务',command=tdtask.start,width=15)
thundertask_bt.grid(row=5,column=1,
              padx=10,pady=10)
              
#过滤迅雷链接
translateurl_bt = tk.Button(root,text='过滤链接',command=translate_url.start,width=15)
translateurl_bt.grid(row=5,column=3,
              padx=10,pady=10)

#部落冲突脚本
coc_bt = tk.Button(root,text='部落冲突',command=coc.start,width=15)
coc_bt.grid(row=6,column=1,
              padx=10,pady=10)
              
#视频下载
'''
videodownload_text = tk.Label(root,#放在框架1里面
                text = '网页视频下载',
                justify='left',#左对齐
                padx=5,
                pady=20,
                compound='left',width=15)
videodownload_text.grid(row=2,column=1,padx=10,pady=10)
'''
videodownload_bt = tk.Button(root,text='视频下载',command=vd.start,width=15)
videodownload_bt.grid(row=1,column=2,
              padx=10,pady=10)

#音乐下载
'''
musicdownload_text = tk.Label(root,#放在框架1里面
                text = '音乐下载',
                justify='left',#左对齐
                padx=5,
                pady=20,
                compound='left',width=15)
musicdownload_text.grid(row=3,column=1,padx=10,pady=10)
'''
musicdownload_bt = tk.Button(root,text='音乐下载',command=music.start,width=15)
musicdownload_bt.grid(row=2,column=2,
              padx=10,pady=10)
#抽奖
'''
lottery_text = tk.Label(root,#放在框架1里面
                text = '点击直播抽奖',
                justify='left',#左对齐
                padx=5,
                pady=20,
                compound='left',width=15)
lottery_text.grid(row=6,column=1,padx=10,pady=10)
'''
lottery_bt = tk.Button(root,text='直播抽奖',command=lottery.start,width=15)
lottery_bt.grid(row=3,column=2,
              padx=10,pady=10)
#定时关机
poweroff_bt = tk.Button(root,text='定时关机',command=poweroff.start,width=15)
poweroff_bt.grid(row=4,column=2,
              padx=10,pady=10)

#开启wifi热点
wifi_bt = tk.Button(root,text='wifi热点',command=wifi.start,width=15)
wifi_bt.grid(row=5,column=2,
              padx=10,pady=10)
              
#更新代码
update_coc_bt = tk.Button(root,text='更新代码',command=update_coc.start,width=15)
update_coc_bt.grid(row=6,column=2,
              padx=10,pady=10)
              
def colorchoose():
    rgb = colorchooser.askcolor()
    with open(r"颜色选择.txt","w") as f:
        f.write(str(rgb))
    subprocess.Popen(r"start 颜色选择.txt",shell=True)
    print(rgb)
'''
#颜色选择器
colorchooser_text = tk.Label(root,
                             text='颜色选择器',
                             justify='left',  # 左对齐
                             padx=5,
                             pady=20,
                             compound='left', width=15)
colorchooser_text.grid(row=4,column=1,padx=10,pady=10)
'''
colorchooser_bt = tk.Button(root,text='颜色选择',command=colorchoose,width=15)
colorchooser_bt.grid(row=1,column=3,
              padx=10,pady=10)
              
#翻译
translate_bt = tk.Button(root,text='翻译',command=translate.start,width=15)
translate_bt.grid(row=2,column=3,
              padx=10,pady=10)
#IP地址查询
netmask_bt = tk.Button(root,text='掩码IP查询',command=netmask.start,width=15)
netmask_bt.grid(row=3,column=3,
              padx=10,pady=10)
#股票信息
stock_bt = tk.Button(root,text='股票信息',command=stock.start,width=15)
stock_bt.grid(row=4,column=3,
              padx=10,pady=10)
              
#伊人av下载
'''
avyrdownload_text = tk.Label(root,#放在框架1里面
                text = '伊人下载',
                justify='left',#左对齐
                padx=5,
                pady=20,
                compound='left',width=15)
avyrdownload_text.grid(row=4,column=1,padx=10,pady=10)

avyrdownload_bt = tk.Button(root,text='伊人下载',command=avyrdl.start,width=15)
avyrdownload_bt.grid(row=3,column=2,
              padx=10,pady=10)
'''

#小说下载
'''
novel_bt = tk.Button(root,text='小说下载',command=novel.start,width=15)
novel_bt.grid(row=4,column=2,
              padx=10,pady=10)
'''

try:
    coc_customer.clarm('coc_customer.csv')
    root.mainloop()

except:
    root.destroy()
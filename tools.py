import tkinter
import tkinter.messagebox as messagebox
import tkinter.filedialog
import tkinter.colorchooser as colorchooser
import AutoClick as ak
import video_download as vd
import music_download as music
import download_hvideo as avyrdl
import thunder_daily_task_v2 as tdtask
import lotteryDraw as lottery
import coc,coc_customer
import poweroff,odps_grant
import translate,translate_url,thunder_sign_in
from PIL import ImageGrab
from pynput.keyboard import Key, Listener
import netmask,stock,subprocess,time,os,sys,ali_users_create
import wuxia_getpos as pos
import inspect,ctypes,wifi,threading,novel,win32clipboard
import work_table as work_tb
#import get_x86report as report
from PIL import Image
from io import BytesIO
import win32gui,win32api,packpy
from win32.lib import win32con
import ocr,statistics_dev,statistics_resource,ecs_init,base64_ctrl

root = tkinter.Tk()
appname = "流梦星璃"
root.title(appname)
title = tkinter.Label(root,text='小工具').grid(row=0,column=2)
#鼠标连点
'''
autoclick_text = tkinter.Label(root,#放在框架1里面
                text = '"`"为开关',
                justify='left',#左对齐
                padx=5,
                pady=20,
                compound='left',width=15)
autoclick_text.grid(row=1,column=1,padx=10,pady=10)
'''
#开启鼠标连点
autoclick_bt = tkinter.Button(root,text='连点"scr"长按"~"',command=ak.start,width=15)
autoclick_bt.grid(row=1,column=1,
              padx=10,pady=10)

#截屏~
# import pyscreenshot as ImageGrab
def send_msg_to_clip(type_data, msg):
    """
    操作剪贴板分四步：
    1. 打开剪贴板：OpenClipboard()
    2. 清空剪贴板，新的数据才好写进去：EmptyClipboard()
    3. 往剪贴板写入数据：SetClipboardData()
    4. 关闭剪贴板：CloseClipboard()

    :param type_data: 数据的格式，
    unicode字符通常是传 win32con.CF_UNICODETEXT
    :param msg: 要写入剪贴板的数据
    """
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(type_data, msg)
    win32clipboard.CloseClipboard()
    
def paste_img(file_img):
    """
    图片转换成二进制字符串，然后以位图的格式写入剪贴板

    主要思路是用Image模块打开图片，
    用BytesIO存储图片转换之后的二进制字符串

    :param file_img: 图片的路径
    """
    # 把图片写入image变量中
    # 用open函数处理后，图像对象的模式都是 RGB
    image = Image.open(file_img)

    # 声明output字节对象
    output = BytesIO()

    # 用BMP (Bitmap) 格式存储
    # 这里是位图，然后用output字节对象来存储
    image.save(output, 'BMP')

    # BMP图片有14字节的header，需要额外去除
    data = output.getvalue()[14:]

    # 关闭
    output.close()

    # DIB: 设备无关位图(device-independent bitmap)，名如其意
    # BMP的图片有时也会以.DIB和.RLE作扩展名
    # 设置好剪贴板的数据格式，再传入对应格式的数据，才能正确向剪贴板写入数据
    send_msg_to_clip(win32clipboard.CF_DIB, data)
    

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
        
        try:
            #os.remove('temp.png')
            os.remove('select.png')
        except FileNotFoundError as reason:
            print(reason)
            
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
            '''fileName = tkinter.filedialog.asksaveasfilename(title='保存截图', filetypes=[('image', '*.jpg *.png')],
                                                defaultextension='.png')

if fileName:'''
            pic.save('select.png')#保存截图
            paste_img('select.png')#复制截图到剪切板
            # 关闭当前窗口
            self.top.destroy()

        self.canvas.bind('<B1-Motion>', onLeftButtonMove)  # 按下左键
        self.canvas.bind('<ButtonRelease-1>', onLeftButtonUp)  # 抬起左键
        # 让canvas充满窗口，并随窗口自动适应大小
        self.canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)

def screenShot():#截屏后剪切
    """ 自由截屏的函数 (button按钮的事件)
    """
    #    print("test")
    root.state('icon')  # 最小化主窗体
    time.sleep(0.5)
    im = ImageGrab.grab()
    # 暂存全屏截图
    im.save('temp.png')
    im.close()
    time.sleep(0.5)
    # 进行自由截屏
    w = FreeCapture(root, 'temp.png')
    # 将主窗口放在最前方，方便截图
    para_hld = win32gui.FindWindow(None, appname)
    win32api.keybd_event(13, 0, 0, 0) #防止出bug
    win32gui.SetForegroundWindow(para_hld)

def screen():#只截屏不剪切
    im = ImageGrab.grab()
    file_name = r'截屏_%s.png' %(time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()))
    count_png = 0
    list_png = []
    for png in os.listdir():
        if '截屏_' in png:
            list_png.append(png)
            count_png += 1
    if count_png >= 10:#截图保存10张
        for rm_png in list_png:
            os.remove(rm_png)
    im.save(file_name)# 存全屏截图
    im.close()
    
def on_press(key):
    pass

def on_release(key):
    global all_key
    all_key.append(str(key))
    print(all_key)
    if 'Key.ctrl_l' in all_key and "'s'" in all_key:  # ctrl+c
        print('截屏')
        all_key.clear()
        screenShot()#截图
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


#分别定义a键的信号量对象
semaphore_flag_ps = threading.Semaphore(0)
semaphore_flag_sl = threading.Semaphore(0)
semaphore_flag_pb = threading.Semaphore(0)
#定义全局变量作为监测线程介入的开关
ps_flag = 0
pb_flag = 0
sl_flag = 0
#定义全局变量作为整个程序的开关
flag_startscreenShot = 0
flag_startscreenocr = 0
flag_startscreen = 0

def on_press_PrintScreen(key):#监听'Print Screen'键作为开始
    # 监听按键`
    global ps_flag
    print(str(key))
    if key == Key.print_screen and ps_flag == 0:
        print('开始',ps_flag)
        #s_flag信号量加一
        semaphore_flag_ps.release()
    elif key == Key.print_screen and ps_flag == 1:
        print("结束",ps_flag)
        ps_flag = 0

def press_PrintScreen():
    global ps_flag
    while True:
    	#消费一个s_flag信号量
        semaphore_flag_ps.acquire()
        #全局变量s_flag赋值为1，阻断监控函数的介入
        ps_flag = 1
        MapVirtualKey = ctypes.windll.user32.MapVirtualKeyA
        #time.sleep(0.1)
        try:
            screenShot()#截图
        except KeyboardInterrupt:
            sys.exit()
        #全局变量s_flag赋值为0，监控函数又可以介入了
        ps_flag = 0
        print('自动过滤位置')

def on_press_ScrollLock(key):#监听'ScrollLock'键作为截屏
    # 监听按键`
    global sl_flag
    print(str(key))
    if key == Key.scroll_lock and sl_flag == 0:
        print('开始截全屏',sl_flag)
        #s_flag信号量加一
        semaphore_flag_sl.release()
    elif key == Key.scroll_lock and sl_flag == 1:
        print("结束",sl_flag)
        sl_flag = 0

def press_ScrollLock():
    global sl_flag
    while True:
        #消费一个s_flag信号量
        semaphore_flag_sl.acquire()
        #全局变量s_flag赋值为1，阻断监控函数的介入
        sl_flag = 1
        MapVirtualKey = ctypes.windll.user32.MapVirtualKeyA
        try:
            screen()#只截图
        except KeyboardInterrupt:
            sys.exit()
        #全局变量s_flag赋值为0，监控函数又可以介入了
        sl_flag = 0
        print('截全屏完成')
    
def on_press_Pause(key):#监听'Pause Break'键作为开始识图信号
    # 监听按键`
    global pb_flag
    print(str(key))
    if key == Key.pause and pb_flag == 0:
        print('开始识图',pb_flag)
        #s_flag信号量加一
        semaphore_flag_pb.release()
    elif key == Key.pause and pb_flag == 1:
        print("结束识图",pb_flag)
        pb_flag = 0

def press_Pause():
    global pb_flag
    while True:
    	#消费一个s_flag信号量
        semaphore_flag_pb.acquire()
        #全局变量s_flag赋值为1，阻断监控函数的介入
        pb_flag = 1
        MapVirtualKey = ctypes.windll.user32.MapVirtualKeyA
        #time.sleep(0.1)
        try:
            screenShot()#截图
            while True:#循环判断是否本地已生成'select.png'文件
                if 'select.png' in os.listdir():
                    try:
                        ocr.start('select.png')#识别
                    except:#没网直接跳过
                        pass
                    break
                time.sleep(0.5)
        except KeyboardInterrupt:
            sys.exit()
        #全局变量pb_flag赋值为0，监控函数又可以介入了
        pb_flag = 0
        print('自动过滤位置')
        
def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    print(tid)
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

def stop_thread(threadid):
    tid = threadid.ident
    print(tid)
    _async_raise( tid , SystemExit)


def startscreenShot():#截屏后剪切
    global flag_startscreenShot
    # 运行进程
    t1 = Listener(on_press=on_press_PrintScreen)
    t1.daemon = True
    t2 = threading.Thread(target=press_PrintScreen, name='screenShot')
    t2.daemon = True
    if flag_startscreenShot == 0:
        t1.start()
        t2.start()
        flag_startscreenShot = 1
    elif flag_startscreenShot == 1:
        #stop_thread(t1)
        #stop_thread(t2)
        flag_startscreenShot = 0
        
def startscreen():#只截全屏
    global flag_startscreen
    # 运行进程
    t3 = Listener(on_press=on_press_ScrollLock)
    t3.daemon = True
    t4 = threading.Thread(target=press_ScrollLock, name='screen')
    t4.daemon = True
    if flag_startscreen == 0:
        t3.start()
        t4.start()
        flag_startscreen = 1
    elif flag_startscreen == 1:
        #stop_thread(t3)
        #stop_thread(t4)
        flag_startscreen = 0
        
def startscreenocr():#截屏后剪切再ocr识图
    global flag_startscreenocr
    # 运行进程
    t5 = Listener(on_press=on_press_Pause)
    t5.daemon = True
    t6 = threading.Thread(target=press_Pause, name='ocr')
    t6.daemon = True
    if flag_startscreenocr == 0:
        t5.start()
        t6.start()
        flag_startscreenocr = 1
    elif flag_startscreenocr == 1:
        #stop_thread(t1)
        #stop_thread(t2)
        flag_startscreenocr = 0

def start_printScreen():
    startscreenShot()
    startscreen()
    
def start_ocr():
    startscreenocr()
    
screenShot_bt = tkinter.Button(root,text='截屏"Print Screen"',command=start_printScreen,width=15)
screenShot_bt.grid(row=2,column=1,
              padx=10,pady=10)
              
ocr_bt = tkinter.Button(root,text='识图"Pause Break"',command=start_ocr,width=15)
ocr_bt.grid(row=3,column=1,
              padx=10,pady=10)
              
#开启过滤侠客风云传位置
pos_bt = tkinter.Button(root,text='侠客位置"·"',command=pos.start,width=15)
pos_bt.grid(row=4,column=1,
              padx=10,pady=10)

#迅雷、芯次元签到
'''
thunderSign_bt = tkinter.Button(root,text='每日签到',command=thunder_sign_in.start,width=15)
thunderSign_bt.grid(row=5,column=1,
              padx=10,pady=10)
'''
#迅雷任务
'''
thundertask_text = tkinter.Label(root,#放在框架1里面
                text = '迅雷任务',
                justify='left',#左对齐
                padx=5,
                pady=20,
                compound='left',width=15)
thundertask_text.grid(row=5,column=1,padx=10,pady=10)

thundertask_bt = tkinter.Button(root,text='迅雷任务',command=tdtask.start,width=15)
thundertask_bt.grid(row=5,column=1,
              padx=10,pady=10)
'''
#部落冲突脚本
coc_bt = tkinter.Button(root,text='部落冲突',command=coc.start,width=15)
coc_bt.grid(row=5,column=1,
              padx=10,pady=10)
              
#ODPS授权
coc_bt = tkinter.Button(root,text='ODPS授权',command=odps_grant.start,width=15)
coc_bt.grid(row=6,column=1,
              padx=10,pady=10)
              
#故障设备
statistics_dev_bt = tkinter.Button(root,text='故障设备',command=statistics_dev.start,width=15)
statistics_dev_bt.grid(row=7,column=1,
              padx=10,pady=10)
              
#ASCM账号
ali_users_create_bt = tkinter.Button(root,text='ASCM账号',command=ali_users_create.start,width=15)
ali_users_create_bt.grid(row=8,column=1,
              padx=10,pady=10)
              
              
#视频下载
'''
videodownload_text = tkinter.Label(root,#放在框架1里面
                text = '网页视频下载',
                justify='left',#左对齐
                padx=5,
                pady=20,
                compound='left',width=15)
videodownload_text.grid(row=2,column=1,padx=10,pady=10)
'''
videodownload_bt = tkinter.Button(root,text='视频下载',command=vd.start,width=15)
videodownload_bt.grid(row=1,column=2,
              padx=10,pady=10)

#音乐下载
'''
musicdownload_text = tkinter.Label(root,#放在框架1里面
                text = '音乐下载',
                justify='left',#左对齐
                padx=5,
                pady=20,
                compound='left',width=15)
musicdownload_text.grid(row=3,column=1,padx=10,pady=10)
'''
musicdownload_bt = tkinter.Button(root,text='音乐下载',command=music.start,width=15)
musicdownload_bt.grid(row=2,column=2,
              padx=10,pady=10)
'''
#直播抽奖
lottery_bt = tkinter.Button(root,text='直播抽奖',command=lottery.start,width=15)
lottery_bt.grid(row=3,column=2,
              padx=10,pady=10)
'''
lottery_bt = tkinter.Button(root,text='直播抽奖',command=lottery.start,width=15)
lottery_bt.grid(row=3,column=2,
              padx=10,pady=10)
#开启wifi热点
wifi_bt = tkinter.Button(root,text='wifi热点',command=wifi.start,width=15)
wifi_bt.grid(row=3,column=2,
              padx=10,pady=10)
              
#定时关机
poweroff_bt = tkinter.Button(root,text='定时关机',command=poweroff.start,width=15)
poweroff_bt.grid(row=4,column=2,
              padx=10,pady=10)

#ecs_init
ecs_init_bt = tkinter.Button(root,text='ecs初始化',command=ecs_init.start,width=15)
ecs_init_bt.grid(row=5,column=2,
              padx=10,pady=10)

#筛选表格
work_tb_bt = tkinter.Button(root,text='筛选表格',command=work_tb.start,width=15)
work_tb_bt.grid(row=6,column=2,
              padx=10,pady=10)
              
#转码base64
base64_bt = tkinter.Button(root,text='转码base64',command=base64_ctrl.start,width=15)
base64_bt.grid(row=7,column=2,
              padx=10,pady=10)
              
              
def colorchoose():
    rgb = colorchooser.askcolor()
    with open(r"颜色选择.txt","w") as f:
        f.write(str(rgb))
    subprocess.Popen(r"start 颜色选择.txt",shell=True)
    print(rgb)
'''
#颜色选择器
colorchooser_text = tkinter.Label(root,
                             text='颜色选择器',
                             justify='left',  # 左对齐
                             padx=5,
                             pady=20,
                             compound='left', width=15)
colorchooser_text.grid(row=4,column=1,padx=10,pady=10)
'''
colorchooser_bt = tkinter.Button(root,text='颜色选择',command=colorchoose,width=15)
colorchooser_bt.grid(row=1,column=3,
              padx=10,pady=10)
              
#翻译
translate_bt = tkinter.Button(root,text='翻译',command=translate.start,width=15)
translate_bt.grid(row=2,column=3,
              padx=10,pady=10)
#IP地址查询
netmask_bt = tkinter.Button(root,text='掩码IP查询',command=netmask.start,width=15)
netmask_bt.grid(row=3,column=3,
              padx=10,pady=10)
#股票信息
stock_bt = tkinter.Button(root,text='股票信息',command=stock.start,width=15)
stock_bt.grid(row=4,column=3,
              padx=10,pady=10)
              
#过滤迅雷链接
translateurl_bt = tkinter.Button(root,text='过滤链接',command=translate_url.start,width=15)
translateurl_bt.grid(row=5,column=3,
              padx=10,pady=10)
#打包程序
packpy_bt = tkinter.Button(root,text='打包程序',command=packpy.start,width=15)
packpy_bt.grid(row=6,column=3,
              padx=10,pady=10)
              
#统计资源
statistics_resource_bt = tkinter.Button(root,text='统计资源',command=statistics_resource.start,width=15)
statistics_resource_bt.grid(row=7,column=3,
              padx=10,pady=10)
'''
#周报汇总
report_bt = tkinter.Button(root,text='周报汇总',command=report.start,width=15)
report_bt.grid(row=6,column=3,
              padx=10,pady=10)
              
#伊人av下载

avyrdownload_text = tkinter.Label(root,#放在框架1里面
                text = '伊人下载',
                justify='left',#左对齐
                padx=5,
                pady=20,
                compound='left',width=15)
avyrdownload_text.grid(row=4,column=1,padx=10,pady=10)

avyrdownload_bt = tkinter.Button(root,text='伊人下载',command=avyrdl.start,width=15)
avyrdownload_bt.grid(row=3,column=2,
              padx=10,pady=10)
'''

#小说下载
'''
novel_bt = tkinter.Button(root,text='小说下载',command=novel.start,width=15)
novel_bt.grid(row=4,column=2,
              padx=10,pady=10)
'''

try:
    coc_customer.clarm('coc_customer.csv')
    root.mainloop()

except:
    root.destroy()
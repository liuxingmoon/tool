#coding:utf-8
import subprocess
import time
import easygui as g
import re
import configparser
import win32gui
from win32.lib import win32con
import datetime
import threading

#元素坐标
pos = {
  'coc_script':[500,680],
  'start_script':[200,1070],
  'sure':[360,935]
  }
#日志路径
Coclog = r'C:\Users\Administrator\Desktop\刘兴\coc\coclog.txt'
configpath = r"E:\Program Files\Python\Python38\works\tools\Config.ini"
ddpath = r'D:\Program Files\DundiEmu\DunDiEmu.exe'

def start(action,startport,wait_time):
    #开模拟器
    subprocess.Popen(action,shell=True)
    time.sleep(wait_time)
    #打印当前时间
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    #确保模拟器进程已经启动
    '''
    while True:
        result = subprocess.Popen('tasklist|findstr DunDiEmu.exe',shell = True,stdout=subprocess.PIPE).stdout.readline().split()[0]
        print (result)
        if result == b'DunDiEmu.exe':
            time.sleep(3)
            break
    
    #确保最小化
    for n in range(2):
        try:
            wnd = win32gui.FindWindow(u'Qt5QWindowIcon', None)  # 获取窗口句柄
            win32gui.CloseWindow(wnd)  # 窗口最小化
            wndcoc = win32gui.FindWindow(None, u'coc_script3')  # 获取窗口句柄
            win32gui.CloseWindow(wndcoc)  # 窗口最小化
        except :
            break
    '''
    #等待系统开机
    time.sleep(30)
    # 关闭模拟器连接
    subprocess.Popen('adb kill-server', shell=True)
    time.sleep(3)
    #开启模拟器连接
    subprocess.Popen('adb start-server', shell=True)
    time.sleep(3)
    #重启并连接连接
    subprocess.Popen(r'adb connect 127.0.0.1:%d' %(startport),shell = True)
    time.sleep(3)
    '''
    if result.split()[0] == b'unable':
        close()
    '''

#打开黑松鼠
def coc_script(startport):
    process = subprocess.Popen(r'adb -s 127.0.0.1:%d shell am start -n com.ais.foxsquirrel.coc/ui.activity.SplashActivity' %(startport),shell=True)
    time.sleep(10)
    
#点击屏幕
def click(x,y,startport):
    process = subprocess.Popen(r'adb -s 127.0.0.1:%d shell input tap %d %d' %(startport,x,y),shell=True)
    time.sleep(3)

def close():
    subprocess.Popen('taskkill /f /t /im DunDiEmu.exe & taskkill /f /t /im DdemuHandle.exe',shell=True)
    time.sleep(3)

#关闭指定id窗口
def handle_window_play(hwnd,extra):
    if win32gui.IsWindowVisible(hwnd):
        global closeplayid
        closeplayid = int(closeplayid)
        if closeplayid <= 0:
            closeplayid = maxid - 6 + closeplayid 
        elif closeplayid < 10:
            closeplayid = '0' + str(closeplayid)
        #关闭的id是跳过列表或者捐兵列表，递归关闭前一个id
        if str(closeplayid + 6) in skipids:
            closeplayid = int(closeplayid) - 1
            print('此关闭id ：%s没有打开，需要跳过!' %(closeplayid))
            win32gui.EnumWindows(handle_window_play,None)
        if str(closeplayid) in win32gui.GetWindowText(hwnd):
            print(closeplayid)
            win32gui.PostMessage(hwnd,win32con.WM_CLOSE,0,0)
#关闭捐兵id
def handle_window_donate(hwnd,wndname):
    if win32gui.IsWindowVisible(hwnd):
        for closedonateid in ['星陨','QQ2-星辰','QQ5-星核','码奴']:
            if closedonateid in win32gui.GetWindowText(hwnd):
                win32gui.PostMessage(hwnd,win32con.WM_CLOSE,0,0)

#等待
def timewait(min):
    for n in range(min):
        time.sleep(60)

def getport(startid,skipids):
    #获取启动端口
    if startid == 0:
        #如果恰好既是第一个id，又是要跳过的id，或者是捐兵id，需要往下id+1
        if str(startid) in skipids:
            print(r'该模拟器id %d 在禁止启动名单之中，跳过!' %(startid))
            startid += 1
            #递归获取port
            return getport(startid,skipids)
        else:
            startport = 5555
            return [startid,startport]
    #skipids
    elif str(startid) in skipids:
        #如果恰好既是最后一个id，又是要跳过的id，需要直接循环为初始id
        if startid == maxid:
            print(r'该模拟器id %d 在禁止启动名单之中，跳过!' %(startid))
            startid = minid
        else:
            print(r'该模拟器id %d 在禁止启动名单之中，跳过!' %(startid))
            startid += 1
        #递归获取port
        return getport(startid,skipids)
    else:
        startport = 52550 + startid
        return [startid,startport]

def play(wait_time,skipids):
    # 参数获取
    #config = configparser.ConfigParser()
    #config.read(configpath, encoding="utf-8")
    #为了指定关闭startid，全局
    global startid
    startid = config.get("coc", "startid")
    startid = int(startid)#取出数据为string
    startlist = getport(startid,skipids)
    startid = int(startlist[0])#获取启动模拟器id
    startport = startlist[1]#获取port
    action = r'"D:\Program Files\DundiEmu\DunDiEmu.exe" -multi %d -disable_audio  -fps 40' %(startid)
    start(action,startport,wait_time)
    print('启动模拟器完成')
    time.sleep(3)
    coc_script(startport)
    print('启动脚本完成')
    time.sleep(1)
    click(pos['sure'][0], pos['sure'][1],startport)
    time.sleep(3)
    click(pos['start_script'][0],pos['start_script'][1],startport)
    #每启动一个模拟器，需要关闭一个
    global closeplayid
    closeplayid = startid - 6 - instance_num
    win32gui.EnumWindows(handle_window_play,None)
    
    #回滚startid
    if startid == maxid:   #结束id
        startid = minid-1   #开始id - 1
    config.set("coc", "startid", str(startid + 1))#只能存储str类型数据
    config.write(open(configpath, "w",encoding='utf-8'))  # 保存到Config.ini
    #打印分割线
    read_id = startid
    if read_id == 0:
        read_id = '星痕'
    elif read_id == 1:
        read_id = '星辰'
    elif read_id == 2:
        read_id = '星空'
    elif read_id == 3:
        read_id = '星河'
    elif read_id == 4:
        read_id = '星核'
    elif read_id == 5:
        read_id = '星陨'
    else:
        read_id = str(read_id - 6)
        if int(read_id) < 0:
            read_id = str(maxid)
    print(r'============================= %s 实例启动完成 ===============================' %(read_id))

#捐兵号
def play_donate(donateid):
    #获取上一次运行的捐兵id
    donateid_now = config.get("coc", "donateid_now")#str
    #获取即将运行的捐兵index
    if donateid_now in donateid:
        donateindex = donateid.index(donateid_now)
    else:
        donateindex = -1
    #获取即将运行的捐兵id
    if (donateindex == len(donateid) - 1) or (donateindex == -1):
        donateid_now = donateid[0]
    else:
        donateid_now = donateid[donateindex + 1]
    #写入config
    config.set("coc", "donateid_now", donateid_now)#只能存储str类型数据
    config.write(open(configpath, "w",encoding='utf-8'))  # 保存到Config.ini
    global startport
    if int(donateid_now) == 0:
        startport = 5555
    else:
        startport = 52550 + int(donateid_now)
    action = r'"D:\Program Files\DundiEmu\DunDiEmu.exe" -multi %d -disable_audio  -fps 40' %(int(donateid_now))
    start(action,startport,3)
    print('启动捐兵模拟器完成')
    time.sleep(3)
    coc_script(startport)
    print('启动脚本完成')
    time.sleep(1)
    click(pos['sure'][0], pos['sure'][1],startport)
    time.sleep(3)
    click(pos['start_script'][0],pos['start_script'][1],startport)
    #打印分割线
    read_id = int(donateid_now)
    if read_id == 0:
        read_id = '星痕'
    elif read_id == 1:
        read_id = '星辰'
    elif read_id == 2:
        read_id = '星空'
    elif read_id == 3:
        read_id = '星河'
    elif read_id == 4:
        read_id = '星核'
    elif read_id == 5:
        read_id = '星陨'
    else:
        read_id = str(read_id - 6)
    print(r'============================= %s 实例启动完成 ===============================' %(read_id))
    
    
#根据时间判断运行实例数量
def instance(donate_switch,donateid):
    # 转换字符串类型时间为datetime.date类型，这样才能做逻辑大小判断
    day_time_end = datetime.datetime.strptime(str(datetime.datetime.now().date()) + " " + day_time, '%Y-%m-%d %H:%M')
    night_time_end =  datetime.datetime.strptime(str(datetime.datetime.now().date()) + " " + night_time, '%Y-%m-%d %H:%M')
    morning_time_end =  datetime.datetime.strptime(str(datetime.datetime.now().date()) + " " + morning_time, '%Y-%m-%d %H:%M')
    # 当前时间
    now_time = datetime.datetime.now()
    # 判断当前时间是否在范围时间内
    if now_time >= day_time_end or now_time < night_time_end:
        print('目前处于晚上,可以执行 %d 实例, %d 分钟，可以运行捐兵实例' %(instance_num_night,instance_time_night*60))
        #付费捐兵号(晚上运行启动)
        if donate_switch in ['True','1','T']:
            print('持久运行号开始运行！')
        else:
            print('没有持久运行号需要运行！')
        return [instance_num_night,instance_time_night,'晚上']
    elif now_time >= night_time_end and now_time < morning_time_end:
        print('目前处于凌晨,可以执行 %d 实例, %d 分钟，不需要运行捐兵实例' %(instance_num_morning,instance_time_morning*60))
        return [instance_num_morning,instance_time_morning,'凌晨']
    else:
        print('目前处于白天,可以执行%d实例,%d分钟' %(instance_num_day,instance_time_day*60))
        #付费捐兵号(白天运行启动)
        if donate_switch in ['True','1','T']:
            print('持久运行号开始运行！')
        else:
            print('没有持久运行号需要运行！')
        return [instance_num_day,instance_time_day,'白天']

#重启打资源
def restartplay():
    #同时运行几个实例
    wait_time = 3
    for times in range(instance_num):
        play(wait_time,skipids)
        wait_time += 1
    #运行该coc实例时间
    t = int(3600*instance_time)
    time.sleep(t)
        
#重启捐兵号
def restartdonate(donateid):
    global donatetime_start
    # 大于4小时就关闭捐兵号，并重新启动捐兵号
    donatetime_end = datetime.datetime.now()
    starttime = donatetime_end - donatetime_start
    if (starttime.seconds / 3600) >= 4:
        print(r'运行捐兵号超过4小时，下线15分钟！')
        win32gui.EnumWindows(handle_window_donate, None)
        timewait(15)
        donatetime_start = datetime.datetime.now()
        print(r'已经下线15分钟，开始捐兵！')
        for n in range(donate_num):
            play_donate(donateid)

#开始操作
#coc
if __name__ == "__main__":
    #获取配置文件参数skipid,donateid,instance_num,instance_time
    config = configparser.ConfigParser()
    config.read(configpath, encoding="utf-8")
    #启动id范围
    minid = int(config.get("coc", "minid"))
    maxid = int(config.get("coc", "maxid"))
    #跳过启动的id初始列表
    skipidlists = config.get("coc", "skipid").split()
    skipids = skipidlists.copy()
    #skipids = [str(x) for x in skipids]#需要把int转换成str，不然下面会报错
    for everyid in skipidlists:
        if "-" in str(everyid):
            start = everyid.split("-")[0]
            end = everyid.split("-")[1]
            #临时跳过列表,注意这里的元素是int
            skiplist = range(int(start),int(end)+1)
            skipids.extend(skiplist)
            skipids.remove(everyid)#删除该列表
            skipids = [str(x) for x in skipids]#需要把int转换成str，不然下面会报错
            skipids = list(set(skipids))#去重
    
    #捐兵（一直运行）
    donate_switch = config.get("coc", "donate_switch")#是否开启捐兵
    donateid = config.get("coc", "donateid").split()#获取捐兵id的list
    donate_num = int(config.get("coc", "donate_num"))#捐兵号的个数
    #查看捐兵号的开关是否打开，打开就跳过该id
    if donate_switch in ['True','1','T']:
        skipids.extend(donateid)#添加捐兵的id到跳过id列表中
        skipids = list(set(skipids))#去重
    print('跳过的实例id：%s' %([x for x in skipids]))
    #白天和夜晚运行的实例数量和时间
    instance_num_day = int(config.get("coc", "instance_num_day"))
    instance_time_day = float(config.get("coc", "instance_time_day"))
    instance_num_night = int(config.get("coc", "instance_num_night"))
    instance_time_night = float(config.get("coc", "instance_time_night"))
    instance_num_morning = int(config.get("coc", "instance_num_morning"))
    instance_time_morning = float(config.get("coc", "instance_time_morning"))
    #获取时间段
    day_time = config.get("coc", "day_time")
    night_time = config.get("coc", "night_time")
    morning_time = config.get("coc", "morning_time")
    #获取当前时间判断启动持续时间
    donatetime_start = datetime.datetime.now()
    #首次启动捐兵号
    for n in range(donate_num):
        play_donate(donateid)
    while True:
        #关闭
        #close()
        #获取当前时间的参数并运行持久化运行号
        result = instance(donate_switch,donateid)
        #启动打资源的模拟器个数
        instance_num = result[0]
        #if result[2] != '凌晨':
        if donate_switch in ['True','1','T']:
            if instance_num < donate_num:
                instance_num = 0
            else:
                instance_num = instance_num - donate_num
        #等待时间
        instance_time = result[1]
        #使用线程实现重启捐兵和启动打资源分开
        thread_restartplay = threading.Thread(target=restartplay(), name='restartdonate')
        thread_restartdonate = threading.Thread(target=restartdonate(donateid), name='restartdonate')
        thread_restartplay.start()
        thread_restartdonate.start()
        thread_restartplay.join()
        thread_restartdonate.join()
#coding=utf-8
import subprocess
import time
import easygui as g
import re
import configparser
import win32gui
from win32.lib import win32con
import datetime
import threading
import coc_template
import os
import AutoClick as ak

#元素坐标
pos = {
  'coc_script':[500,680],
  'start_script':[200,1070],
  'login_wandoujia1': [640, 500],
  'login_wandoujia2': [640, 300],
  'login_kunlun': [640, 250],
  'login_kunlun1': [640, 560],
  'login_kunlun2': [640, 620],
  'sure':[360,935]
  }

#日志路径
Coclog = r'E:\Program Files\Python\Python38\works\tool\coclog.txt'
configpath = r"E:\Program Files\Python\Python38\works\tool\Config.ini"
ddpath = r'D:\Program Files\DundiEmu\DunDiEmu.exe'


def reboot():
    subprocess.Popen(r'shutdown /f /r /t 60',shell=True)

def start(action,startport,wait_time):
    #开模拟器
    subprocess.Popen(action,shell=True)
    time.sleep(wait_time)
    #打印当前时间
    print(r'当前的时间为：%s' %(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    #确保模拟器进程已经启动

    #等待系统开机
    time.sleep(40)
    # 关闭模拟器连接
    subprocess.Popen('adb kill-server', shell=True)
    time.sleep(3)
    #开启模拟器连接
    subprocess.Popen('adb start-server', shell=True)
    time.sleep(3)
    #重启并连接连接
    if startport == 5555:
        subprocess.Popen(r'adb connect emulator-5554',shell = True)
        subprocess.Popen(r'adb connect 127.0.0.1:%d' %(startport),shell = True)
    else:
        subprocess.Popen(r'adb connect 127.0.0.1:%d' %(startport),shell = True)
    time.sleep(3)
    '''
    if result.split()[0] == b'unable':
        close()
    '''

#打开黑松鼠
def coc_script(startport,wait_time):
    time.sleep(wait_time)
    if startport == 5555:
        subprocess.Popen(r'adb -s emulator-5554 shell am start -n com.ais.foxsquirrel.coc/ui.activity.SplashActivity',shell=True)
        result = subprocess.Popen(r'adb -s 127.0.0.1:%d shell am start -n com.ais.foxsquirrel.coc/ui.activity.SplashActivity' %(startport),shell=True,stdout=subprocess.PIPE)
        text = result.stdout.readlines()#元组存储
    else:
        result = subprocess.Popen(r'adb -s 127.0.0.1:%d shell am start -n com.ais.foxsquirrel.coc/ui.activity.SplashActivity' %(startport),shell=True,stdout=subprocess.PIPE)
        text = result.stdout.readlines()#元组存储
    if 'not found' in text:
        with open(Coclog,'a') as Coclogfile:
            Coclogfile.write('出现bug重启主机,重启时间：%s\n' %(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        reboot()
    time.sleep(10)
    
    
#点击屏幕
def click(x,y,startport,*args):
    if startport == 5555:
        subprocess.Popen(r'adb -s emulator-5554 shell input tap %d %d' %(x,y),shell=True)
    subprocess.Popen(r'adb -s 127.0.0.1:%d shell input tap %d %d' %(startport,x,y),shell=True)
    print(x,y)
    time.sleep(3)
    if len(args) > 0:
        time.sleep(args[0])

def close():
    subprocess.Popen('taskkill /f /t /im DunDiEmu.exe & taskkill /f /t /im DdemuHandle.exe & taskkill /f /t /im adb.exe',shell=True)
    time.sleep(3)

#等待
def timewait(min):
    for n in range(min):
        time.sleep(60)

def getport(startid,skipids):
    #每启动一个模拟器，需要关闭一个
    global closeplayid
    #关闭id
    closeplayid = startid - 6 - instance_num
    #win32gui.EnumWindows(handle_window_play,None)
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
            print(r'============================= 该模拟器id %d 在禁止启动名单之中，跳过! ===============================' %(startid))
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
    try:
        #启动新一个打资源id前先关闭上一个打资源id
        win32gui.EnumWindows(handle_window_play,None)
        global startid
        startid = config.get("coc", "startid")
        startid = int(startid)#取出数据为string
        startlist = getport(startid,skipids)
        startid = int(startlist[0])#获取启动模拟器id
        startport = startlist[1]#获取port
        action = r'"D:\Program Files\DundiEmu\DunDiEmu.exe" -multi %d -disable_audio  -fps 40' %(startid)
        start(action,startport,wait_time)
        print('============================= 启动模拟器完成 =============================')
        time.sleep(3)
        coc_script(startport,wait_time)
        click(pos['sure'][0], pos['sure'][1],startport)
        time.sleep(5)
        click(pos['start_script'][0],pos['start_script'][1],startport)
        print('============================= 启动打资源脚本完成 =============================')
        if startport == 52555:#如果是星陨，尝试点击登录 
            time.sleep(20)
            click(pos['login_wandoujia1'][0], pos['login_wandoujia1'][1], startport,3)
            click(pos['login_wandoujia2'][0], pos['login_wandoujia2'][1], startport,3)
        else:
            #昆仑
            time.sleep(20)
            #click(pos['login_kunlun'][0], pos['login_kunlun'][1], startport,3)
            click(pos['login_kunlun1'][0], pos['login_kunlun1'][1], startport,3)
            click(pos['login_kunlun2'][0], pos['login_kunlun2'][1], startport,3)
        #打印分割线
        read_id = playnames[startid]
        print(r'============================= %s 实例启动完成 ===============================' %(read_id))  
        #回滚startid
        if startid == maxid:   #结束id
            startid = minid-1   #开始id - 1
        config.set("coc", "startid", str(startid + 1))#只能存储str类型数据
        config.write(open(configpath, "w",encoding='utf-8'))  # 保存到Config.ini
    except:
        print('============================= 实例启动失败 ===============================')

#付费捐兵号
def play_donate_for_paid(donateids):
    #获取上一次运行的捐兵id
    global donateid_now
    donateid_now = config.get("coc", "donateid_for_paid_now")#str
    #获取即将运行的捐兵index
    if donateid_now in donateids:
        try:
            donateindex = donateids.index(donateid_now)
        except:
            donateindex = -1
    else:
        donateindex = -1
    #获取即将运行的捐兵id
    if (donateindex == len(donateids) - 1) or (donateindex == -1):
        donateid_now = donateids[0]
    else:
        donateid_now = donateids[donateindex + 1]
    #写入config
    config.set("coc", "donateid_for_paid_now", donateid_now)#只能存储str类型数据
    config.write(open(configpath, "w",encoding='utf-8'))  # 保存到Config.ini
    if int(donateid_now) == 0:
        startport = 5555
    else:
        startport = 52550 + int(donateid_now)
    action = r'"D:\Program Files\DundiEmu\DunDiEmu.exe" -multi %d -disable_audio  -fps 40' %(int(donateid_now))
    start(action,startport,30)
    print(r'============================= 启动付费捐兵模拟器完成 ===============================')
    time.sleep(3)
    coc_script(startport,5)
    time.sleep(5)
    click(pos['sure'][0], pos['sure'][1],startport)
    time.sleep(5)
    click(pos['start_script'][0],pos['start_script'][1],startport)
    if startport == 52555:#如果是星陨，尝试点击登录 
        time.sleep(20)
        click(pos['login_wandoujia1'][0], pos['login_wandoujia1'][1], startport,3)
        click(pos['login_wandoujia2'][0], pos['login_wandoujia2'][1], startport,3)
    else:
        #昆仑
        time.sleep(20)
        #click(pos['login_kunlun'][0], pos['login_kunlun'][1], startport,3)
        click(pos['login_kunlun1'][0], pos['login_kunlun1'][1], startport,3)
        click(pos['login_kunlun2'][0], pos['login_kunlun2'][1], startport,3)
    print(r'============================= 启动付费捐兵脚本完成 ===============================')

    
#捐兵号
def play_donate(donateids):
    
    #获取上一次运行的捐兵id
    global donateid_now#这是为了让handler能够获取到该id
    donateid_now = config.get("coc", "donateid_now")#str
    #获取即将运行的捐兵index
    if donateid_now in donateids:
        try:
            donateindex = donateids.index(donateid_now)
        except:
            donateindex = -1
    else:
        donateindex = -1
    #获取即将运行的捐兵id
    if (donateindex == len(donateids) - 1) or (donateindex == -1):
        donateid_now = donateids[0]
    else:
        donateid_now = donateids[donateindex + 1]
    #写入config
    config.set("coc", "donateid_now", donateid_now)#只能存储str类型数据
    config.write(open(configpath, "w",encoding='utf-8'))  # 保存到Config.ini
    if int(donateid_now) == 0:
        startport = 5555
    else:
        startport = 52550 + int(donateid_now)
    action = r'"D:\Program Files\DundiEmu\DunDiEmu.exe" -multi %d -disable_audio  -fps 40' %(int(donateid_now))
    start(action,startport,30)
    print(r'============================= 启动捐兵模拟器完成 ===============================')
    time.sleep(3)
    coc_script(startport,5)
    time.sleep(5)
    click(pos['sure'][0], pos['sure'][1],startport)
    time.sleep(5)
    click(pos['start_script'][0],pos['start_script'][1],startport)
    if startport == 52555:#如果是星陨，尝试点击登录 
        time.sleep(20)
        click(pos['login_wandoujia1'][0], pos['login_wandoujia1'][1], startport,3)
        click(pos['login_wandoujia2'][0], pos['login_wandoujia2'][1], startport,3)
    else:
        #昆仑
        time.sleep(20)
        #click(pos['login_kunlun'][0], pos['login_kunlun'][1], startport,3)
        click(pos['login_kunlun1'][0], pos['login_kunlun1'][1], startport,3)
        click(pos['login_kunlun2'][0], pos['login_kunlun2'][1], startport,3)
    print(r'============================= 启动自用捐兵脚本完成 ===============================')
    #打印分割线
    read_id = donatenames[donateid_now]
    print(r'============================= %s 实例启动完成 ===============================' %(read_id))
    
def play_resource(resourceids):
    #获取上一次运行的打资源id
    #global resourceid_now
    resourceid_now = config.get("coc", "resourceid_now")#str
    #获取即将运行的捐兵index
    if resourceid_now in resourceids:
        try:
            resourceidindex = resourceids.index(resourceid_now)
        except:
            resourceidindex = -1
    else:
        resourceidindex = -1
    #获取即将运行的捐兵id
    if (resourceidindex == len(resourceids) - 1) or (resourceidindex == -1):
        resourceid_now = resourceids[0]
    else:
        resourceid_now = resourceids[resourceidindex + 1]
    #写入config
    config.set("coc", "resourceid_now", resourceid_now)#只能存储str类型数据
    config.write(open(configpath, "w",encoding='utf-8'))  # 保存到Config.ini
    if int(resourceid_now) == 0:
        startport = 5555
    else:
        startport = 52550 + int(resourceid_now)
    action = r'"D:\Program Files\DundiEmu\DunDiEmu.exe" -multi %d -disable_audio  -fps 40' %(int(resourceid_now))
    start(action,startport,30)
    print(r'============================= 启动模拟器完成 ===============================')
    time.sleep(3)
    coc_script(startport,5)
    time.sleep(5)
    click(pos['sure'][0], pos['sure'][1],startport)
    time.sleep(5)
    click(pos['start_script'][0],pos['start_script'][1],startport)
    if startport == 52555:#如果是星陨，尝试点击登录 
        time.sleep(20)
        click(pos['login_wandoujia1'][0], pos['login_wandoujia1'][1], startport,3)
        click(pos['login_wandoujia2'][0], pos['login_wandoujia2'][1], startport,3)
    else:
        #昆仑
        time.sleep(20)
        #click(pos['login_kunlun'][0], pos['login_kunlun'][1], startport,3)
        click(pos['login_kunlun1'][0], pos['login_kunlun1'][1], startport,3)
        click(pos['login_kunlun2'][0], pos['login_kunlun2'][1], startport,3)
    print(r'============================= 启动持续打资源脚本完成 ===============================')
   
    
    
#根据时间判断运行实例数量
def instance(donate_switch,donateids):
    # 转换字符串类型时间为datetime.date类型，这样才能做逻辑大小判断
    day_time_end = datetime.datetime.strptime(str(datetime.datetime.now().date()) + " " + day_time, '%Y-%m-%d %H:%M')
    night_time_end =  datetime.datetime.strptime(str(datetime.datetime.now().date()) + " " + night_time, '%Y-%m-%d %H:%M')
    morning_time_end =  datetime.datetime.strptime(str(datetime.datetime.now().date()) + " " + morning_time, '%Y-%m-%d %H:%M')
    # 当前时间
    now_time = datetime.datetime.now()
    # 判断当前时间是否在范围时间内
    if now_time >= night_time_end or now_time < morning_time_end:
        print('目前处于晚上,可以执行 %d 实例, %d 分钟，可以运行捐兵实例' %(instance_num_night,instance_time_night*60))
        #付费捐兵号(晚上运行启动)
        if donate_switch in ['True','1','T']:
            print(r'============================= 持久运行号开始运行！ ===============================')
        else:
            print('没有持久运行号需要运行！')
        return [instance_num_night,instance_time_night,'晚上']
    elif now_time >= morning_time_end and now_time < day_time_end:
        print('目前处于凌晨,可以执行 %d 实例, %d 分钟，不需要运行捐兵实例' %(instance_num_morning,instance_time_morning*60))
        return [instance_num_morning,instance_time_morning,'凌晨']
    elif now_time >= day_time_end and now_time < night_time_end:
        print('目前处于白天,可以执行%d实例,%d分钟' %(instance_num_day,instance_time_day*60))
        #付费捐兵号(白天运行启动)
        if donate_switch in ['True','1','T']:
            print(r'============================= 持久运行号开始运行！ ===============================')
        else:
            print(r'============================= 没有持久运行号需要运行！ ===============================')
        return [instance_num_day,instance_time_day,'白天',donate_status]

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
        if str(int(closeplayid) + 6) in skipids:
            closeplayid = int(closeplayid) - 1
            print(r'============================= 此关闭的轮循打资源模拟器名字 ：%s没有打开，需要向上跳过1位! ===============================' %(str(int(closeplayid) + 1)))
            win32gui.EnumWindows(handle_window_play,None)
        if str(closeplayid) in win32gui.GetWindowText(hwnd):
            print(r'============================= 关闭的轮循打资源模拟器名字为：%s ===============================' %(str(closeplayid)))
            win32gui.PostMessage(hwnd,win32con.WM_CLOSE,0,0)

#关闭持续打资源号            
def handle_window_resource(hwnd,wndname):
    if win32gui.IsWindowVisible(hwnd):
        #关闭持续打资源号
        for resourceid in resource_names:
            closename = resource_names[donateid]
            if closename in win32gui.GetWindowText(hwnd):
                print(r'============================= 关闭的持续打资源号模拟器名字为：%s ===============================' %(str(closename)))
                #关闭一个捐兵号
                win32gui.PostMessage(hwnd,win32con.WM_CLOSE,0,0)

#关闭捐兵id
def handle_window_donate(hwnd,wndname):
    if win32gui.IsWindowVisible(hwnd):
        #关闭自用捐兵号
        for donateid in donatenames:
            closedonatename = donatenames[donateid]
            if closedonatename in win32gui.GetWindowText(hwnd):
                print(r'============================= 关闭的自用捐兵号模拟器名字为：%s ===============================' %(str(closedonatename)))
                #关闭一个捐兵号
                win32gui.PostMessage(hwnd,win32con.WM_CLOSE,0,0)
                
#重启打资源
def restartplay():
    #同时运行几个实例
    wait_time = 3
    for times in range(instance_num):
        play(wait_time,skipids)
        wait_time += 5
    #运行该coc实例时间
    t = int(3600*instance_time)
    time.sleep(t)
        
#重启捐兵号
def restartdonate(donateids):
    global donatetime_start
    # 大于4小时就关闭捐兵号，并重新启动捐兵号
    donatetime_end = datetime.datetime.now()
    starttime = donatetime_end - donatetime_start
    
    if (starttime.seconds / 3600) >= donate_time:
        win32gui.EnumWindows(handle_window_donate, None)
        if donate_mode == "A":
            print(r'============================= 运行捐兵号超过4小时，下线15分钟！ ===============================')
            timewait(15)
        else:
            print(r'============================= 当前使用的是轮循捐兵模式，不用等待15分钟！ ===============================')
        donatetime_start = datetime.datetime.now()
        print(r'============================= 已经下线15分钟，开始捐兵！ ===============================')
        for n in range(donate_num):
            play_donate(donateids)

#开始操作
#coc
if __name__ == "__main__":
    try:
        #关闭
        close()
        #打开自动点击
        ak.start()
        #第一次启动时间
        starttime_global = datetime.datetime.now()
        #获取配置文件参数skipid,donateids,instance_num,instance_time
        config = configparser.ConfigParser()
        config.read(configpath, encoding="utf-8")
        #启动id范围
        minid = int(config.get("coc", "minid"))
        maxid = len(os.listdir(r'D:\Program Files\DundiEmu\DundiData\avd\\')) - 2
        #maxid = int(config.get("coc", "maxid"))
        donate_time = float(config.get("coc", "donate_time"))
        #捐兵模式：一直捐兵（A)，还是半捐
        donate_mode = config.get("coc", "donate_mode")
        #跳过启动的id初始列表
        skipidlists = config.get("coc", "skipids").split()
        skipids = skipidlists.copy()
        warids = config.get("coc", "warids").split()
        skipids.extend(warids)#添加部落战控制的id到跳过id列表中
        skipids = list(set(skipids))#去重
        #skipids = [str(x) for x in skipids]#需要把int转换成str，不然下面会报错
        for everyid in skipidlists:
            if "-" in str(everyid):
                start = everyid.split("-")[0]
                end = everyid.split("-")[1]
                #临时跳过列表,注意这里的元素是int,必须全部转换为str，不然不一致了
                skiplist = [str(x) for x in range(int(start),int(end)+1)]
                print(skiplist)
                print(skipids)
                skipids.extend(skiplist)
                skipids.remove(everyid)#删除该列表
                print(skipids)
                skipids = [str(x) for x in skipids]#需要把int转换成str，不然下面会报错
                skipids = list(set(skipids))#去重
        
        #捐兵（一直运行）
        donate_switch = config.get("coc", "donate_switch")#是否开启捐兵
        donateids_for_paid = config.get("coc", "donateids_for_paid").split()#获取付费捐兵id的list
        donateids_for_paid_del_army = config.get("coc", "donateids_for_paid_del_army").split()#获取付费捐兵id删除兵的list
        donateids = config.get("coc", "donateids").split()#获取捐兵id的list
        resourceids = config.get("coc", "resourceids").split()#获取持续打资源id的list
        #在持续打资源的list去除付费捐兵的list
        resourceids = [x for x in resourceids if x not in donateids_for_paid]
        #在捐兵列表中去除付费捐兵的list和持续打资源的list
        donateids = [x for x in donateids if (x not in donateids_for_paid) and (x not in resourceids)]
        donatenames_for_paid = {}
        for donateid_for_paid in donateids_for_paid:
            donateconfig = r'D:\Program Files\DundiEmu\DundiData\avd\dundi%s\config.ini' %(donateid_for_paid)
            with open(donateconfig,'r') as donatefile:
                configlines = donatefile.readlines()
                for configline in configlines:
                    if 'EmulatorTitleName' in configline:
                        donatename = configline.split('=')[-1].rstrip('\n')
                        donatenames_for_paid[donateid_for_paid] = donatename
        print(r'============================= 当前的付费捐兵号id和名字为: %s ===============================' %(donatenames_for_paid))
        
        resource_names = {}
        for resourceid in resourceids:
            donateconfig = r'D:\Program Files\DundiEmu\DundiData\avd\dundi%s\config.ini' %(resourceid)
            with open(donateconfig,'r') as donatefile:
                configlines = donatefile.readlines()
                for configline in configlines:
                    if 'EmulatorTitleName' in configline:
                        donatename = configline.split('=')[-1].rstrip('\n')
                        resource_names[resourceid] = donatename
        print(r'============================= 当前的持续打资源号id和名字为: %s ===============================' %(resource_names))
        
        donatenames = {}
        for donateid in donateids:
            donateconfig = r'D:\Program Files\DundiEmu\DundiData\avd\dundi%s\config.ini' %(donateid)
            with open(donateconfig,'r') as donatefile:
                configlines = donatefile.readlines()
                for configline in configlines:
                    if 'EmulatorTitleName' in configline:
                        donatename = configline.split('=')[-1].rstrip('\n')
                        donatenames[donateid] = donatename
        print(r'============================= 当前的捐兵号id和名字为: %s ===============================' %(donatenames))
        
        #获取付费捐兵号数量
        donateids_for_paid_num = len(donateids_for_paid)
        #获取持续打资源id的list
        resourceids_num = int(config.get("coc", "resourceids_num"))#打资源号的个数
        #获取捐兵的数量
        if donate_mode == "A":
            donate_num = len(donateids)
        else:
            donate_num = int(config.get("coc", "donate_num"))#捐兵号的个数
        #查看捐兵号的开关是否打开，打开就跳过该id
        if donate_switch in ['True','1','T']:
            skipids.extend(donateids)#添加捐兵的id到跳过id列表中
            skipids.extend(donateids_for_paid)#添加捐兵的id到跳过id列表中
            skipids.extend(resourceids)#添加持续打资源的id到跳过id列表中
            skipids = list(set(skipids))#去重
            skipids.sort()
        print(r'============================= 跳过的实例id：%s ===============================' %(skipids))
        
        playnames = {}
        notplaylist = []
        notplaylist.extend(donateids)
        notplaylist.extend(donateids_for_paid)
        notplaylist.extend(resourceids)
        notplaylist.extend(skipids)
        notplaylist = list(set(notplaylist))#去重
        for playid in range(maxid +1):
            if str(playid) not in notplaylist:
                playconfig = r'D:\Program Files\DundiEmu\DundiData\avd\dundi%d\config.ini' %(playid)
                with open(playconfig,'r') as playfile:
                    configlines = playfile.readlines()
                    for configline in configlines:
                        if 'EmulatorTitleName' in configline:
                            playname = configline.split('=')[-1].rstrip('\n')
                            playnames[playid] = playname
        print(r'============================= 当前的打资源号和名字为: %s ===============================' %(playnames))
            
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
        while True:
            #获取捐兵号的状态（当前是在捐兵还是在打资源）
            config.read(configpath, encoding="utf-8")
            donate_status = config.get("coc", "donate_status")
            #关闭
            #close()
            #获取当前时间的参数并运行持久化运行号
            result = instance(donate_switch,donateids)
            #启动打资源的模拟器个数
            instance_num = result[0]
            if donate_switch in ['True','1','T']:
                if instance_num < donate_num:
                    instance_num = 0
                else:
                    instance_num = instance_num - donate_num - donateids_for_paid_num - resourceids_num
            #等待时间
            instance_time = result[1]
            #现在时间
            donate_time = result[2]
            #凌晨切换捐兵状态为打资源，顺便做一次部落战捐兵
            if (donate_time == '凌晨') and (donate_status == 'donate'):
                coc_template.convert_mode(donateids_for_paid,donate_status)
                coc_template.convert_mode(donateids,donate_status)
                coc_template.convert_mode(resourceids,donate_status)
                with open(Coclog,'a') as Coclogfile:
                    Coclogfile.write('凌晨切换捐兵状态为打资源,切换时间：%s\n' %(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
                #关闭
                close()
                donate_status = 'play'
                config.read(configpath, encoding="utf-8")
                config.set("coc", "donate_status", donate_status)#只能存储str类型数据
                config.write(open(configpath, "w",encoding='utf-8'))  # 保存到Config.ini
                #部落战捐兵
                #coc_template.wardonate(warids)
            #早上切换打资源状态为捐兵
            elif (donate_time != '凌晨') and (donate_status == 'play'):
                #刚启动等待一分钟避免打开模拟器卡顿
                print(r'============================= 刚重启主机启动coc测试等待一分钟避免打开模拟器卡顿 ===============================')
                timewait(1)
                coc_template.convert_mode(donateids_for_paid,donate_status,donateids_for_paid_del_army)
                #周5打资源，其他时间捐兵
                try:
                    if datetime.datetime.now().weekday() in [0,1,2,3,5,6]:
                        coc_template.convert_mode(donateids,donate_status)
                except:
                    print('出故障，不捐兵，继续打资源')
                with open(Coclog,'a') as Coclogfile:
                    Coclogfile.write('早上切换打资源状态为捐兵,切换时间：%s\n' %(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
                #关闭 
                close()
                donate_status = 'donate'
                config.read(configpath, encoding="utf-8")
                config.set("coc", "donate_status", donate_status)#只能存储str类型数据
                config.write(open(configpath, "w",encoding='utf-8'))  # 保存到Config.ini
            #启动付费捐兵号
            for n in range(donateids_for_paid_num):
                play_donate_for_paid(donateids_for_paid)
            #关闭持续打资源号
            win32gui.EnumWindows(handle_window_resource, None)
            #启动持续打资源号
            for n in range(resourceids_num):
                play_resource(resourceids)
            #关闭自用捐兵号    
            win32gui.EnumWindows(handle_window_donate, None)
            #启动捐兵号
            for n in range(donate_num):
                play_donate(donateids)
            #启动打资源号
            restartplay()
            endtime_global = datetime.datetime.now()
            runtime_global = endtime_global - starttime_global
            #每隔一天重启一次
            runtime = int(runtime_global.seconds / 3600)
            print(r'当前脚本已运行 %d 个小时!' %(runtime))
            if runtime >= 23:
                with open(Coclog,'a') as Coclogfile:
                    Coclogfile.write('运行时间超过一天重启主机,重启时间：%s\n' %(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
                #reboot()
    except:
        with open(Coclog,'a') as Coclogfile:
            Coclogfile.write('出现bug重启主机,重启时间：%s\n' %(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        reboot()
'''
        #使用线程实现重启捐兵和启动打资源分开
        thread_restartplay = threading.Thread(target=restartplay(), name='restartdonate')
        thread_restartdonate = threading.Thread(target=restartdonate(donateids), name='restartdonate')
        thread_restartplay.start()
        thread_restartdonate.start()
        thread_restartplay.join()
        thread_restartdonate.join()
'''

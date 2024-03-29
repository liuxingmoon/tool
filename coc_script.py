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
import keyboard as k
from coc_start import connect,login_click,close_emu_err,close_windows,getport,click,close,kill_adb,kill_server,start_server,restart_server,start_emu_convert,close_emu_id,pos
from multiprocessing import Process
import file_ctrl as fc
from config_ctrl import *
from readfile import *
from read_config import *


#日志路径
Coclog = r'coclog.txt'
ddpath = config_read(configpath,"coc","ddpath")
ddavd_path = config_read(configpath,'coc','ddavd_path')
configdir = os.path.dirname(os.path.abspath(configpath))#配置文件目录
backupdir = configdir + os.sep + "backup"
QQlists = config_read(configpath,"coc", "QQlists").split()
    
    
def close_VirtualBox():
    #关闭模拟器报错
    close_name = 'VirtualBox Headless Frontend'
    close_windows(close_name)
    
def start(action,startport,wait_time):
    #开模拟器
    subprocess.Popen(action,shell=True)
    time.sleep(wait_time)
    #打印当前时间
    print(r'当前的时间为：%s' %(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    #确保模拟器进程已经启动
    #等待系统开机
    time.sleep(40)
    restart_server()
    #重启并连接连接
    connect(startport)
    time.sleep(3)

def shutdown():
    close()
    with open(Coclog,'a') as Coclogfile:
        Coclogfile.write('关机时间：%s\n' %(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    subprocess.Popen(r'shutdown /f /s /t 30',shell=True)
    
def reboot():
    close()
    with open(Coclog,'a') as Coclogfile:
        Coclogfile.write('重启时间：%s\n' %(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    subprocess.Popen(r'shutdown /f /r /t 30',shell=True)
    
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
            Coclogfile.write('出现bug重启adb和模拟器,重启时间：%s\n' %(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        restart_server()
        connect(startport)
        coc_script(startport,wait_time)#递归重新执行一次
    time.sleep(20)
    

#等待
def timewait(min):
    for n in range(min):
        time.sleep(60)
        
def play(wait_time,skipids):
    #为了指定关闭startid，全局
    global startid
    startid = config_read(configpath,"coc", "startid")#获取的下一个准备开启的id
    startid = int(startid)#取出数据为string，获取启动模拟器id
    startlist = getport(startid,skipids)
    startid = int(startlist[0])#获取启动模拟器id,这里不能注释掉，因为getport函数会重新根据skipids递归获取新的startid
    startport = startlist[1]#获取port
    play_index = play_ids.index(startid)#获取启动id的index
    close_index = play_index - instance_num
    if close_index < 0:
        close_index = len(play_ids) + close_index
    close_id = play_ids[close_index]
    #关闭前一个模拟器
    close_emu_id(close_id)
    action = r'"D:\Program Files\DundiEmu\\DunDiEmu.exe" -multi %d -disable_audio  -fps 40' %(startid)
    #action = r'"D:\Program Files\DundiEmu\dundi_helper.exe" --index %d --start' %(startid)
    #启动新id
    start(action,startport,wait_time)
    print('============================= 启动模拟器完成 =============================')
    time.sleep(3)
    coc_script(startport,10)
    click(pos['sure'][0], pos['sure'][1],startport)
    time.sleep(60)
    click(pos['start_script'][0],pos['start_script'][1],startport)
    print('============================= 启动打资源脚本完成 =============================')
    login_click(startid)
    #打印分割线
    read_id = playnames[startid]
    print(r'============================= %s 实例启动完成 ===============================' %(read_id))
    #回滚startid
    if startid == maxid:   #结束id
        startid = minid-1   #开始id - 1
    config_write(configpath,"coc", "startid", str(startid + 1))#只能存储str类型数据

#付费捐兵号
def play_donate_for_paid(donateids):
    #获取上一次运行的捐兵id
    global donateid_now
    donateid_now = config_read(configpath,"coc", "donateid_for_paid_now")#str
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
    config_write(configpath,"coc", "donateid_for_paid_now", donateid_now)#只能存储str类型数据
    startport = getport(int(donateid_now))
    action = r'"D:\Program Files\DundiEmu\\DunDiEmu.exe" -multi %d -disable_audio  -fps 40' %(int(donateid_now))
    #action = r'"D:\Program Files\DundiEmu\dundi_helper.exe" --index %d --start' %(int(donateid_now))
    start(action,startport,40)
    print(r'============================= 启动付费捐兵模拟器完成 ===============================')
    time.sleep(3)
    coc_script(startport,10)
    time.sleep(5)
    click(pos['sure'][0], pos['sure'][1],startport)
    time.sleep(60)
    click(pos['start_script'][0],pos['start_script'][1],startport)
    login_click(donateid_now)
    print(r'============================= 启动付费捐兵脚本完成 ===============================')

    
#捐兵号
def play_donate(donateids):
    #获取上一次运行的捐兵id
    global donateid_now#这是为了让handler能够获取到该id
    donateid_now = config_read(configpath,"coc", "donateid_now")#str
    #获取即将运行的捐兵index
    if donateid_now in donateids:
        try:
            donateindex = donateids.index(donateid_now)
        except:
            donateindex = -1
    else:
        donateindex = -1
    #获取即将运行的捐兵id
    if (donateindex == len(donateids) - 1) or (donateindex == -1):#如果前一个id已经是最后一个
        donateid_now = donateids[0]
    else:
        donateid_now = donateids[donateindex + 1]
    close_index = (donateindex + 1) - donate_num
    if close_index < 0:
        close_index = len(donateids) + close_index
    close_id = donateids[close_index]
    #关闭前一个模拟器
    close_emu_id(close_id)
    #写入config
    config_write(configpath,"coc", "donateid_now", donateid_now)#只能存储str类型数据
    startport = getport(int(donateid_now))
    action = r'"D:\Program Files\DundiEmu\\DunDiEmu.exe" -multi %d -disable_audio  -fps 40' %(int(donateid_now))
    #action = r'"D:\Program Files\DundiEmu\dundi_helper.exe" --index %d --start' %(int(donateid_now))
    start(action,startport,40)
    print(r'============================= 启动捐兵模拟器完成 ===============================')
    time.sleep(3)
    coc_script(startport,10)
    time.sleep(5)
    click(pos['sure'][0], pos['sure'][1],startport)
    time.sleep(60)
    click(pos['start_script'][0],pos['start_script'][1],startport)
    print(r'============================= 启动自用捐兵脚本完成 ===============================')
    #打印分割线
    login_click(donateid_now)
    read_id = donatenames[donateid_now]
    print(r'============================= %s 实例启动完成 ===============================' %(read_id))

def start_resource(resourceid_now):
    #写入config
    config_write(configpath,"coc", "resourceid_now", resourceid_now)#只能存储str类型数据
    if int(resourceid_now) == 0:
        startport = 5555
    else:
        startport = 52550 + int(resourceid_now)
    startport = getport(int(resourceid_now))
    action = r'"D:\Program Files\DundiEmu\\DunDiEmu.exe" -multi %d -disable_audio  -fps 40' %(int(resourceid_now))
    #action = r'"D:\Program Files\DundiEmu\dundi_helper.exe" --index %d --start' %(int(resourceid_now))
    start(action,startport,40)
    print(r'============================= 启动持续打资源模拟器完成 ===============================')
    time.sleep(3)
    coc_script(startport,10)
    time.sleep(10)
    click(pos['sure'][0], pos['sure'][1],startport)
    time.sleep(60)
    click(pos['start_script'][0],pos['start_script'][1],startport,5)
    login_click(resourceid_now)
    print(r'============================= 启动持续打资源脚本完成 ===============================')
        
def play_resource(resourceids):
    #获取上一次运行的打资源id
    #global resourceid_now
    resourceid_now = config_read(configpath,"coc", "resourceid_now")#str
    flag_play_resource = config_read(configpath,"coc", "flag_play_resource")#False:切换 True：不切换一直运行
    #获取即将运行的捐兵index
    if resourceid_now in resourceids:
        try:
            resourceidindex = resourceids.index(resourceid_now)
        except:
            resourceidindex = -1
    else:
        resourceidindex = -1
    #获取即将运行的捐兵id
    if (resourceidindex == len(resourceids) - 1) or (resourceidindex == -1):#如果前一个id已经是最后一个
        resourceid_now = resourceids[0]
    else:
        resourceid_now = resourceids[resourceidindex + 1]
    close_index = (resourceidindex + 1) - resourceids_num
    if close_index < 0:
        close_index = len(resourceids) + close_index
    close_id = resourceids[close_index]
    if (len(resourceids) > resourceids_num):#如果持续打资源号数量要大于设定数量才关闭切换，不然就直接一直运行不切换了
        #关闭前一个模拟器
        close_emu_id(close_id)
        start_resource(resourceid_now)
    elif (len(resourceids) == resourceids_num) and (flag_play_resource == "False"):
        config_write(configpath,"coc", "flag_play_resource", "True")
        start_resource(resourceid_now)
    else:
        print(r'============================= 跳过持续打资源号切换 ===============================')
       
    
    
#根据时间判断运行实例数量
def instance(donate_switch,donate_status):
    # 转换字符串类型时间为datetime.date类型，这样才能做逻辑大小判断
    day_time_end = datetime.datetime.strptime(str(datetime.datetime.now().date()) + " " + day_time, '%Y-%m-%d %H:%M')
    night_time_end =  datetime.datetime.strptime(str(datetime.datetime.now().date()) + " " + night_time, '%Y-%m-%d %H:%M')
    morning_time_end =  datetime.datetime.strptime(str(datetime.datetime.now().date()) + " " + morning_time, '%Y-%m-%d %H:%M')
    # 当前时间
    now_time = datetime.datetime.now()
    # 判断当前时间是否在范围时间内
    if now_time >= night_time_end or now_time < morning_time_end:
        print('目前处于晚上,可以执行 %d 实例, %d 分钟，可以运行捐兵实例' %(instance_num_night,instance_time_night))
        #付费捐兵号(晚上运行启动)
        if donate_switch in ['True','1','T']:
            print(r'============================= 自用捐兵号运行！ ===============================')
        else:
            print('没有自用捐兵号需要运行！')
        return [instance_num_night,instance_time_night,'晚上']
    elif now_time >= morning_time_end and now_time < day_time_end:
        print('目前处于凌晨,可以执行 %d 实例, %d 分钟，不需要运行捐兵实例' %(instance_num_morning,instance_time_morning))
        return [instance_num_morning,instance_time_morning,'凌晨']
    elif now_time >= day_time_end and now_time < night_time_end:
        print('目前处于白天,可以执行%d实例,%d分钟' %(instance_num_day,instance_time_day))
        #付费捐兵号(白天运行启动)
        if donate_switch in ['True','1','T']:
            print(r'============================= 自用捐兵号开始运行！ ===============================')
        else:
            print(r'============================= 没有自用捐兵号需要运行！ ===============================')
        return [instance_num_day,instance_time_day,'白天',donate_status]

#关闭指定id窗口          
def handle_window_play(hwnd,extra):
    #关闭id
    global closeplayid
    closeplayid = startid - 6 - instance_num
    if win32gui.IsWindowVisible(hwnd):
        if closeplayid <= 0:
            closeplayid = maxid - 6 + closeplayid 
        elif closeplayid < 10:
            closeplayid = '0' + str(closeplayid)
        #关闭的id是跳过列表或者捐兵列表，递归关闭前一个id
        if str(int(closeplayid) + 6) in skipids:
            closename = resource_names[resourceid]
            closeplayid = int(closeplayid) - 1
            print(r'============================= 此关闭的轮循打资源模拟器名字 ：%s没有打开，需要向上跳过1位! ===============================' %(str(int(closeplayid) + 1)))
            win32gui.EnumWindows(handle_window_play,None)
        if str(closeplayid) in win32gui.GetWindowText(hwnd):
            print(r'============================= 关闭的轮循打资源模拟器名字为：%s ===============================' %(str(closeplayid)))
            win32gui.PostMessage(hwnd,win32con.WM_CLOSE,0,0)

#关闭模拟器列表（列表中所有）
def close_emu_all(closelist,*args):
    for close_id in closelist:
        close_name = closelist[close_id]
        # 关闭一个捐兵号
        close_windows(close_name)
        print('============================= 关闭的模拟器名字为：%s ===============================' %(close_name))
        if len(args) >0:#暂停args[0]分钟关闭
            timewait(args[0])
        
#启动模拟器（列表中所有）       
def start_emu(start_id,wait_time):
    startport = getport(int(start_id))
    action = r'"D:\Program Files\DundiEmu\\DunDiEmu.exe" -multi %d -disable_audio  -fps 40' %(int(start_id))
    #action = r'"D:\Program Files\DundiEmu\dundi_helper.exe" --index %d --start' %(int(start_id))
    start(action,startport,wait_time)
    print(r'============================= 启动实例（%d）模拟器完成 ==============================='%(int(start_id)))
    timewait(1)
    print(startport)
    coc_script(startport,5)
    time.sleep(10)
    click(pos['sure'][0], pos['sure'][1],startport)
    if int(start_id == 6):#星核多等45秒，总是卡住
        time.sleep(60)
    else:
        time.sleep(60)
    click(pos['start_script'][0],pos['start_script'][1],startport,5)
    #login_click(start_id)
    print(r'============================= 启动实例（%d）脚本完成 ==============================='%(int(start_id)))
    #if (str(start_id) in (donateids_for_paid + resourceids)) and (int(start_id) > 6):
    login_click(start_id)
    print(r'============================= 确认登录实例（%d）完成 ==============================='%(int(start_id)))
        
#依次重启模拟器（列表中所有）
def restart_emu(restartlist,*args):
    if len(args) >0:
        donateids_for_paid_2nd = args[0]
    else:
        donateids_for_paid_2nd = []
    restart_server()
    for restart_id in restartlist:
        restart_name = restartlist[restart_id]#关闭的模拟器名字
        close_window = win32gui.FindWindow(None, restart_name)
        # 关闭一个捐兵号
        try:
            win32gui.PostMessage(close_window, win32con.WM_CLOSE, 0, 0)
        except:
            print ("配额不足，无法处理，跳过！")
            pass
        if (len(donateids_for_paid_2nd) > 0) and (str(restart_id) in donateids_for_paid_2nd[0]):
            print('============================= 重启的模拟器：%s 是第二梯队的,第一梯队重启结束等待15分钟再重启 ===============================' %(restart_name))
        else:
            print('============================= 重启的模拟器名字为：%s ===============================' %(restart_name))
            #start_emu_process = Process(target=start_emu,args=(int(restart_id),60))
            #start_emu_process.start()
            start_emu(int(restart_id),30)
    if len(donateids_for_paid_2nd) > 0:
        timewait(15)#有第二梯队的号，等待15分钟后启动，和第一梯队号错开，保证第一梯队号下线时，第二梯队也能捐兵
        for restart_id in donateids_for_paid_2nd[0]:
            #start_emu_process = Process(target=start_emu,args=(int(restart_id),30))
            #start_emu_process.start()
            start_emu(int(restart_id),30)#启动第二梯队
    restart_server()

#重启打资源
def restartplay(wait_time):
    restart_server()
    #启动新一个打资源id前先关闭上一个打资源id
    '''
    try:
        close_emu_all(playnames)
    except:
        print('关闭轮循打资源号失败')
    '''
    for times in range(instance_num):
        #获取捐兵号的状态（当前是在捐兵还是在打资源）
        donate_status = config_read(configpath,"coc", "donate_status")
        #获取当前时间的参数并运行持久化运行号
        result = instance(donate_switch,donate_status)
        #现在时间段
        time_status = result[2]
        if donate_for_paid_switch in ['True','1','T'] or donate_switch in ['True','1','T']:
            if (time_status == '白天' and donate_status == 'play') or (time_status == '凌晨' and donate_status == 'donate'):#到了早上还没切换捐兵，或者到了凌晨还没切换打资源，跳过等待循环立刻切换
                break
            else:
                pass
        play(wait_time,skipids)
        wait_time += 5
        
#启动模拟器并打开脚本但是不启动脚本     
def start_emu_wait(start_id,wait_time):
    startport = getport(int(start_id))
    action = r'"D:\Program Files\DundiEmu\\DunDiEmu.exe" -multi %d -disable_audio  -fps 40' %(int(start_id))
    #action = r'"D:\Program Files\DundiEmu\dundi_helper.exe" --index %d --start' %(int(start_id))
    start(action,startport,wait_time)
    print(r'============================= 启动实例（%d）模拟器完成 ==============================='%(int(start_id)))
    timewait(1)
    print(startport)
    coc_script(startport,5)

#只点击脚本    
def start_script_wait(start_id):
    startport = getport(int(start_id))
    restart_server()
    #重启并连接连接
    connect(startport)
    time.sleep(3)
    click(pos['start_script'][0],pos['start_script'][1],startport,5)
    print(r'============================= 启动实例（%d）脚本完成 ==============================='%(int(start_id)))
    
        
#重启捐兵号
def restartdonate(rewait_ids,rewait_names):
    global donatetime_start
    # 大于4小时就关闭捐兵号，并重新启动捐兵号
    donatetime_end = datetime.datetime.now()
    starttime = donatetime_end - donatetime_start    
    if (starttime.seconds / 3600) >= (restart_time - 0.3):
        close_emu_all(rewait_names)#关闭所有重启捐兵号
        for rewait_id in rewait_ids:
            start_emu_wait(int(rewait_id),30)#启动模拟器并打开脚本但是不点击
        print(r'============================= 运行捐兵号超过4小时，下线30分钟！ ===============================')
        timewait(28)
        for rewait_id in rewait_ids:
            start_script_wait(int(rewait_id))#只点击脚本
        donatetime_start = datetime.datetime.now()
        print(r'============================= 已经下线30分钟，开始捐兵！ ===============================')

    
#开始操作
#coc
if __name__ == "__main__":
    #关闭前面的模拟器
    #close()
    #打开自动点击
    ak.start()
    #捐兵模式：一直捐兵（A)，还是半捐
    donate_mode = config_read(configpath,"coc","donate_mode")
    #跳过启动的id初始列表
    skipidlists = config_read(configpath,"coc","skipids").split()
    skipids = skipidlists.copy()
    warids = config_read(configpath,"coc", "warids").split()
    skipids.extend(warids)#添加部落战控制的id到跳过id列表中
    skipids = list(set(skipids))#去重
    #skipids = [str(x) for x in skipids]#需要把int转换成str，不然下面会报错
    for everyid in skipidlists:
        if "-" in str(everyid):
            start = everyid.split("-")[0]
            end = everyid.split("-")[1]
            #临时跳过列表,注意这里的元素是int,必须全部转换为str，不然不一致了
            skiplist = [str(x) for x in range(int(start),int(end)+1)]
            skipids.extend(skiplist)
            skipids.remove(everyid)#删除该列表
            skipids = [str(x) for x in skipids]#需要把int转换成str，不然下面会报错
            skipids = list(set(skipids))#去重

    #捐兵（一直运行）
    donate_for_paid_switch = config_read(configpath,"coc", "donate_for_paid_switch")#是否开启持续打资源
    play_resource_switch = config_read(configpath,"coc", "play_resource_switch")#是否开启持续打资源
    donate_switch = config_read(configpath,"coc", "donate_switch")#是否开启自用捐兵
    play_switch = config_read(configpath,"coc", "play_switch")#是否开启轮循打资源
    war_donate_switch = config_read(configpath,"coc", "war_donate_switch")#是否开启自动部落战捐兵
    donateids_for_paid = config_read(configpath,"coc", "donateids_for_paid").split()#获取付费捐兵id的list
    donateids = config_read(configpath,"coc", "donateids").split()#获取捐兵id的list
    levelupids = config_read(configpath,"coc", "levelupids").split()#获取9本升级id的list
    resourceids_server01 = get_resourceids("server01")
    resourceids_server02 = get_resourceids("server02")
    resourceids_server03 = get_resourceids("server03")
    #在持续打资源的list去除付费捐兵的list
    resourceids = get_resourceids(servername)#本主机的捐兵列表
    resourceids = [x for x in resourceids if x not in donateids_for_paid]
    #在捐兵列表中去除付费捐兵的list和持续打资源的list
    donateids = [x for x in donateids if (x not in donateids_for_paid) and (x not in resourceids)]
    donatenames_for_paid = {}
    try:
        for donateid_for_paid in donateids_for_paid:
            donateconfig = r'D:\Program Files\DundiEmu\DundiData\avd\dundi%s\config.ini' %(donateid_for_paid)
            with open(donateconfig,'r') as donatefile:
                configlines = donatefile.readlines()
                for configline in configlines:
                    if 'EmulatorTitleName' in configline:
                        donatename = configline.split('=')[-1].rstrip('\n')
                        donatenames_for_paid[donateid_for_paid] = donatename
        print('============================= 当前的付费捐兵号id和名字如下 ===============================\n%s' %(donatenames_for_paid))
    except:
        print('============================= 当前的付费捐兵号不全 ===============================')
    resource_names = {}
    try:
        for resourceid in resourceids:
            donateconfig = r'D:\Program Files\DundiEmu\DundiData\avd\dundi%s\config.ini' %(resourceid)
            with open(donateconfig,'r') as donatefile:
                configlines = donatefile.readlines()
                for configline in configlines:
                    if 'EmulatorTitleName' in configline:
                        donatename = configline.split('=')[-1].rstrip('\n')
                        resource_names[resourceid] = donatename
        print('============================= 当前的持续打资源号id和名字如下 ===============================\n%s' %(resource_names))
    except:
        print('============================= 当前的持续打资源号不全 ===============================')
    donatenames = {}
    try:
        for donateid in donateids:
            donateconfig = r'D:\Program Files\DundiEmu\DundiData\avd\dundi%s\config.ini' %(donateid)
            with open(donateconfig,'r') as donatefile:
                configlines = donatefile.readlines()
                for configline in configlines:
                    if 'EmulatorTitleName' in configline:
                        donatename = configline.split('=')[-1].rstrip('\n')
                        donatenames[donateid] = donatename
        print('============================= 当前的捐兵号id和名字如下 ===============================\n%s' %(donatenames))
    except:
        print('============================= 当前的自用捐兵号不全 ===============================')
    rewait_ids = [ x for x in QQlists if x in donateids_for_paid ]#获取重启的模拟器id列表
    rewait_names = {}
    try:
        for rewait_id in rewait_ids:
            donateconfig = r'D:\Program Files\DundiEmu\DundiData\avd\dundi%s\config.ini' %(rewait_id)
            with open(donateconfig,'r') as donatefile:
                configlines = donatefile.readlines()
                for configline in configlines:
                    if 'EmulatorTitleName' in configline:
                        donatename = configline.split('=')[-1].rstrip('\n')
                        rewait_names[rewait_id] = donatename
        print('============================= 当前的重启号id和名字如下 ===============================\n%s' %(rewait_names))
    except:
        print('============================= 当前的重启号不全 ===============================')

    #查看捐兵号的开关是否打开，打开就跳过该id
    skipids.extend(donateids_for_paid)#添加捐兵的id到跳过id列表中
    skipids.extend(donateids)#添加捐兵的id到跳过id列表中
    skipids.extend(levelupids)#添加9本升级的id到跳过id列表中
    skipids.extend(resourceids_server01)#添加持续打资源的id到跳过id列表中
    skipids.extend(resourceids_server02)#添加持续打资源的id到跳过id列表中
    skipids.extend(resourceids_server03)#添加持续打资源的id到跳过id列表中
    skipids = list(set(skipids))#去重
    skipids.sort()
    print('============================= 跳过的实例id如下 ===============================\n%s' %(skipids))

    playnames = {}
    notplaylist = []
    notplaylist.extend(donateids)
    notplaylist.extend(donateids_for_paid)
    notplaylist.extend(resourceids)
    notplaylist.extend(skipids)
    notplaylist = list(set(notplaylist))#去重
    try:
        for playid in range(maxid + 1):
            if str(playid) not in notplaylist:
                playconfig = r'D:\Program Files\DundiEmu\DundiData\avd\dundi%d\config.ini' %(playid)
                '''
                with open(playconfig,'r') as playfile:
                    print(playid)
                    configlines = playfile.readlines()
                '''
                configlines = readFile(playconfig)
                for configline in configlines:
                    if 'EmulatorTitleName' in configline:
                        playname = configline.split('=')[-1].rstrip('\n')
                        playnames[playid] = playname
        play_ids = list(playnames.keys())
        print('============================= 当前的打资源号和名字如下: ===============================\n%s' %(playnames))
    except FileNotFoundError as reason:
        print('============================= 当前的打资源号不全:%s ===============================' %(reason))
    #白天和夜晚运行的实例数量和时间
    instance_num_day = int(config_read(configpath,"coc", "instance_num_day"))
    instance_time_day = float(config_read(configpath,"coc", "instance_time_day"))
    instance_num_night = int(config_read(configpath,"coc", "instance_num_night"))
    instance_time_night = float(config_read(configpath,"coc", "instance_time_night"))
    instance_num_morning = int(config_read(configpath,"coc", "instance_num_morning"))
    instance_time_morning = float(config_read(configpath,"coc", "instance_time_morning"))
    #获取时间段
    day_time = config_read(configpath,"coc", "day_time")
    night_time = config_read(configpath,"coc", "night_time")
    morning_time = config_read(configpath,"coc", "morning_time")
    #获取当前时间判断启动持续时间
    donatetime_start = datetime.datetime.now()
    # 获取捐兵号的状态（当前是在捐兵还是在打资源）
    donate_status = config_read(configpath,"coc", "donate_status")
    result = instance(donate_switch,donate_status)
    #获取付费捐兵号数量
    if donate_for_paid_switch in ['True','1','T']:
        donateids_for_paid_num = len(donateids_for_paid)
    else:
        donateids_for_paid_num = 0
    #时间段
    time_status = result[2]
    if play_resource_switch in ['True','1','T']:
        #获取持续打资源id的list
        resourceids_num = int(config_read(configpath,"coc", "resourceids_num"))#打资源号的个数
    elif play_resource_switch in ['False','0','F']:
        resourceids_num = 0
    #获取重启模拟器时间（小时）
    restart_time = int(config_read(configpath,"coc", "restart_time"))
    #切换重启状态为'F'，表示已经过了那个重启的时间，把状态归零
    restart_status = 'F'
    #第一次启动时间
    starttime_global = datetime.datetime.now()
    #获取付费捐兵号第二梯队列表
    donateids_for_paid_2nd = config_read(configpath,"coc", "donateids_for_paid_2nd").split()
    #首次运行打开付费捐兵号
    if ((time_status != '凌晨') and (donate_status == 'donate')) or ((time_status == '凌晨') and (donate_status == 'play')):
        #启动付费捐兵号
        kill_adb()
        if donate_for_paid_switch in ['True','1','T']:
            restart_emu(donatenames_for_paid,donateids_for_paid_2nd)#启动了第二梯队
        #启动持续打资源号
        if play_resource_switch in ['True','1','T']:
            config_write(configpath,"coc", "flag_play_resource", "False")
            if resourceids_num != 0:
                for n in range(resourceids_num):
                    try:
                        play_resource(resourceids)
                    except IndexError as reason:
                        print(reason)
                        continue
            
    while True:
        kill_adb()
        endtime_global = datetime.datetime.now()
        runtime_global = endtime_global - starttime_global
        #每隔一段时间重启一次
        runtime_hours = int(runtime_global.total_seconds() / 3600)
        runtime_days = int(runtime_hours / 24)
        if (runtime_hours != 0) and ((runtime_hours % restart_time) == 0) and (restart_status == 'F'):
            if donate_for_paid_switch in ['True','1','T']:
                print(r'============================= 当前脚本每运行 %d 小时，全部模拟器重启一次! =============================' %(restart_time))
                restart_status = 'T'#切换重启状态为'T'，表示已经重启过了，在这个小时内不要再重启了
                #close_emu_all(donatenames_for_paid)
                #relax_time = 30 - (len(donatenames_for_paid) * 2)
                #relax_time = 30#休息半小时
                #timewait(relax_time)
                #restart_emu(donatenames_for_paid)#只重启付费捐兵号
                for start_id in donateids_for_paid:
                    if (str(start_id) in (donateids_for_paid + resourceids)) and (int(start_id) > 6):
                        login_click(start_id)
                    print(r'============================= 确认登录实例（%d）完成 ==============================='%(int(start_id)))
        elif (runtime_hours != 0) and ((runtime_hours % restart_time) != 0) and (restart_status == 'T'):
            restart_status = 'F'#切换重启状态为'F'，表示已经过了那个重启的时间，把状态归零
        print(r'============================= 当前脚本已运行 %d 天 %d 个小时! =============================' %(runtime_days , (runtime_hours - runtime_days*24)))
        if runtime_days >= 7:
            with open(Coclog,'a') as Coclogfile:
                Coclogfile.write('============================= 运行时间超过 %d 天重启主机,重启时间：%s =============================\n' %(runtime_days , time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            reboot()
        #获取捐兵号的状态（当前是在捐兵还是在打资源）
        donate_status = config_read(configpath,"coc", "donate_status")
        #关闭
        #close()
        #获取当前时间的参数并运行持久化运行号
        result = instance(donate_switch,donate_status)
        #启动打资源的模拟器个数
        instance_num = result[0]
        '''
        if donate_switch in ['True','1','T']:
            if instance_num < donate_num:
                instance_num = 0
            else:
        '''
        #等待时间
        instance_time = result[1]
        #现在时间段
        time_status = result[2]
        #获取捐兵的数量
        if time_status == "凌晨":
            if donate_mode == "A":
                donate_num = len(donateids)
            elif donate_switch in ['True','1','T']:
                donate_num = int(config_read(configpath,"coc", "donate_num_morning"))#捐兵号的个数
            elif donate_switch == "F":
                donate_num = 0
        else:
            if donate_mode == "A":
                donate_num = len(donateids)
            elif donate_switch in ['True','1','T']:
                donate_num = int(config_read(configpath,"coc", "donate_num"))#捐兵号的个数
            elif donate_switch not in ['True','1','T']:
                donate_num = 0
        instance_num = instance_num - donate_num - donateids_for_paid_num - resourceids_num
        #凌晨切换捐兵状态为打资源，备份Config.ini配置文件
        if (time_status == '凌晨') and (donate_status == 'donate'):
            fc.copy_file("Config.ini",configdir,backupdir)#备份
            flag_reboot = 'False'#设置flag为FALSE
            config_write(configpath,"coc", "flag_reboot", flag_reboot)#只能存储str类型数据，设置flag为FALSE
            close()#关闭所有模拟器、adb
            restart_server()
            #启动持续打资源号
            if play_resource_switch in ['True','1','T']:
                if resourceids_num != 0:
                    config_write(configpath,"coc", "flag_play_resource", "False")
                    for n in range(resourceids_num):
                        try:
                            play_resource(resourceids)
                        except IndexError as reason:
                            print(reason)
                            continue
                restart_server()
            with open(Coclog,'a') as Coclogfile:
                Coclogfile.write('凌晨切换捐兵状态为打资源,切换开始时间：%s\n' %(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            if donate_for_paid_switch in ['True','1','T']:
                for convert_id in donateids_for_paid:
                    coc_template.convert_mode(convert_id,donate_status)
                restart_server()
            if play_resource_switch in ['True','1','T']:
                for convert_id in resourceids:
                    coc_template.convert_mode(convert_id,donate_status)
                #restart_emu(resource_names)#启动一下持续打资源号
            if donate_switch in ['True','1','T']:
                for convert_id in donateids:
                    coc_template.convert_mode(convert_id,donate_status)
            with open(Coclog,'a') as Coclogfile:
                Coclogfile.write('凌晨切换捐兵状态为打资源,切换完成时间：%s\n' %(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            donate_status = 'play'
            config_write(configpath,"coc", "donate_status", donate_status)#只能存储str类型数据
            #部落战捐兵
            if war_donate_switch in ['True', '1', 'T']:
                coc_template.wardonate(warids)
            if donate_for_paid_switch in ['True','1','T']:
                restart_emu(donatenames_for_paid)#只重启付费捐兵号
        #早晨关机休息
        elif (time_status != '凌晨') and (donate_status == 'play'):
            flag_reboot = config_read(configpath,"coc", "flag_reboot")#获取重启flag
            if flag_reboot not in ['True','1','T']:
                flag_reboot = 'True'
                config_write(configpath,"coc", "flag_reboot", flag_reboot)#只能存储str类型数据，设置flag为True
                #reboot()#重启
                shutdown()#关机，必须配合自动开机功能使用
            elif flag_reboot in ['True','1','T']:
                with open(Coclog,'a') as Coclogfile:
                    Coclogfile.write('早上切换打资源状态为捐兵,切换开始时间：%s\n' %(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
                close_emu_all(donatenames_for_paid)#关闭所有付费捐兵号
                close_emu_all(donatenames)#关闭所有自用捐兵号
                #print(r'============================= 等待30分钟避免切换时没有授权导致切换失败 ===============================')
                #timewait(30)#等待30分钟避免启动时没有授权登录
            #启动持续打资源号
            if play_resource_switch in ['True','1','T']:
                if resourceids_num != 0:
                    config_write(configpath,"coc", "flag_play_resource", "False")
                    for n in range(resourceids_num):
                        try:
                            play_resource(resourceids)
                        except IndexError as reason:
                            print(reason)
                            continue
                restart_server()
            #早上切换打资源状态为捐兵
            if donate_for_paid_switch in ['True','1','T']:
                for convert_id in donateids_for_paid:
                    action = r'"D:\Program Files\DundiEmu\\DunDiEmu.exe" -multi %d -disable_audio  -fps 40' % (int(convert_id))
                    #action = r'"D:\Program Files\DundiEmu\dundi_helper.exe" --index %d --start' % (int(convert_id))
                    start_emu_convert(action, convert_id, 40)#启动
                    startport = getport(convert_id)
                    coc_template.start_script(startport,'donate')#切换
                    if convert_id == donateids_for_paid[-1]:#最后一个模拟器等待3分钟避免切换的时候刚好被打导致切换失败
                        timewait(3)
                        click(pos['cancel'][0], pos['cancel'][1],startport)
                        time.sleep(30)
                        close_emu_all(donatenames_for_paid)#关闭所有付费捐兵号
                    #close_emu_id(convert_id)#关闭模拟器
                for convert_id in donateids_for_paid:
                    coc_template.convert_mode(convert_id,donate_status)#删除兵+造兵
                restart_server()
            #早上切换打资源状态为捐兵
            if donate_switch in ['True','1','T']:
                try:
                    if datetime.datetime.now().weekday() in [0,1,2,3,4,5,6]:#所有时间捐兵，如果要打资源取消时间即可，0是周一，6是周日
                        for convert_id in donateids:
                            action = r'"D:\Program Files\DundiEmu\\DunDiEmu.exe" -multi %d -disable_audio  -fps 40' % (int(convert_id))
                            #action = r'"D:\Program Files\DundiEmu\dundi_helper.exe" --index %d --start' % (int(convert_id))
                            start_emu_convert(action, convert_id, 40)#启动
                            startport = getport(convert_id)
                            coc_template.start_script(startport,'donate')#切换
                            if convert_id == donateids[-1]:#最后一个模拟器等待3分钟避免切换的时候刚好被打导致切换失败
                                timewait(3)
                                click(pos['cancel'][0], pos['cancel'][1],startport)
                                time.sleep(30)
                                close_emu_all(donatenames)#关闭所有付费捐兵号
                            #close_emu_id(convert_id)#关闭模拟器
                        for convert_id in donateids:
                            coc_template.convert_mode(convert_id,donate_status)#删除兵+造兵
                        restart_server()
                except:
                        print('============================= 出故障，不捐兵，继续打资源 =============================')
            #点击中间关闭adb.exe弹出的错误按钮
            #for n in range(15):
                #k.mouse_click(894, 544)
            with open(Coclog,'a') as Coclogfile:
                Coclogfile.write('============================= 早上切换打资源状态为捐兵,切换完成时间：%s =============================\n' %(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            donate_status = 'donate'
            config_write(configpath,"coc", "donate_status", donate_status)#只能存储str类型数据
            if donate_for_paid_switch in ['True','1','T']:
                restart_emu(donatenames_for_paid,donateids_for_paid_2nd)#只重启付费捐兵号
        #关闭持续打资源号
        #close_emu_all(resource_names)
        #启动持续打资源号
        if play_resource_switch in ['True','1','T']:
            if resourceids_num != 0:
                config_write(configpath,"coc", "flag_play_resource", "False")
                for n in range(resourceids_num):
                    try:
                        play_resource(resourceids)
                    except IndexError as reason:
                        print(reason)
                        continue
            restart_server()
        #启动捐兵号
        if donate_switch in ['True','1','T']:
            #关闭自用捐兵号
            #close_emu_all(donatenames)
            if donate_num != 0:
                for n in range(donate_num):
                    try:
                        play_donate(donateids)
                    except IndexError as reason:
                        print(reason)
                        continue
            restart_server()
        if play_switch in ['True','1','T']:
            #启动打资源号
            restartplay(90)

        #确认登录捐兵号，点击登录按钮
        logincheck_lists = [ x for x in donateids_for_paid ]
        for logincheckid in logincheck_lists:
            login_click(logincheckid)
            
        #运行该coc实例时间
        t = int(instance_time)
        for time_minite in range(t,0,-1):
            print('============================= 进入等待,还剩 %d 分钟 =============================' %(time_minite))
            #获取捐兵号的状态（当前是在捐兵还是在打资源）
            donate_status = config_read(configpath,"coc", "donate_status")
            #获取当前时间的参数并运行持久化运行号
            result = instance(donate_switch,donate_status)
            #现在时间段
            time_status = result[2]
            if donate_for_paid_switch in ['True','1','T'] or donate_switch in ['True','1','T']:
                restartdonate(rewait_ids,rewait_names)#4小时强制下线
                if (time_status == '白天' and donate_status == 'play') or (time_status == '凌晨' and donate_status == 'donate'):#到了早上还没切换捐兵，或者到了凌晨还没切换打资源，跳过等待循环立刻切换
                    break
                else:
                    pass
                timewait(1)
        restart_server()


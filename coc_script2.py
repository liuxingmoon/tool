#coding:utf-8
import subprocess
import time
import easygui as g
import re
import configparser
import win32gui
import datetime

#元素坐标
pos = {
  'coc_script':[500,680],
  'start_script':[200,1070],
  'sure':[360,935],
  'cancel': [1200, 350],
  'exitstore': [1230, 50],
  'script_item3':[430,260],
  'script_item3_click':[360,510],
  'script_donateTowar':[360,550],
  'script_warTodonate':[360,650],
  'trainning': [54, 524],
  'trainningitem1': [150, 45],
  'trainning_remove_trp1': [141, 230],
  'trainning_remove_trp2': [241, 230],
  'trainning_remove_trp3': [341, 230],
  'trainning_remove_trp4': [441, 230],
  'trainning_editarmy': [1140, 590],
  'trainning_sureremove': [1140, 650],
  'trainning_sureremove_enter': [785, 465],
  'trainningitem2': [370, 45],
  'trainningitem2_remove': [1200, 135],
  'trainningitem3': [590, 45],
  'trainningitem4': [810, 45],
  'trainningitem5': [1050, 45],
  'trainning_ALL1': [1135, 330],
  'train_troop01': [130, 440]
  }
#日志路径
Coclog = r'C:\Users\Administrator\Desktop\刘兴\coc\coclog.txt'


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
    print('启动模拟器完成')
    '''
    if result.split()[0] == b'unable':
        close()
    '''

def home(startport):
    process = subprocess.Popen('adb -s 127.0.0.1:%s shell input keyevent 3' % (startport), shell=True)
    time.sleep(3)

#启动coc
def startcoc(startport):
    subprocess.Popen(r'adb -s 127.0.0.1:%d shell am start -n com.supercell.clashofclans.uc/com.supercell.titan.kunlun.uc.GameAppKunlunUC' % (startport), shell=True)
    time.sleep(30)

#打开黑松鼠
def coc_script(startid,startport,*args):
    subprocess.Popen(r'adb -s 127.0.0.1:%d shell am start -n com.ais.foxsquirrel.coc/ui.activity.SplashActivity' %(startport),shell=True)
    time.sleep(12)
    #点击更新内容
    click(pos['sure'][0], pos['sure'][1],startport)
    time.sleep(3)
    #根据选项选择是否切换
    for event in args:
        if event == 0:#0代表从捐兵转换为打资源
            click(pos['script_item3'][0],pos['script_item3'][1],startport)
            click(pos['script_item3_click'][0],pos['script_item3_click'][1],startport)
            click(pos['script_donateTowar'][0],pos['script_donateTowar'][1],startport)
        elif event == 1:#0代表从打资源转换为捐兵
            click(pos['script_item3'][0],pos['script_item3'][1],startport)
            click(pos['script_item3_click'][0],pos['script_item3_click'][1],startport)
            click(pos['script_warTodonate'][0],pos['script_warTodonate'][1],startport)
    #点击开始运行
    click(pos['start_script'][0],pos['start_script'][1],startport)
    print('启动脚本完成')
    #打印分割线
    read_id = int(startid)
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
    
#点击屏幕
def click(x,y,startport):
    subprocess.Popen(r'adb -s 127.0.0.1:%d shell input tap %d %d' %(startport,x,y),shell=True)
    time.sleep(3)

# 快速点击屏幕
def click_short(x,y,startport,times):
    for n in range(times):
        subprocess.Popen(r'adb -s 127.0.0.1:%d shell input tap %d %d' %(startport,x,y),shell=True)
        time.sleep(0.1)
        print(x,y)
def close():
    subprocess.Popen('taskkill /f /t /im DunDiEmu.exe',shell=True)
    time.sleep(3)

def getport(startid,skipids):
    #获取启动端口
    if startid == 0:
        startport = 5555
        return [startid,startport]
    #skipids
    elif str(startid) in skipids:
        #如果恰好既是最后一个id，又是要跳过的id，需要直接循环为初始id
        if startid == maxid:
            startid = minid
        else:
            print(r'该模拟器id %d 在禁止启动名单之中，跳过!' %(startid))
            startid += 1
        return getport(startid,skipids)#递归获取port
    else:
        startport = 52550 + startid
        return [startid,startport]

def play(wait_time,skipids):
    # 参数获取
    #config = configparser.ConfigParser()
    #config.read("Config.ini", encoding="utf-8")
    startid = config.get("coc", "startid")
    startid = int(startid)#取出数据为string
    startlist = getport(startid,skipids)
    startid = int(startlist[0])#获取启动模拟器id
    startport = startlist[1]#获取port
    action = r'"D:\Program Files\DundiEmu\DunDiEmu.exe" -multi %d -disable_audio  -fps 40' %(startid)
    start(action,startport,wait_time)
    coc_script(startid,startport)
    #回滚startid
    if startid == maxid:   #结束id
        startid = minid-1   #开始id - 1
    config.set("coc", "startid", str(startid + 1))#只能存储str类型数据
    config.write(open("Config.ini", "w",encoding='utf-8'))  # 保存到Config.ini


#捐兵号
def play_donate(donateid,*args):
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
    config.write(open("Config.ini", "w",encoding='utf-8'))  # 保存到Config.ini
    startport = 52550 + int(donateid_now)
    action = r'"D:\Program Files\DundiEmu\DunDiEmu.exe" -multi %d -disable_audio  -fps 40' %(int(donateid_now))
    start(action,startport,3)
    for event in args:
        if event == 0:
            coc_script(donateid_now, startport, 0)  # 0代表从捐兵转换为打资源
            # 关闭模拟器
            close()
        elif event == 1:
            #启动部落冲突
            startcoc(startport)
            #删除正在训练的兵
            click(pos['trainning'][0], pos['trainning'][1], startport)
            click(pos['trainningitem2'][0], pos['trainningitem2'][1], startport)
            click_short(pos['trainningitem2_remove'][0], pos['trainningitem2_remove'][1], startport,300)
            #删除法术
            click(pos['trainningitem3'][0], pos['trainningitem3'][1], startport)
            click_short(pos['trainningitem2_remove'][0], pos['trainningitem2_remove'][1], startport, 11)
            #删除兵营的兵
            '''
            click(pos['trainningitem1'][0], pos['trainningitem1'][1], startport)
            click(pos['trainning_editarmy'][0],pos['trainning_editarmy'][1],startport)
            click_short(pos['trainning_remove_trp1'][0],pos['trainning_remove_trp1'][1],startport,50)
            click_short(pos['trainning_remove_trp2'][0],pos['trainning_remove_trp2'][1],startport,180)
            click_short(pos['trainning_remove_trp3'][0],pos['trainning_remove_trp3'][1],startport,30)
            click_short(pos['trainning_remove_trp4'][0],pos['trainning_remove_trp4'][1],startport,20)
            click(pos['trainning_sureremove'][0], pos['trainning_sureremove'][1], startport)
            click(pos['trainning_sureremove_enter'][0], pos['trainning_sureremove_enter'][1], startport)
            '''
            #一键训练
            if int(donateid_now) in [1,5]:
                click(pos['trainningitem5'][0], pos['trainningitem5'][1], startport)
            else:
                click(pos['trainningitem4'][0], pos['trainningitem4'][1], startport)
            click(pos['trainning_ALL1'][0], pos['trainning_ALL1'][1], startport)
            #退出
            home(startport)
            # 1代表从打资源转换为捐兵
            coc_script(donateid_now, startport, 1)
            # 关闭模拟器
            close()
        else:
            coc_script(donateid_now,startport)


#根据时间判断运行实例数量
def instance(donate_switch,donateid):
    # 转换字符串类型时间为datetime.date类型，这样才能做逻辑大小判断
    day_time_end = datetime.datetime.strptime(str(datetime.datetime.now().date()) + " " + day_time, '%Y-%m-%d %H:%M')
    night_time_end =  datetime.datetime.strptime(str(datetime.datetime.now().date()) + " " + night_time, '%Y-%m-%d %H:%M')
    morning_time_end =  datetime.datetime.strptime(str(datetime.datetime.now().date()) + " " + morning_time, '%Y-%m-%d %H:%M')
    donate_status = config.get("coc", "donate_status")  # 是否捐兵打资源切换
    # 当前时间
    now_time = datetime.datetime.now()
    # 判断当前时间是否在范围时间内
    if now_time >= day_time_end and now_time < night_time_end:
        print('目前处于晚上,可以执行 %d 实例, %d 分钟，可以运行捐兵实例' %(instance_num_night,instance_time_night*60))
        #付费捐兵号(晚上运行启动)
        if donate_switch in ['True','1','T']:
            print('持久运行号开始运行！')
            for n in range(donate_num):
                play_donate(donateid)
        else:
            print('没有持久运行号需要运行！')
        return [instance_num_night,instance_time_night,'晚上']
    elif (now_time >= night_time_end) and (now_time < morning_time_end):
        if donate_status in ['True','1','T']:#切换为打资源状态
            print('目前处于凌晨,可以执行 %d 实例, %d 分钟，切换为打资源' %(instance_num_night,instance_time_night*60))
            #转换为打资源
            for n in range(len(donateid)):
                play_donate(donateid,0)# 0代表从捐兵转换为打资源
            config.set("coc", "donate_status", "T")  # 只能存储str类型数据
            config.write(open("Config.ini", "w", encoding='utf-8'))  # 保存到Config.ini
        else:
            print('目前处于凌晨,可以执行 %d 实例, %d 分钟，打资源' % (instance_num_night, instance_time_night * 60))
            for n in range(donate_num):
                play_donate(donateid)
        return [instance_num_night,instance_time_night,'凌晨']

    else:
        if donate_status not in ['True','1','T']:#切换为捐兵状态
            print('目前处于白天,可以执行%d实例,%d分钟，切换为捐兵' % (instance_num_day, instance_time_day * 60))
            #转换为捐兵
            for n in range(len(donateid)):
                play_donate(donateid, 1)  # 1代表从打资源转换为捐兵
            config.set("coc", "donate_status", "F")  # 只能存储str类型数据
            config.write(open("Config.ini", "w", encoding='utf-8'))  # 保存到Config.ini
            #开始打资源
            print('持久运行号开始运行！')
            for n in range(donate_num):
                play_donate(donateid)
        else:
            print('目前处于白天,可以执行%d实例,%d分钟' %(instance_num_day,instance_time_day*60))
            #付费捐兵号(白天运行启动)
            if donate_switch in ['True','1','T']:
                print('持久运行号开始运行！')
                for n in range(donate_num):
                    play_donate(donateid)
            else:
                print('没有持久运行号需要运行！')
        return [instance_num_day,instance_time_day,'白天']

#开始操作
#coc
if __name__ == "__main__":
    #获取配置文件参数skipid,donateid,instance_num,instance_time
    config = configparser.ConfigParser()
    config.read("Config.ini", encoding="utf-8")
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
    #获取时间段
    day_time = config.get("coc", "day_time")
    night_time = config.get("coc", "night_time")
    morning_time = config.get("coc", "morning_time")
    
    while True:
        #获取当前时间的参数并运行持久化运行号
        result = instance(donate_switch,donateid)
        #启动打资源的模拟器个数
        instance_num = result[0]
        if result[2] != '凌晨':
            if donate_switch in ['True','1','T']:
                if instance_num < donate_num:
                    instance_num = 0
                else:
                    instance_num = instance_num - donate_num
        #等待时间
        instance_time = result[1]
        #同时运行几个实例
        wait_time = 3
        for times in range(instance_num):
            play(wait_time,skipids)
            wait_time += 1
        #运行该coc实例时间
        t = int(3600*instance_time)
        time.sleep(t)
        #关闭
        close()


#coding:utf-8
import subprocess
import time
import win32gui
from win32.lib import win32con
from config_ctrl import *
from read_config import configpath

QQlists = config_read(configpath,"coc", "QQlists").split()
baidulists = config_read(configpath,"coc", "baidulists").split()


#元素坐标
pos = {
    'coc_script':[500,680],
    'start_script':[200,1070],
    'sure':[360,935],
    'pointleft': [149, 456],
    'pointtop': [622, 100],
    'pointtop_continue': [736, 188],
    'pointright': [1090, 475],
    'pointbot': [658, 525],
    'pointbot_continue': [793, 424],
    'action': [640, 590],
    'cancel': [1200, 50],
    'exitstore': [1230, 50],
    'name': [640, 325],
    'name_done': [640, 235],
    'alias_name': [640, 510],
    'idcard': [640, 470],
    'agree1': [365, 110],
    'agree2': [640, 170],
    'register': [760, 545],
    'store': [1200, 635],
    'relogin': [500, 825],
    'login_wandoujia': [640, 500],
    'login_wandoujia1': [640, 300],
    'login_wandoujia2': [640, 500],
    'login_kunlun': [640, 250],
    'login_kunlun1': [1000, 300],
    'login_kunlun2': [650, 200],
    'login_kunlun3': [1000, 300],
    'login_baidu1': [440, 545],
    'login_baidu2': [500, 460],
    'store_build': [300, 100],
    'storeitem1': [330, 260],
    'storeitem2': [540, 260],
    'storeitem3': [750, 260],
    'storeitem4': [960, 260],
    'store_1': [200, 440],
    'store_2': [420, 440],
    'store_3': [640, 440],
    'store_4': [860, 440],
    'store_5': [1080, 440],
    'built01': [570, 235],
    'built02': [725, 580],
    'built03': [465, 460],
    'built04': [695, 140],
    'built05': [600, 350],
    'built06': [880, 230],
    'built07': [565, 100],
    'built08': [470, 300],
    'built09': [700, 280],
    'built10': [570, 320],
    'built11': [820, 320],
    'built12': [730, 390],
    'built13': [440, 270],
    'built14': [710, 195],
    'built15': [643, 416],
    'built16': [770, 310],
    'built17': [430, 105],
    'built18': [370, 230],
    'built19': [935, 420],
    'built20': [1035, 160],
    'built21': [1160, 215],
    'built22': [370, 370],
    'built23': [970, 360],
    'built24': [610, 220],
    'backcamp': [640, 640],
    'camp': [420, 420],
    'ruins': [850, 220],
    'base': [640, 380],
    'base2': [630, 325],
    'sure': [360, 935],
    'levelup': [715, 600],
    'levelup2': [615, 600],
    'enter': [640, 630],
    'war': [50, 440],
    'war_1': [360, 280],
    'war_2': [590, 320],
    'war_donate': [480, 550],
    'war_donate_last': [340, 570],
    'war_donate_next': [950, 570],
    'war_donate_trp1': [310, 170],
    'war_donate_trp2': [400, 170],
    'war_donate_trp3': [490, 170],
    'war_donate_trp4': [580, 170],
    'trainning_bt': [700, 600],
    'trainning': [54, 524],
    'trainningitem1': [150, 45],
    'trainningitem2': [370, 45],
    'trainningitem3': [590, 45],
    'trainningitem4': [810, 45],
    'trainningitem5': [1030, 45],
    'train_troop01': [130, 440],
    'train_troop02': [260, 440],
    'train_troop03': [390, 440],
    'train_troop04': [520, 440],
    'train_troop05': [650, 440],
    'train_troop06': [780, 440],
    'train_troop07': [910, 440],
    'train_troop08': [1060, 440],
    'train_troop11': [130, 580],
    'train_troop12': [260, 580],
    'train_troop13': [390, 580],
    'train_troop14': [520, 580],
    'train_troop15': [650, 580],
    'train_troop16': [780, 580],
    'train_troop17': [910, 580],
    'train_troop18': [1060, 580],
    'train_template00': [1130, 180],
    'train_template01': [1130, 330],
    'train_template02': [1130, 480],
    'train_template03': [1130, 630],
    'train_siege_unit01': [180, 500],
    'train_siege_unit02': [410, 500],
    'train_siege_unit03': [650, 500],
    'train_siege_unit04': [880, 500],
    'attack_troop01': [200, 655],
    'attack_troop02': [300, 655],
    'attack_troop03': [400, 655],
    'attack_troop04': [500, 655],
    'attack_troop05': [600, 655],
    'attack': [100, 650],
    'attack_single': [170, 350],
    'goblin01': [850, 470],
    'goblin02': [1080, 475],
    'goblin03': [865, 475],
    'goblin01_point': [550, 300],
    'goblin02_point1': [670, 337],
    'goblin02_point2': [766, 265],
    'goblin03_point': [988, 552],
    'achievement': [50, 50],
    'achievement1': [1040, 170],
    'achievement2': [1040, 260],
    'achievement3': [1040, 350],
    'achievement4': [1040, 440],
    'achievement5': [1040, 520],
    'achievement6': [1040, 610],
    '2levelup': [713, 593],
    '3levelup': [640, 600],
    '4levelup': [714, 592],
    'mine1': [735, 180],
    'mine2': [735, 520],
    'mine3': [800, 450],
    'collector1': [500, 380],
    'collector2': [470, 500],
    'train1': [380, 320],
    'train2': [600, 440],
    'gold1': [470, 130],
    'water1': [790, 280],
    'rmtree': [640, 590],
    'script_start':[200,1070],
    'script_item1': [130, 290],
    'script_item2': [280, 290],
    'script_item3': [430, 290],
    'script_item4': [590, 290],
    'script_canceltroop': [1200, 135],
    'script_switch_mode': [340, 610],
    'script_swipetop': [340, 740],
    'script_swipebot': [340, 1000],
    'script_night_attackmode': [425, 780],
    'script_night_attackmode_no': [425, 840],
    'script_night_attackmode_prize': [425, 900],
    'script_night_attackmode_alltime': [425, 970],
    'script_night_auto_collect': [250, 610],
    'script_night_Accelerate_tower': [450, 610],
    'script_night_wait_rebot': [250, 660],
    'script_night_auto_weeding': [450, 660],
    'script_night_auto_levelup': [270, 715],
    'script_night_auto_research': [480, 715],
    'boat': [800, 300],
    'script_play': [340, 660],
    'script_donate': [340, 800],
    'edit_army': [1135, 585],
    'del_army': [1135, 650],
    'del_army_sure': [780, 470],
    'del_army_trp01': [110, 200],
    'del_army_trp02': [210, 200],
    'del_army_trp03': [310, 200],
    'del_army_trp04': [410, 200],
    'del_army_trp05': [510, 200],
    'del_army_trp06': [610, 200],
    'del_army_trp07': [710, 200],
    'del_army_trp08': [810, 200],
    'del_army_pt01': [110, 400],
    'del_army_pt02': [210, 400],
    'del_army_pt03': [310, 400],
    'del_army_pt04': [410, 400],
    'del_army_pt05': [510, 400],
    'del_army_pt06': [610, 400],
    'del_army_pt07': [710, 400]

}

QQ1 = r'"D:\Program Files\DundiEmu\DunDiEmu.exe" -multi 0 -disable_audio  -fps 40'
QQ2 = r'"D:\Program Files\DundiEmu\DunDiEmu.exe" -multi 1 -disable_audio  -fps 40'
QQ3 = r'"D:\Program Files\DundiEmu\DunDiEmu.exe" -multi 2 -disable_audio  -fps 40'
QQ4 = r'"D:\Program Files\DundiEmu\DunDiEmu.exe" -multi 3 -disable_audio  -fps 40'
QQ5 = r'"D:\Program Files\DundiEmu\DunDiEmu.exe" -multi 4 -disable_audio  -fps 40'

#获取启动port
def getport(startid):
    startid = int(startid)
    #获取启动端口
    if startid == 0:
        startport = 5555
        return startport
    else:
        startport = 52550 + int(startid)
        return startport

#获取启动id
def getid(startport):
    startport = int(startport)
    #获取启动端口
    if startport == 5555:
        startid = 0
        return startid
    else:
        startid = startport - 52550
        return startid
        
# 连接模拟器
def connect(startport):
    if startport == 5555:
        subprocess.Popen(r'adb connect 127.0.0.1:%d' %(startport),shell = True)
    else:
        result = subprocess.Popen(r'adb connect 127.0.0.1:%d' %(startport),shell = True,stdout=subprocess.PIPE)
        text = result.stdout.readlines()
        try:
            if ('unable to connect to' in str(text[0])) or ('offline' in str(text[0])):
                print('连接失败，重启虚拟机后重连')
                close_id = getid(startport)
                close_emu_id(close_id)#关闭
                restart_server()
                action = r'"D:\Program Files\DundiEmu\DunDiEmu.exe" -multi %s -disable_audio  -fps 40' %(close_id)
                #action = r'"D:\Program Files\DundiEmu\dundi_helper.exe" --index %d --start' %(close_id)
                start_emu_id(action,close_id)#启动     
                connect(startport)#递归获取一下启动port
        except:
            pass
            
            
#根据字典值获取索引
def get_keys(dict, value):
     temp = [k for k,v in dict.items() if v == value]
     return temp[0]
# 结束
def finish(startport):
    process = subprocess.Popen('adb disconnect %s' % (startport), shell=True)
    time.sleep(3)
# 点击屏幕
def click(x,y,startport,*args):
    subprocess.Popen(r'adb -s 127.0.0.1:%d shell input tap %d %d' %(startport,x,y),shell=True)
    print(x,y)
    time.sleep(3)
    if len(args) > 0:
        time.sleep(args[0])
# 快速点击屏幕
def click_short(x,y,startport,times):
    for n in range(times):
        process = subprocess.Popen(r'adb -s 127.0.0.1:%d shell input tap %d %d' %(startport,x,y),shell=True)
        time.sleep(0.1)
        print(x,y)
        
# 慢速多次点击屏幕
def click_mid(x,y,startport,times):
    for n in range(times):
        process = subprocess.Popen(r'adb -s 127.0.0.1:%d shell input tap %d %d' %(startport,x,y),shell=True)
        time.sleep(2)
        print(x,y)
        
#长按屏幕
def click_long(x,y,time,startport):
    process = subprocess.Popen(r'adb -s 127.0.0.1:%d shell input swipe %d %d %d %d %d' %(startport,x,y,x,y,time*1000),shell=True)
    print(x,y)
# 滑屏
def swipe(drt,startport):
    if drt == 'top':
        process = subprocess.Popen('adb -s 127.0.0.1:%s shell input swipe 640 200 640 700' % (startport), shell=True)
        time.sleep(2)
    elif drt == 'bot':
        process = subprocess.Popen('adb -s 127.0.0.1:%s shell input swipe 640 650 640 150' % (startport), shell=True)
        time.sleep(2)
    elif drt == 'left':
        process = subprocess.Popen('adb -s 127.0.0.1:%s shell input swipe 100 380 1000 360' % (startport), shell=True)
        time.sleep(2)
    elif drt == 'right':
        process = subprocess.Popen('adb -s 127.0.0.1:%s shell input swipe 1000 380 100 360' % (startport), shell=True)
        time.sleep(2)
#定点滑动
def swipeport(x1,y1,x2,y2,startport):
    subprocess.Popen('adb -s 127.0.0.1:%s shell input swipe %d %d %d %d' % (startport,x1,y1,x2,y2), shell=True)
    time.sleep(3)
# 输入文本
def text(text,startport):
    subprocess.Popen('adb -s 127.0.0.1:%s shell input text %s' % (startport, text), shell=True)
    time.sleep(1)
# 返回
def back(startport):
    print('back')
    subprocess.Popen('adb -s 127.0.0.1:%s shell input keyevent 4' % (startport), shell=True)
    time.sleep(3)
# HOME
def home(startport):
    subprocess.Popen('adb -s 127.0.0.1:%s shell input keyevent 3' % (startport), shell=True)
    time.sleep(3)
# HOME
def menu(startport):
    subprocess.Popen('adb -s 127.0.0.1:%s shell input keyevent 82' % (startport), shell=True)
    time.sleep(3)

# 熄灭
def interest(startport):
    subprocess.Popen('adb -s 127.0.0.1:%s shell input keyevent 223' % (startport), shell=True)
    time.sleep(3)
# 点亮
def light(startport):
    subprocess.Popen('adb -s 127.0.0.1:%s shell input keyevent 224' % (startport), shell=True)
    time.sleep(3)
# 静音
def silence(startport):
    process = subprocess.Popen('adb -s 127.0.0.1:%s shell input keyevent 164' % (startport), shell=True)
    time.sleep(1.5)
    click(pos['silence'][0], pos['silence'][1])
    
#关闭模拟器已停止工作报错        
def close_emu_err():
    close_window = win32gui.FindWindow(None, "VirtualBox Headless Frontend")
    win32gui.PostMessage(close_window, win32con.WM_CLOSE, 0, 0)
    
#关闭模拟器名字    
def close_emu_id(close_id):
    close_id = int(close_id)
    close_config = r'D:\Program Files\DundiEmu\DundiData\avd\dundi%d\config.ini' %(close_id)
    with open(close_config,'r') as close_file:
        configlines = close_file.readlines()
        for configline in configlines:
            if 'EmulatorTitleName' in configline:
                close_name = configline.split('=')[-1].rstrip('\n')
        close_emu_err()
        close_window = win32gui.FindWindow(None, close_name)
        win32gui.PostMessage(close_window, win32con.WM_CLOSE, 0, 0)# 关闭一个捐兵号
    '''
    action = r'"D:\Program Files\DundiEmu\dundi_helper.exe" --index %d --stop' %(close_id)
    subprocess.Popen(action,shell=True)
    '''
    print('============================= 关闭的模拟器名字为：%s ===============================' %(close_name))
        

    

#开模拟器
def start_emu_id(action,startid,*args):
    """0不用最小化,1最小化"""
    subprocess.Popen(action,shell=True)
    #确保模拟器进程已经启动
    if len(args) > 0:
        if int(args[0]) == 0:
            print('不用最小化')
        elif int(args[0]) == 1:
            while True:
                    result = subprocess.Popen('tasklist|findstr DunDiEmu.exe',shell = True,stdout=subprocess.PIPE).stdout.readline().split()[0]
                    print (result)
                    if result == b'DunDiEmu.exe':
                        time.sleep(1)
                        break
            #确保最小化
            for n in range(2):
                wnd = win32gui.FindWindow(u'Qt5QWindowIcon', None)  # 获取窗口句柄
                try:
                    win32gui.CloseWindow(wnd)  # 窗口最小化
                except:
                    pass
                time.sleep(3)
    #等待系统开机
    time.sleep(80)
    
def close():
    subprocess.Popen('taskkill /f /t /im DunDiEmu.exe & taskkill /f /t /im DdemuHandle.exe & taskkill /f /t /im adb.exe',shell=True)
    time.sleep(3)
    
#等待
def timewait(min,startport):
    for n in range(min):
        time.sleep(60)
        click(pos['cancel'][0], pos['cancel'][1], startport)
        
#启动coc
def startcoc(startport,wait_time):
    #connect(startport)
    start_id = str(int(startport) - 52550)
    if start_id in QQlists:#腾讯
        subprocess.Popen(r'adb -s 127.0.0.1:%d shell am start -n com.tencent.tmgp.supercell.clashofclans/com.supercell.titan.tencent.GameAppTencent' % (startport), shell=True)
    elif start_id in baidulists:#百度
        subprocess.Popen(r'adb -s 127.0.0.1:%d shell am start -n com.supercell.clashofclans.baidu/com.supercell.titan.kunlun.GameAppKunlun' % (startport), shell=True)
    else:#九游
        subprocess.Popen(r'adb -s 127.0.0.1:%d shell am start -n com.supercell.clashofclans.uc/com.supercell.titan.kunlun.uc.GameAppKunlunUC' % (startport), shell=True)
    #豌豆荚
    #subprocess.Popen(r'adb -s 127.0.0.1:%d shell am start -n com.supercell.clashofclans.uc/com.supercell.titan.kunlun.uc.GameAppKunlunUC' % (startport), shell=True)
    time.sleep(wait_time)
    login_click(start_id)
    #点击取消位置取消广告
    click(pos['exitstore'][0], pos['exitstore'][1], startport)
    click(pos['cancel'][0], pos['cancel'][1], startport)

#登录点击确认
def login_click(startid):
    startport = getport(startid)
    restart_server()
    connect(startport)#连接    
    time.sleep(10)
    if int(startid) == 1:#如果是星陨，尝试点击登录
        click(pos['login_wandoujia1'][0], pos['login_wandoujia1'][1], startport,3)
        click(pos['login_wandoujia2'][0], pos['login_wandoujia2'][1], startport,3)
    #elif str(startid) not in notplaylist:#双重否定表肯定，在轮循打资源列表中的id
    elif str(startid) in QQlists:#QQ
        click(pos['start_script'][0],pos['start_script'][1],startport,5)
    elif str(startid) in baidulists:#baidu
        click(pos['login_baidu1'][0],pos['login_baidu1'][1],startport,5)
        click(pos['login_baidu2'][0],pos['login_baidu2'][1],startport,3)
    else:
        #昆仑
        click(pos['login_kunlun1'][0], pos['login_kunlun1'][1], startport,3)
        click(pos['login_kunlun2'][0], pos['login_kunlun2'][1], startport,3)
        click(pos['login_kunlun3'][0], pos['login_kunlun3'][1], startport,3)
    
#重启coc
def restartcoc(startport):
    home(startport)
    time.sleep(60)
    startcoc(startport,35)
    
        
def kill_adb():
    subprocess.Popen('taskkill /f /t /im adb.exe',shell=True)
    time.sleep(3)
    
def kill_server():
    # 关闭模拟器连接
    subprocess.Popen('adb kill-server', shell=True)
    time.sleep(3)
    
def start_server():
    #开启模拟器连接
    subprocess.Popen('adb start-server', shell=True)
    time.sleep(3)

def restart_server():
    kill_adb()
    kill_server()

#打开黑松鼠
def coc_script_black(startport,wait_time):
    subprocess.Popen(r'adb -s 127.0.0.1:%d shell am start -n com.ais.foxsquirrel.coc/ui.activity.SplashActivity' %(startport),shell=True,stdout=subprocess.PIPE)
    time.sleep(wait_time)

#开始脚本操作
#coc
def start(startid):
    #startid = g.buttonbox(msg='选择启动的模拟器',title='coc',choices=['QQ1','QQ2','QQ3','QQ4','QQ5','星陨6','码奴7','码奴8','码奴9'])
    print(startid)
    if int(startid) == 0:
        action = r"D:\Program Files\DundiEmu\DunDiEmu.exe"
    else:
        action = r'"D:\Program Files\DundiEmu\DunDiEmu.exe" -multi %s -disable_audio  -fps 40' %(startid)
    #action = r'"D:\Program Files\DundiEmu\dundi_helper.exe" --index %d --start' %(startid)
    start_emu_id(action,startid)#开模拟器
    print('启动模拟器完成')
    startport = getport(startid)
    connect(startport)
    print('连接模拟器完成')
    coc_script_black(startport,20)
    print('启动黑松鼠脚本完成')
    time.sleep(10)
    click(pos['sure'][0],pos['sure'][1],startport)
    time.sleep(10)
    click(pos['start_script'][0],pos['start_script'][1],startport)
    time.sleep(15)
    login_click(startid)
    

#转换模式启动
def start_convert(action,startid,time_wait):
    subprocess.Popen(action,shell=True)
    #等待系统开机
    time.sleep(time_wait)
    # 连接模拟器
    startport = getport(startid)
    # 开启模拟器连接
    start_server()
    #多连接几次确保连接上
    connect(startport)

class Thunder:
    def start(self):
        subprocess.Popen(r'"D:\Program Files\Thunder Network\Thunder\Program\Thunder.exe"',shell=True)
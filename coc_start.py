#coding:utf-8
import subprocess
import time
import easygui as g
import re
import win32gui



#元素坐标
pos = {
  'coc_script':[500,680],
  'start_script':[200,1070],
  'sure':[360,935]
  }

QQ1 = r'"D:\Program Files\DundiEmu\DunDiEmu.exe" -multi 0 -disable_audio  -fps 40'
QQ2 = r'"D:\Program Files\DundiEmu\DunDiEmu.exe" -multi 1 -disable_audio  -fps 40'
QQ3 = r'"D:\Program Files\DundiEmu\DunDiEmu.exe" -multi 2 -disable_audio  -fps 40'
QQ4 = r'"D:\Program Files\DundiEmu\DunDiEmu.exe" -multi 3 -disable_audio  -fps 40'
QQ5 = r'"D:\Program Files\DundiEmu\DunDiEmu.exe" -multi 4 -disable_audio  -fps 40'


class Thunder:
    def start(self):
        subprocess.Popen(r'"D:\Program Files\Thunder Network\Thunder\Program\Thunder.exe"',shell=True)

class Coc:
    #开模拟器
    def start(self,qq,id,*args):
        subprocess.Popen(qq,shell=True)
        #确保模拟器进程已经启动
        for event in args:
            if event == 0:
                print('不用最小化')
            else:
                while True:
                    result = subprocess.Popen('tasklist|findstr DunDiEmu.exe',shell = True,stdout=subprocess.PIPE).stdout.readline().split()[0]
                    print (result)
                    if result == b'DunDiEmu.exe':
                        time.sleep(3)
                        break
                #确保最小化
                for n in range(2):
                    wnd = win32gui.FindWindow(u'Qt5QWindowIcon', None)  # 获取窗口句柄
                    win32gui.CloseWindow(wnd)  # 窗口最小化
                    time.sleep(3)
        #等待系统开机
        time.sleep(30)

        # 连接模拟器
        global startport
        if id == 0:
            startport = 5555
        else:
            startport = 52550 + id
        # 关闭模拟器连接
        subprocess.Popen('adb kill-server', shell=True)
        time.sleep(3)
        # 开启模拟器连接
        subprocess.Popen('adb start-server', shell=True)
        time.sleep(5)
        #多连接几次确保连接上
        for n in range(3):
            subprocess.Popen('adb connect 127.0.0.1:%d' % (startport), shell=True)
            time.sleep(3)

    #打开黑松鼠
    def coc_script(self,id):
        process = subprocess.Popen('adb -s 127.0.0.1:%d shell am start -n com.ais.foxsquirrel.coc/ui.activity.SplashActivity' %(id),shell=True)
        time.sleep(10)
        
    #点击屏幕
    def click(self,x,y,id):
        process = subprocess.Popen('adb -s 127.0.0.1:%d shell input tap %d %d' %(id,x,y),shell=True)
        time.sleep(3)

#开始操作
#coc
def start(startid):
    #startid = g.buttonbox(msg='选择启动的模拟器',title='coc',choices=['QQ1','QQ2','QQ3','QQ4','QQ5','星陨6','码奴7','码奴8','码奴9'])
    print(startid)
    #startnum = re.findall(r'\d+',startid)
    #startnum = int(startnum[0]) - 1
    action = r'"D:\Program Files\DundiEmu\DunDiEmu.exe" -multi %s -disable_audio  -fps 40' %(startid)
    c = Coc()
    c.start(action,startid)
    #c.start(星辰)
    print('start')
    c.coc_script(startport)
    print('script')
    time.sleep(1)
    c.click(pos['sure'][0],pos['sure'][1],startport)
    time.sleep(3)
    c.click(pos['start_script'][0],pos['start_script'][1],startport)
    time.sleep(3)


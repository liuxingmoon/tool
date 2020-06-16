#coding:utf-8
import subprocess
import time
import easygui as g
import re


#元素坐标
pos = {
  'coc_script':[500,680],
  'start_script':[195,1065]
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
    def start(self,qq):
        subprocess.Popen(qq,shell=True)
        time.sleep(30)
        #复制adb到模拟器目录
        #subprocess.Popen(r'copy "D:\Program Files\Python38\ADB\*.exe" "D:\Games\Nox\bin\"',shell=True)
        #获取模拟器的端口
        self.phoneid = subprocess.getoutput('adb devices')
        self.phoneid = self.phoneid.split()
        self.phoneid.pop()
        self.phoneid = self.phoneid.pop()

    #打开黑松鼠
    def coc_script(self):
        #process = subprocess.Popen('adb -s %s shell am start -n com.ais.foxsquirrel.coc/ui.activity.SplashActivity' %(self.phoneid),shell=True)
        process = subprocess.Popen('adb shell am start -n com.ais.foxsquirrel.coc/ui.activity.SplashActivity',shell=True)
        time.sleep(10)
        
    #点击屏幕
    def click(self,x,y):
        process = subprocess.Popen('adb shell input tap %d %d' %(x,y),shell=True)
        time.sleep(3)

#开始操作
#coc
def start():
    startid = g.buttonbox(msg='选择启动的模拟器',title='coc',choices=['QQ1','QQ2','QQ3','QQ4','QQ5','星陨6','码奴7'])
    print(startid)
    startnum = re.findall(r'\d+',startid)
    startnum = int(startnum[0]) - 1
    action = r'"D:\Program Files\DundiEmu\DunDiEmu.exe" -multi %s -disable_audio  -fps 40' %(startnum)
    c = Coc()
    c.start(action)
    #c.start(星辰)
    print('start')
    for n in range(6):
        c.coc_script()
        print('script')
    time.sleep(3)
    c.click(pos['start_script'][0],pos['start_script'][1])
    time.sleep(3)
'''
#迅雷
t = Thunder()
t.start()
time.sleep(3)
'''
#最小化
#s.mouse_click(1297, 1055)


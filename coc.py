import tkinter as tk
import coc_start
import coc_template
import configparser
import os
import coc_customer
import AutoClick as ak
import coc_update,coc_resume,coc_config
from config_ctrl import *
from file_ctrl import rename,replace
from read_config import *

basedir = os.getcwd()#tool目录
ddavd_path = r"D:\Program Files\DundiEmu\DundiData\avd"

def start():
    #启动部落冲突自动启动鼠标连点
    try:
        ak.start()
    except:
        print ('第二次打开部落冲突')
    try:
        def getinfo():
            info = coc_id.get()
            if (info == ""):
                # 不写就打开部落战id和升级id
                startidlist = config_read(configpath,"coc", "warids").split()
                levelupids = config_read(configpath,"coc", "levelupids").split()
                startidlist.extend(levelupids)#合并列表
            elif (info in ['w', 'W', 'war', 'War']):
                #部落战id
                startidlist = config_read(configpath,"coc", "warids").split()
            elif info.isdigit():
                # 如果输入的是数字
                startidlist = [info]
            elif info in ['a', 'A', 'all', 'ALL']:
                # 有All代表启动所有的
                os.chdir(ddavd_path)
                emulist = os.listdir()
                emulist = [x for x in emulist if '.rar' not in x]
                emulist.remove('vboxData')
                # 选出模拟器的启动id
                emunum = []
                for emu in emulist:
                    emunum.append(int(emu.replace('dundi', '')))
                # 排序
                emunum.sort()
                startidlist = emunum
            elif info in ['P', 'paid', 'Paid']:
                # P代表付费捐兵号
                startidlist = config_read(configpath,"coc", "donateids_for_paid").split()
            elif info in ['p', 'play', 'PLAY']:
                # p代表启动除了捐兵号，跳过号以及部落战号剩下的play号
                os.chdir(ddavd_path)
                emulist = os.listdir()
                emulist.remove('vboxData')
                emulist = [x for x in emulist if "rar" not in x]
                # 选出模拟器的启动id
                emunum = []
                for emu in emulist:
                    emunum.append(int(emu.replace('dundi', '')))
                skipids = config_read(configpath,"coc", "skipids").split()
                levelupids = config_read(configpath,"coc", "levelupids").split()
                donateids_for_paid = config_read(configpath,"coc", "donateids_for_paid").split()#获取付费捐兵id的list
                resourceids_server01 = get_resourceids("server01")
                resourceids_server02 = get_resourceids("server02")
                resourceids_server03 = get_resourceids("server03")
                warids = config_read(configpath,"coc", "warids").split()
                donateids = config_read(configpath,"coc", "donateids").split()
                skipids.extend(levelupids)  # 添加升级的id到跳过id列表中
                skipids.extend(warids)  # 添加部落战控制的id到跳过id列表中
                skipids.extend(donateids_for_paid)  # 添加部落战控制的id到跳过id列表中
                skipids.extend(donateids)  # 添加捐兵控制的id到跳过id列表中
                skipids.extend(resourceids_server01)  # 添加持续打资源的id到跳过id列表中
                skipids.extend(resourceids_server02)  # 添加持续打资源的id到跳过id列表中
                skipids.extend(resourceids_server03)  # 添加持续打资源的id到跳过id列表中
                skipids = [int(x) for x in skipids]  # 转换str型为int
                # 删除所有在emunum而也在skipids的
                startidlist = [x for x in emunum if x not in skipids]
                # 排序
                startidlist.sort()
            #9本升级的id，用于主pc升级完后放到worker03去打资源
            elif info in ['l', 'L', 'levelup', 'LEVELUP']:
                levelupids = config_read(configpath,"coc", "levelupids").split()
                startidlist = [x for x in levelupids]
            elif info in ['s', 'S', 'skip', 'SKIP']:
                skipids = config_read(configpath,"coc", "skipids").split()
                # 删除0和15
                # startidlist = [x for x in skipids if x not in ['0','15','28','35','39']]
                startidlist = [x for x in skipids if x not in ['0', '15', '1', '2', '3', '4', '5']]
            elif info in ['d', 'D', 'donate', 'DONATE']:
                donateids = config_read(configpath,"coc", "donateids").split()
                donateids_for_paid = config_read(configpath,"coc", "donateids_for_paid").split()#获取付费捐兵id的list
                #在持续打资源的list去除付费捐兵的list
                resourceids = get_resourceids(servername)#本主机的捐兵列表
                resourceids = [x for x in resourceids if x not in donateids_for_paid]
                # 在捐兵列表中去除付费捐兵的list和持续打资源的list
                startidlist = [x for x in donateids if (x not in donateids_for_paid) and (x not in resourceids)]
            elif info in ['r', 'R', 'resourceids']:
                resourceids = get_resourceids(servername)#本主机的捐兵列表
                resourceids = [x for x in resourceids if x not in donateids_for_paid]
                # 在持续打资源的list去除付费捐兵的list
                startidlist = [x for x in resourceids]
            elif info in ['u', 'U', 'up', 'UP']:  # 升级的模拟器id
                startid = int(config_read(configpath,"coc", "maxid")) + 1
                endid = max([int(x.strip('dundi').rstrip('.rar')) for x in os.listdir(ddavd_path) if x != 'vboxData'])
                startidlist = [x for x in range(startid, (endid + 1))]
            else:
                # 剩下的就是首尾格式的列表
                startidlist = info.split()
            print(startidlist, type(startidlist))
            os.chdir(basedir)
            return (startidlist)
        #部落战捐兵
        def wardonate():
            startidlist = getinfo()
            coc_template.wardonate(startidlist)
        #切换捐兵/打资源状态
        def convert_mode():
            startidlist = getinfo()
            for convert_id in startidlist:
                coc_template.convert_mode(convert_id,"play","force")#切换为捐兵
        #打资源
        def cocStart():
            startidlist = getinfo()  # 获取输入框信息
            for startid in startidlist:
                coc_start.start(int(startid))
        #砍树
        def cocRT():
            startid = int(coc_id.get())  # 获取输入框信息
            timewait = 2
            coc_template.removeTree(startid,timewait)
        #夜世界砍树
        def cocRTN():
            startid = int(coc_id.get())  # 获取输入框信息
            coc_template.removeTree_night(startid)
        #新号
        def cocNS():
            startid = coc_id.get()  # 获取输入框信息
            #输入框为空自动定义为最大id
            if startid == "":
                startid = len(os.listdir(ddavd_path)) - 2
            else:
                startid = int(startid)
            name = coc_newid.get()
            #自动定义名称为startid - 6
            if name == "":
                name = '0' + str(int(startid) - 6)
            coc_template.register(name,startid)
        
        #改目录id
        def change_id(oldid,newid):
            olddir = "dundi%d"%(oldid)
            newdir = "dundi%d"%(newid)
            rename(olddir,newdir)
            oldname = "EmulatorTitleName%d"%(oldid)
            newname = "EmulatorTitleName%d"%(newid)
            os.chdir(newdir)
            replace(oldname,newname,"config.ini")
            os.chdir(ddavd_path)
        
        #迁移模拟器实例位置
        def coc_moveid():
            startid = int(coc_moveid_start.get())  # 获取起始id
            endid = int(coc_moveid_end.get())  # 获取结束id
            tmpdir = "dundi" + str(startid) + "_bak"
            startdir = "dundi%d"%(startid)
            enddir = "dundi%d"%(endid)
            startname = "EmulatorTitleName%d"%(startid)
            endname = "EmulatorTitleName%d"%(endid)
            os.chdir(ddavd_path)#切换到avd目录
            #先将初始目录改名临时目录
            rename(startdir,tmpdir)
            if startid > endid:
                for changeid in range(startid-1,endid-1,-1):#不包含startid自己
                    change_id(changeid,changeid+1)
            else:
                for changeid in range(startid+1,endid+1):
                    change_id(changeid,changeid-1)
            rename(tmpdir,enddir)
            os.chdir(enddir)
            replace(startname,endname,"config.ini")          
            os.chdir(basedir)#返回原始目录
            
        #升级资源
        def cocRC():
            startidlist = getinfo()
            startid = coc_id.get()  # 获取输入框信息
            skipids = config_read(configpath,"coc", "skipids").split()
            levelupids = [int(x) for x in skipids if x not in ['0', '15']]
            #输入框为空自动定义为最大id
            if startid == "":
                startid = int(config_read(configpath,"coc", "maxid")) + 1
                endid = max([int(x.strip('dundi').rstrip('.rar')) for x in os.listdir(ddavd_path) if x != 'vboxData'])
                if startid > endid:#maxid后没有新建模拟器，只升级levelupids
                    for levelupid in levelupids:
                        coc_template.resource_up(levelupid)
                else:
                    coc_template.resource_all(startid,endid,levelupids)
            else:
                coc_template.resource_all(startidlist)
        #启动部落冲突
        def cocst():
            startidlist = getinfo()
            coc_template.start_coc(startidlist)
        #升级3本
        def levelup_3():
            startidlist = getinfo()
            startidlist = [int(x) for x in startidlist]
            startid = coc_id.get()  # 获取输入框信息
            skipids = config_read(configpath,"coc", "skipids").split()
            levelupids = [int(x) for x in skipids if x not in ['0', '15']]
            #输入框为空自动定义为最大id
            if startid == "":
                startid = int(config_read(configpath,"coc", "maxid")) + 1
                endid = max([int(x.strip('dundi').rstrip('.rar')) for x in os.listdir(ddavd_path) if x != 'vboxData'])
                if startid > endid:#maxid后没有新建模拟器，只升级levelupids
                    for levelupid in levelupids:
                        coc_template.levelup_3(levelupid)
                else:
                    coc_template.levelup_3_all(startid,endid,levelupids)
            else:
                coc_template.levelup_3_all(startidlist)
        #更新游戏
        def update_coc():
            startidlist = getinfo()
            coc_template.update_coc(startidlist)
            
        #更新黑松鼠
        def update_hss():
            startidlist = getinfo()
            coc_template.update_hss(startidlist)
            
        root = tk.Tk()
        root.title('部落冲突')
        #title = tk.Label(root, text='部落冲突脚本功能')
        #title.grid(row=0, column=2)
        coc_label = tk.Label(root, text='模拟器id')
        coc_label.grid(row=0, column=1, sticky='w' + 'e')  # 居中
        coc_id = tk.Entry(root, width=15)
        coc_id.grid(row=0, column=2,
                          padx=10, pady=10)
        #部落战捐兵
        wardonate_bt = tk.Button(root, text='部落战捐兵', width=15, command=wardonate)
        wardonate_bt.grid(row=0, column=3)
        # 部落冲突新账号建立
        coc_newlabel = tk.Label(root, text='新号id')
        coc_newlabel.grid(row=1, column=1, sticky='w' + 'e')  # 居中
        coc_newid = tk.Entry(root, width=15)
        coc_newid.grid(row=1, column=2,
                          padx=10, pady=10)
        cocremove_bt = tk.Button(root, text='新号脚本', command=cocNS, width=15)
        cocremove_bt.grid(row=1, column=3,
                          padx=10, pady=10)
        #迁移模拟器实例位置
        coc_moveid_start = tk.Entry(root, width=15)
        coc_moveid_start.grid(row=2, column=1,
                          padx=10, pady=10)
        coc_moveid_end = tk.Entry(root, width=15)
        coc_moveid_end.grid(row=2, column=2,
                          padx=10, pady=10)
        coc_moveid_bt = tk.Button(root, text='迁移模拟器', command=coc_moveid, width=15)
        coc_moveid_bt.grid(row=2, column=3,
                          padx=10, pady=10)
        # 部落冲突打资源
        coc_bt = tk.Button(root, text='打资源', command=cocStart, width=15)
        coc_bt.grid(row=3, column=1,
                    padx=10, pady=10)
        #3本新建建筑
        coclevelup_bt = tk.Button(root, text='3本建造建筑', command=levelup_3, width=15)
        coclevelup_bt.grid(row=3, column=2,
                          padx=10, pady=10)
        # 部落冲突升级资源
        cocremove_bt = tk.Button(root, text='升级资源', command=cocRC, width=15)
        cocremove_bt.grid(row=3, column=3,
                          padx=10, pady=10)
        #只启动部落冲突，不打资源
        cocstart_bt = tk.Button(root, text='启动部落冲突', command=cocst, width=15)
        cocstart_bt.grid(row=4, column=1,
                          padx=10, pady=10)
        # 部落冲突砍树
        cocremove_bt = tk.Button(root, text='砍树', command=cocRT, width=15)
        cocremove_bt.grid(row=4, column=2,
                          padx=10, pady=10)
        # 部落冲突砍树
        cocremoveN_bt = tk.Button(root, text='夜世界砍树@', command=cocRTN, width=15)
        cocremoveN_bt.grid(row=4, column=3,
                          padx=10, pady=10)
        #切换捐兵/打资源状态
        convert_mode_bt = tk.Button(root, text='切换捐兵状态', command=convert_mode, width=15)
        convert_mode_bt.grid(row=5, column=1,
                          padx=10, pady=10)
        #客户信息
        custmoer_bt = tk.Button(root, text='客户信息', command=coc_customer.start, width=15)
        custmoer_bt.grid(row=5, column=2,
                          padx=10, pady=10)
        #更新代码
        coc_update_code_bt = tk.Button(root,text='更新代码',command=coc_update.start,width=15)
        coc_update_code_bt.grid(row=5,column=3,
              padx=10,pady=10)
        #恢复备份
        coc_resume_bt = tk.Button(root,text='恢复代码',command=coc_resume.start,width=15)
        coc_resume_bt.grid(row=6,column=1,
              padx=10,pady=10)
        #脚本配置
        coc_config_bt = tk.Button(root,text='脚本配置',command=coc_config.start,width=15)
        coc_config_bt.grid(row=6,column=2,
              padx=10,pady=10)
        #更新游戏
        coc_update_coc_bt = tk.Button(root,text='更新游戏',command=update_coc,width=15)
        coc_update_coc_bt.grid(row=6,column=3,
              padx=10,pady=10)
        #更新黑松鼠
        coc_update_hss_bt = tk.Button(root,text='更新黑松鼠',command=update_hss,width=15)
        coc_update_hss_bt.grid(row=7,column=1,
              padx=10,pady=10)
        root.mainloop()
    except:
        root.destroy()
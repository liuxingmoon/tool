import tkinter as tk
import coc_start
import coc_template
import configparser
import os
import coc_customer
import AutoClick as ak
import coc_update,coc_resume,coc_config

basedir = os.getcwd()
def start():
    #启动部落冲突自动启动鼠标连点
    try:
        ak.start()
    except:
        print ('第二次打开部落冲突')
    try:
        def getinfo():
            info = coc_id.get()
            config = configparser.ConfigParser()
            config.read("Config.ini", encoding="utf-8")
            if (info == "") or (info in ['w', 'W', 'war', 'War']):
                # 不写就打开部落战id
                startidlist = config.get("coc", "warids").split()
            elif info.isdigit():
                # 如果输入的是数字
                startidlist = [info]
            elif info in ['a', 'A', 'all', 'ALL']:
                # 有All代表启动所有的
                os.chdir(r'D:\Program Files\DundiEmu\DundiData\avd')
                emulist = os.listdir()
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
                startidlist = config.get("coc", "donateids_for_paid").split()
            elif info in ['p', 'play', 'PLAY']:
                # p代表启动除了捐兵号，跳过号以及部落战号剩下的play号
                os.chdir(r'D:\Program Files\DundiEmu\DundiData\avd')
                emulist = os.listdir()
                emulist.remove('vboxData')
                # 选出模拟器的启动id
                emunum = []
                for emu in emulist:
                    emunum.append(int(emu.replace('dundi', '')))
                skipids = config.get("coc", "skipids").split()
                resourceids_work01 = config.get("coc", "resourceids_work01").split()  # 获取持续打资源id的list
                resourceids_work02 = config.get("coc", "resourceids_work02").split()  # 获取持续打资源id的list
                resourceids_work03 = config.get("coc", "resourceids_work03").split()  # 获取持续打资源id的list
                warids = config.get("coc", "warids").split()
                donateids_for_paid = config.get("coc", "donateids_for_paid").split()
                resourceids = [x for x in resourceids_work01 if x not in donateids_for_paid]  # 在持续打资源的list去除付费捐兵的list
                donateids = config.get("coc", "donateids").split()
                skipids.extend(warids)  # 添加部落战控制的id到跳过id列表中
                skipids.extend(donateids_for_paid)  # 添加部落战控制的id到跳过id列表中
                skipids.extend(donateids)  # 添加捐兵控制的id到跳过id列表中
                skipids.extend(resourceids_work01)  # 添加持续打资源的id到跳过id列表中
                skipids.extend(resourceids_work02)  # 添加持续打资源的id到跳过id列表中
                skipids.extend(resourceids_work03)  # 添加持续打资源的id到跳过id列表中
                skipids = [int(x) for x in skipids]  # 转换str型为int
                # 删除所有在emunum而也在skipids的
                startidlist = [x for x in emunum if x not in skipids]
                # 排序
                startidlist.sort()
            #9本升级的id，用于主pc升级完后放到worker03去打资源
            elif info in ['l', 'L', 'levelup', 'LEVELUP']:
                levelupids = config.get("coc", "levelupids").split()
                startidlist = [x for x in levelupids]
            elif info in ['s', 'S', 'skip', 'SKIP']:
                skipids = config.get("coc", "skipids").split()
                # 删除0和15
                # startidlist = [x for x in skipids if x not in ['0','15','28','35','39']]
                startidlist = [x for x in skipids if x not in ['0', '15', '1', '2', '3', '4', '5']]
            elif info in ['d', 'D', 'donate', 'DONATE']:
                donateids = config.get("coc", "donateids").split()
                donateids_for_paid = config.get("coc", "donateids_for_paid").split()  # 获取付费捐兵id的list
                resourceids_work01 = config.get("coc", "resourceids_work01").split()  # 获取持续打资源id的list
                resourceids_work02 = config.get("coc", "resourceids_work02").split()  # 获取持续打资源id的list
                resourceids_work03 = config.get("coc", "resourceids_work03").split()  # 获取持续打资源id的list
                # 在持续打资源的list去除付费捐兵的list
                resourceids = [x for x in resourceids_work01 if x not in donateids_for_paid]
                # 在捐兵列表中去除付费捐兵的list和持续打资源的list
                startidlist = [x for x in donateids if (x not in donateids_for_paid) and (x not in resourceids)]
            elif info in ['u', 'U', 'up', 'UP']:  # 升级的模拟器id
                config = configparser.ConfigParser()
                config.read("Config.ini", encoding="utf-8")
                startid = int(config.get("coc", "maxid")) + 1
                endid = max([int(x.strip('dundi').rstrip('.rar')) for x in os.listdir(r'D:\Program Files\DundiEmu\DundiData\avd\\') if x != 'vboxData'])
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
                startid = len(os.listdir(r'D:\Program Files\DundiEmu\DundiData\avd\\')) - 2
            else:
                startid = int(startid)
            name = coc_newid.get()
            #自动定义名称为startid - 6
            if name == "":
                name = '0' + str(int(startid) - 6)
            coc_template.register(name,startid)
        #升级资源
        def cocRC():
            startidlist = getinfo()
            startid = coc_id.get()  # 获取输入框信息
            config = configparser.ConfigParser()
            config.read("Config.ini", encoding="utf-8")
            skipids = config.get("coc", "skipids").split()
            levelupids = [int(x) for x in skipids if x not in ['0', '15']]
            #输入框为空自动定义为最大id
            if startid == "":
                startid = int(config.get("coc", "maxid")) + 1
                endid = max([int(x.strip('dundi').rstrip('.rar')) for x in os.listdir(r'D:\Program Files\DundiEmu\DundiData\avd\\') if x != 'vboxData'])
                if startid > endid:#maxid后没有新建模拟器，只升级levelupids
                    for levelupid in levelupids:
                        coc_template.resource_up(levelupid)
                else:
                    coc_template.resource_all(startid,endid,levelupids)
            else:
                coc_template.resource_all(levelupids)
        #启动部落冲突
        def cocst():
            startidlist = getinfo()
            coc_template.start_coc(startidlist)
        #升级3本
        def levelup_3():
            startidlist = getinfo()
            startid = coc_id.get()  # 获取输入框信息
            #输入框为空自动定义为最大id
            if startid == "":
                config = configparser.ConfigParser()
                config.read("Config.ini", encoding="utf-8")
                startid = int(config.get("coc", "maxid")) + 1
                endid = len(os.listdir(r'D:\Program Files\DundiEmu\DundiData\avd\\')) - 2
            #print(startidlist, type(startidlist))
            else:
                startid = int(startidlist[0])
                endid = int(startidlist[1])
            coc_template.levelup_3(startid,endid)

        root = tk.Tk()
        root.title('部落冲突')
        title = tk.Label(root, text='部落冲突脚本功能')
        title.grid(row=0, column=2)
        coc_label = tk.Label(root, text='模拟器id')
        coc_label.grid(row=1, column=1, sticky='w' + 'e')  # 居中
        coc_id = tk.Entry(root)
        coc_id.grid(row=1, column=2)
        #部落战捐兵
        wardonate_bt = tk.Button(root, text='部落战捐兵', width=15, command=wardonate)
        wardonate_bt.grid(row=1, column=3)
        # 部落冲突新账号建立
        coc_newlabel = tk.Label(root, text='新号id')
        coc_newlabel.grid(row=2, column=1, sticky='w' + 'e')  # 居中
        coc_newid = tk.Entry(root)
        coc_newid.grid(row=2, column=2)
        cocremove_bt = tk.Button(root, text='新号脚本', command=cocNS, width=15)
        cocremove_bt.grid(row=2, column=3,
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
        coc_update_bt = tk.Button(root,text='更新备份',command=coc_update.start,width=15)
        coc_update_bt.grid(row=5,column=3,
              padx=10,pady=10)
        #恢复备份
        coc_resume_bt = tk.Button(root,text='恢复代码',command=coc_resume.start,width=15)
        coc_resume_bt.grid(row=6,column=1,
              padx=10,pady=10)
        #脚本配置
        coc_config_bt = tk.Button(root,text='脚本配置',command=coc_config.start,width=15)
        coc_config_bt.grid(row=6,column=2,
              padx=10,pady=10)
        root.mainloop()
    except:
        root.destroy()
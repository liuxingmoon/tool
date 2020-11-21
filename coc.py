import tkinter as tk
import coc_start
import coc_template
import configparser
import os
import coc_customer
import AutoClick as ak

def start():
    #启动部落冲突自动启动鼠标连点
    try:
        ak.start()
    except:
        print ('第二次打开部落冲突')
    try:
        
        def getinfo():
            # info = coc_id.get().split()
            info = int(coc_id.get())
            print(info,type(info))
            return info
        def wardonate():
            info = coc_id.get()
            #不写就打开部落战id
            if info == "":
                config = configparser.ConfigParser()
                config.read("Config.ini", encoding="utf-8")
                startidlist = config.get("coc", "warids").split()
            else:
                startidlist = info.split()
            print(startidlist,type(startidlist))
            coc_template.wardonate(startidlist)
        def convert_mode():
            startidlist = coc_id.get().split()
            print(startidlist,type(startidlist))
            coc_template.convert_mode(startidlist)
        def cocStart():
            startid = getinfo()  # 获取输入框信息
            coc_start.start(startid)
        def cocRT():
            startid = getinfo()  # 获取输入框信息
            timewait = 2
            coc_template.removeTree(startid,timewait)
        def cocRTN():
            startid = getinfo()  # 获取输入框信息
            coc_template.removeTree_night(startid)
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
        def cocRC():
            startidlist = coc_id.get().split()
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
                endid = int(startidlist[-1])
            coc_template.resource(startid,endid)
        def cocst():
            info = coc_id.get()
            config = configparser.ConfigParser()
            config.read("Config.ini", encoding="utf-8")
            if info == "":
                # 不写就打开部落战id
                startidlist = config.get("coc", "warids").split()
            elif info in ['a','A','all','ALL']:
                #有All代表启动所有的
                os.chdir(r'D:\Program Files\DundiEmu\DundiData\avd')
                emulist = os.listdir()
                emulist.remove('vboxData')
                #选出模拟器的启动id
                emunum = []
                for emu in emulist:
                    emunum.append(int(emu.replace('dundi', '')))
                #排序
                emunum.sort()
                startidlist = emunum
            elif info in ['p','P','play','PLAY']:
                #P代表启动除了捐兵号，跳过号以及部落战号剩下的play号
                os.chdir(r'D:\Program Files\DundiEmu\DundiData\avd')
                emulist = os.listdir()
                emulist.remove('vboxData')
                #选出模拟器的启动id
                emunum = []
                for emu in emulist:
                    emunum.append(int(emu.replace('dundi', '')))
                skipids = config.get("coc", "skipids").split()
                warids = config.get("coc", "warids").split()
                donateids = config.get("coc", "donateids").split()
                skipids.extend(warids)  # 添加部落战控制的id到跳过id列表中
                skipids.extend(donateids)  # 添加捐兵控制的id到跳过id列表中
                skipids = [int(x) for x in skipids] # 转换str型为int
                #删除所有在emunum而也在skipids的
                startidlist = [x for x in emunum if x not in skipids]
                #排序
                startidlist.sort()
            elif info in ['s', 'S', 'skip', 'SKIP']:
                skipids = config.get("coc", "skipids").split()
                #删除0和26
                startidlist = [x for x in skipids if x not in ['0','26']]
            else:
                startidlist = info.split()
            print(startidlist, type(startidlist))
            #startid = int(startidlist[0])
            #endid = int(startidlist[1])
            coc_template.start_coc(startidlist)
        def levelup_3():
            startidlist = coc_id.get().split()
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
        convert_mode_bt = tk.Button(root, text='切换状态', command=convert_mode, width=15)
        convert_mode_bt.grid(row=5, column=1,
                          padx=10, pady=10)
        #客户信息
        custmoer_bt = tk.Button(root, text='客户信息', command=coc_customer.start, width=15)
        custmoer_bt.grid(row=5, column=2,
                          padx=10, pady=10)

        root.mainloop()
    except:
        root.destroy()
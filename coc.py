import tkinter as tk
import coc_start
import coc_template
import configparser

def start():
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
            startid = getinfo()  # 获取输入框信息
            name = coc_newid.get()
            coc_template.register(name,startid)
        def cocRC():
            startidlist = coc_id.get().split()
            print(startidlist, type(startidlist))
            startid = int(startidlist[0])
            endid = int(startidlist[1])
            coc_template.resource(startid,endid)
        def cocst():
            info = coc_id.get()
            #不写就打开部落战id
            if info == "":
                config = configparser.ConfigParser()
                config.read("Config.ini", encoding="utf-8")
                startidlist = config.get("coc", "warids").split()
            else:
                startidlist = info.split()
            print(startidlist, type(startidlist))
            #startid = int(startidlist[0])
            #endid = int(startidlist[1])
            coc_template.start_coc(startidlist)
        def levelup_3():
            startidlist = coc_id.get().split()
            print(startidlist, type(startidlist))
            startid = int(startidlist[0])
            endid = int(startidlist[1])
            coc_template.levelup_3(startid,endid)

        root = tk.Tk()
        root.title('部落冲突')
        title = tk.Label(root, text='部落冲突脚本功能')
        title.grid(row=0, column=2)
        coc_label = tk.Label(root, text='模拟器id')
        coc_label.grid(row=1, column=1, sticky='w')  # 左对齐
        coc_id = tk.Entry(root)
        coc_id.grid(row=1, column=2)
        #部落战捐兵
        wardonate_bt = tk.Button(root, text='部落战捐兵', width=10, command=wardonate)
        wardonate_bt.grid(row=1, column=3)
        # 部落冲突打资源
        coc_bt = tk.Button(root, text='打资源', command=cocStart, width=15)
        coc_bt.grid(row=2, column=1,
                    padx=10, pady=10)
        #3本新建建筑
        coclevelup_bt = tk.Button(root, text='3本建造建筑', command=levelup_3, width=15)
        coclevelup_bt.grid(row=2, column=2,
                          padx=10, pady=10)
        # 部落冲突升级资源
        cocremove_bt = tk.Button(root, text='升级资源', command=cocRC, width=15)
        cocremove_bt.grid(row=2, column=3,
                          padx=10, pady=10)
        # 部落冲突新账号建立
        coc_newlabel = tk.Label(root, text='新号id')
        coc_newlabel.grid(row=3, column=1, sticky='w')  # 左对齐
        coc_newid = tk.Entry(root)
        coc_newid.grid(row=3, column=2)
        cocremove_bt = tk.Button(root, text='新号脚本', command=cocNS, width=15)
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

        root.mainloop()
    except:
        root.destroy()
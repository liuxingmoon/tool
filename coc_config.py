import tkinter as tk
import configparser
import os
import ast

basedir = os.getcwd()
def start():
    def getinfo():
        info = coc_query_id_entry.get()
        # 读取配置
        config = configparser.ConfigParser()
        config.read("Config.ini", encoding="utf-8")
        if (info == "") or (info in ['w','W','war','War']):
            # 不写就打开部落战id
            startidlist = config.get("coc", "warids").split()
        elif info.isdigit():
            # 如果输入的是数字
            startidlist = [info]
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
        elif info in ['P','paid','Paid']:
            #P代表付费捐兵号
            startidlist = config.get("coc", "donateids_for_paid").split()
        elif info in ['p','play','PLAY']:
            #p代表启动除了捐兵号，跳过号以及部落战号剩下的play号
            os.chdir(r'D:\Program Files\DundiEmu\DundiData\avd')
            emulist = os.listdir()
            emulist.remove('vboxData')
            #选出模拟器的启动id
            emunum = []
            for emu in emulist:
                emunum.append(int(emu.replace('dundi', '')))
            skipids = config.get("coc", "skipids").split()
            levelupids = config.get("coc", "levelupids").split()
            resourceids_work01 = config.get("coc", "resourceids_work01").split()#获取持续打资源id的list
            resourceids_work02 = config.get("coc", "resourceids_work02").split()#获取持续打资源id的list
            resourceids_work03 = config.get("coc", "resourceids_work03").split()#获取持续打资源id的list
            warids = config.get("coc", "warids").split()
            donateids_for_paid = config.get("coc", "donateids_for_paid").split()
            resourceids = [x for x in resourceids_work01 if x not in donateids_for_paid]#在持续打资源的list去除付费捐兵的list
            donateids = config.get("coc", "donateids").split()
            skipids.extend(warids)  # 添加部落战控制的id到跳过id列表中
            skipids.extend(donateids_for_paid)  # 添加部落战控制的id到跳过id列表中
            skipids.extend(donateids)  # 添加捐兵控制的id到跳过id列表中
            skipids.extend(levelupids)  # 添加捐兵控制的id到跳过id列表中
            skipids.extend(resourceids_work01)#添加持续打资源的id到跳过id列表中
            skipids.extend(resourceids_work02)#添加持续打资源的id到跳过id列表中
            skipids.extend(resourceids_work03)#添加持续打资源的id到跳过id列表中
            skipids = [int(x) for x in skipids] # 转换str型为int
            #删除所有在emunum而也在skipids的
            startidlist = [x for x in emunum if x not in skipids]
            #排序
            startidlist.sort()
        #9本升级的id，用于主pc升级完后放到worker03去打资源
        elif info in ['l', 'L', 'levelup', 'LEVELUP']:
            levelupids = config.get("coc", "levelupids").split()
            startidlist = [x for x in levelupids]
        elif info in ['s', 'S', 'skip', 'SKIP']:
            skipids = config.get("coc", "skipids").split()
            #删除0和15
            startidlist = [x for x in skipids if x not in ['0','15','1','2','3','4','5']]
        elif info in ['d', 'D', 'donate', 'DONATE']:
            donateids = config.get("coc", "donateids").split()
            donateids_for_paid = config.get("coc", "donateids_for_paid").split()#获取付费捐兵id的list
            resourceids_work01 = config.get("coc", "resourceids_work01").split()  # 获取持续打资源id的list
            resourceids_work02 = config.get("coc", "resourceids_work02").split()  # 获取持续打资源id的list
            resourceids_work03 = config.get("coc", "resourceids_work03").split()  # 获取持续打资源id的list
            # 在持续打资源的list去除付费捐兵的list
            resourceids = [x for x in resourceids_work01 if x not in donateids_for_paid]
            #在捐兵列表中去除付费捐兵的list和持续打资源的list
            startidlist = [x for x in donateids if (x not in donateids_for_paid) and (x not in resourceids)]
        elif info in ['u', 'U', 'up', 'UP']:#3本升级的模拟器id
            config = configparser.ConfigParser()
            config.read("Config.ini", encoding="utf-8")
            startid = int(config.get("coc", "maxid")) + 1
            endid = max([int(x.strip('dundi').rstrip('.rar')) for x in os.listdir(r'D:\Program Files\DundiEmu\DundiData\avd\\') if x != 'vboxData'])
            startidlist = [x for x in range(startid,(endid + 1))]
        else:
            #剩下的就是首尾格式的列表
            startidlist = info.split()
        print(startidlist, type(startidlist))
        os.chdir(basedir)
        return (startidlist)

    def getstatus(startidlist):
        startid_status_dict = {}
        config = configparser.ConfigParser()
        config.read("Config.ini", encoding="utf-8")
        for id in startidlist:
            startid = "startid%s" %(id)
            #获取各个id的捐兵状态
            try:
                startid_status = config.get("coc", startid)
            except configparser.NoOptionError as reason:
                print(reason)
                startid_status = 'No_option'
            startid_status_dict[startid] = startid_status
        return (startid_status_dict)

    def query():
        startidlist = getinfo()
        startid_status_dict = getstatus(startidlist)
        coc_query_status_entry.delete(0,'end')
        coc_query_status_entry.insert(0,startid_status_dict)
    def save_config():
        # 读取配置
        config = configparser.ConfigParser()
        config.read("Config.ini", encoding="utf-8")
        
        day_time = coc_time_day_entry.get()
        night_time = coc_time_night_entry.get()
        morning_time = coc_time_morning_entry.get()
        donateids_for_paid = coc_donateids_for_paid_entry.get()
        donateids_for_paid_2nd = coc_donateids_for_paid_2nd_entry.get()
        donateids = coc_donateids_entry.get()
        resourceids_work01 = coc_resourceids_work01_entry.get()
        resourceids_work02 = coc_resourceids_work02_entry.get()
        resourceids_work03 = coc_resourceids_work03_entry.get()
        resourceids_num = coc_resourceids_num_entry.get()
        donate_num = coc_donate_num_entry.get()
        donate_num_morning = coc_donate_num_morning_entry.get()
        instance_num_day = coc_instance_num_day_entry.get()
        instance_time_day = coc_instance_time_day_entry.get()
        instance_num_night = coc_instance_num_night_entry.get()
        instance_time_night = coc_instance_time_night_entry.get()
        instance_num_morning = coc_instance_num_morning_entry.get()
        instance_time_morning = coc_instance_time_morning_entry.get()
        levelupids = coc_lvup_id_entry.get()
        skipids = coc_skip_id_entry.get()
        coc_query_status = coc_query_status_entry.get()#结果为str不是dict
        if coc_query_status == "":
            flag_status = "none" 
        else:
            coc_query_status = ast.literal_eval(coc_query_status)#转换为dict
            flag_status = "exist" 

        #保存配置
        config.set("coc", "day_time", day_time)#只能存储str类型数据
        config.set("coc", "night_time", night_time)#只能存储str类型数据
        config.set("coc", "morning_time", morning_time)#只能存储str类型数据
        config.set("coc", "donateids_for_paid", donateids_for_paid)#只能存储str类型数据
        config.set("coc", "donateids_for_paid_2nd", donateids_for_paid_2nd)#只能存储str类型数据
        config.set("coc", "donateids", donateids)#只能存储str类型数据
        config.set("coc", "resourceids_work01", resourceids_work01)#只能存储str类型数据
        config.set("coc", "resourceids_work02", resourceids_work02)#只能存储str类型数据
        config.set("coc", "resourceids_work03", resourceids_work03)#只能存储str类型数据
        config.set("coc", "resourceids_num", resourceids_num)#只能存储str类型数据
        config.set("coc", "donate_num", donate_num)#只能存储str类型数据
        config.set("coc", "donate_num_morning", donate_num_morning)#只能存储str类型数据
        config.set("coc", "instance_num_day", instance_num_day)#只能存储str类型数据
        config.set("coc", "instance_time_day", instance_time_day)#只能存储str类型数据
        config.set("coc", "instance_num_night", instance_num_night)#只能存储str类型数据
        config.set("coc", "instance_time_night", instance_time_night)#只能存储str类型数据
        config.set("coc", "instance_num_morning", instance_num_morning)#只能存储str类型数据
        config.set("coc", "instance_time_morning", instance_time_morning)#只能存储str类型数据
        config.set("coc", "levelupids", levelupids)#只能存储str类型数据
        config.set("coc", "skipids", skipids)#只能存储str类型数据

        if flag_status == "exist" :
            #保存各个实例的状态
            for mu_id in coc_query_status:
                config.set("coc", mu_id, coc_query_status[mu_id])#只能存储str类型数据
        #写到配置文件
        config.write(open("Config.ini", "w",encoding='utf-8'))  # 保存到Config.ini
        

    root = tk.Tk()
    root.title('脚本配置')
    title = tk.Label(root, text='部落冲突脚本配置功能')
    title.grid(row=0, column=1,columnspan=6,sticky='w'+'e')
    # 读取配置
    config = configparser.ConfigParser()
    config.read("Config.ini", encoding="utf-8")
    #获取时间段
    day_time = config.get("coc", "day_time")
    night_time = config.get("coc", "night_time")
    morning_time = config.get("coc", "morning_time")
    #切换时间节点
    coc_time_day_lb = tk.Label(root, text='早上节点（切换捐兵）')
    coc_time_day_lb.grid(row=1, column=1, sticky='w' + 'e',padx=10, pady=10)  # 居中
    coc_time_day_entry = tk.Entry(root)
    coc_time_day_entry.insert(0,day_time)
    coc_time_day_entry.grid(row=1, column=2,padx=10, pady=10)

    coc_time_night_lb = tk.Label(root, text='晚上节点（高峰切低峰）')
    coc_time_night_lb.grid(row=1, column=3, sticky='w' + 'e',padx=10, pady=10)  # 居中
    coc_time_night_entry = tk.Entry(root)
    coc_time_night_entry.insert(0,night_time)
    coc_time_night_entry.grid(row=1, column=4,padx=10, pady=10)

    coc_time_morning_lb = tk.Label(root, text='凌晨节点（切换打资源）')
    coc_time_morning_lb.grid(row=1, column=5, sticky='w' + 'e',padx=10, pady=10)  # 居中
    coc_time_morning_entry = tk.Entry(root)
    coc_time_morning_entry.insert(0,morning_time)
    coc_time_morning_entry.grid(row=1, column=6,padx=10, pady=10)

    #捐兵号
    donateids_for_paid = config.get("coc", "donateids_for_paid")#获取付费捐兵id
    donateids_for_paid_2nd = config.get("coc", "donateids_for_paid_2nd")
    donateids = config.get("coc", "donateids")#获取捐兵id

    coc_donateids_for_paid_lb = tk.Label(root, text='付费捐兵号')
    coc_donateids_for_paid_lb.grid(row=2, column=1, sticky='w' + 'e',padx=10, pady=10)  # 居中
    coc_donateids_for_paid_entry = tk.Entry(root)
    coc_donateids_for_paid_entry.insert(0,donateids_for_paid)
    coc_donateids_for_paid_entry.grid(row=2, column=2,padx=10, pady=10)

    coc_donateids_for_paid_2nd_lb = tk.Label(root, text='付费捐兵号第二梯队')
    coc_donateids_for_paid_2nd_lb.grid(row=2, column=3, sticky='w' + 'e',padx=10, pady=10)  # 居中
    coc_donateids_for_paid_2nd_entry = tk.Entry(root)
    coc_donateids_for_paid_2nd_entry.insert(0,donateids_for_paid_2nd)
    coc_donateids_for_paid_2nd_entry.grid(row=2, column=4,padx=10, pady=10)

    coc_donateids_lb = tk.Label(root, text='自用捐兵号')
    coc_donateids_lb.grid(row=2, column=5, sticky='w' + 'e',padx=10, pady=10)  # 居中
    coc_donateids_entry = tk.Entry(root)
    coc_donateids_entry.insert(0,donateids)
    coc_donateids_entry.grid(row=2, column=6,padx=10, pady=10)

    #打资源号
    resourceids_work01 = config.get("coc", "resourceids_work01")#获取持续打资源id的list
    resourceids_work02 = config.get("coc", "resourceids_work02")#获取持续打资源id的list
    resourceids_work03 = config.get("coc", "resourceids_work03")#获取持续打资源id的list

    coc_resourceids_work01_lb = tk.Label(root, text='持续打资源号worker01')
    coc_resourceids_work01_lb.grid(row=3, column=1, sticky='w' + 'e',padx=10, pady=10)  # 居中
    coc_resourceids_work01_entry = tk.Entry(root)
    coc_resourceids_work01_entry.insert(0,resourceids_work01)
    coc_resourceids_work01_entry.grid(row=3, column=2,padx=10, pady=10)

    coc_resourceids_work02_lb = tk.Label(root, text='持续打资源号worker02')
    coc_resourceids_work02_lb.grid(row=3, column=3, sticky='w' + 'e',padx=10, pady=10)  # 居中
    coc_resourceids_work02_entry = tk.Entry(root)
    coc_resourceids_work02_entry.insert(0,resourceids_work02)
    coc_resourceids_work02_entry.grid(row=3, column=4,padx=10, pady=10)

    coc_resourceids_work03_lb = tk.Label(root, text='持续打资源号worker03')
    coc_resourceids_work03_lb.grid(row=3, column=5, sticky='w' + 'e',padx=10, pady=10)  # 居中
    coc_resourceids_work03_entry = tk.Entry(root)
    coc_resourceids_work03_entry.insert(0,resourceids_work03)
    coc_resourceids_work03_entry.grid(row=3, column=6,padx=10, pady=10)

    #启动实例数量
    resourceids_num = int(config.get("coc", "resourceids_num"))#打资源号的个数
    donate_num = int(config.get("coc", "donate_num"))#捐兵号的个数
    donate_num_morning = int(config.get("coc", "donate_num_morning"))#凌晨打资源时间段捐兵号的个数

    coc_resourceids_num_lb = tk.Label(root, text='持续打资源号数量')
    coc_resourceids_num_lb.grid(row=4, column=1, sticky='w' + 'e',padx=10, pady=10)  # 居中
    coc_resourceids_num_entry = tk.Entry(root)
    coc_resourceids_num_entry.insert(0,resourceids_num)
    coc_resourceids_num_entry.grid(row=4, column=2,padx=10, pady=10)

    coc_donate_num_lb = tk.Label(root, text='白天捐兵号数量')
    coc_donate_num_lb.grid(row=4, column=3, sticky='w' + 'e',padx=10, pady=10)  # 居中
    coc_donate_num_entry = tk.Entry(root)
    coc_donate_num_entry.insert(0,donate_num)
    coc_donate_num_entry.grid(row=4, column=4,padx=10, pady=10)

    coc_donate_num_morning_lb = tk.Label(root, text='凌晨打资源时段捐兵号数量')
    coc_donate_num_morning_lb.grid(row=4, column=5, sticky='w' + 'e',padx=10, pady=10)  # 居中
    coc_donate_num_morning_entry = tk.Entry(root)
    coc_donate_num_morning_entry.insert(0,donate_num_morning)
    coc_donate_num_morning_entry.grid(row=4, column=6,padx=10, pady=10)

    #白天和夜晚运行的实例数量和时间
    instance_num_day = int(config.get("coc", "instance_num_day"))
    instance_time_day = int(config.get("coc", "instance_time_day"))
    instance_num_night = int(config.get("coc", "instance_num_night"))
    instance_time_night = int(config.get("coc", "instance_time_night"))
    instance_num_morning = int(config.get("coc", "instance_num_morning"))
    instance_time_morning = int(config.get("coc", "instance_time_morning"))

    coc_instance_num_day_lb = tk.Label(root, text='早上节点总实例数量')
    coc_instance_num_day_lb.grid(row=5, column=1, sticky='w' + 'e',padx=10, pady=10)  # 居中
    coc_instance_num_day_entry = tk.Entry(root)
    coc_instance_num_day_entry.insert(0,instance_num_day)
    coc_instance_num_day_entry.grid(row=5, column=2,padx=10, pady=10)

    coc_instance_num_night_lb = tk.Label(root, text='夜晚节点总实例数量')
    coc_instance_num_night_lb.grid(row=5, column=3, sticky='w' + 'e',padx=10, pady=10)  # 居中
    coc_instance_num_night_entry = tk.Entry(root)
    coc_instance_num_night_entry.insert(0,instance_num_night)
    coc_instance_num_night_entry.grid(row=5, column=4,padx=10, pady=10)

    coc_instance_num_morning_lb = tk.Label(root, text='凌晨节点总实例数量')
    coc_instance_num_morning_lb.grid(row=5, column=5, sticky='w' + 'e',padx=10, pady=10)  # 居中
    coc_instance_num_morning_entry = tk.Entry(root)
    coc_instance_num_morning_entry.insert(0,instance_num_morning)
    coc_instance_num_morning_entry.grid(row=5, column=6,padx=10, pady=10)

    coc_instance_time_day_lb = tk.Label(root, text='早上节点轮询时间（分钟）')
    coc_instance_time_day_lb.grid(row=6, column=1, sticky='w' + 'e',padx=10, pady=10)  # 居中
    coc_instance_time_day_entry = tk.Entry(root)
    coc_instance_time_day_entry.insert(0,instance_time_day)
    coc_instance_time_day_entry.grid(row=6, column=2,padx=10, pady=10)

    coc_instance_time_night_lb = tk.Label(root, text='夜晚节点轮询时间（分钟）')
    coc_instance_time_night_lb.grid(row=6, column=3, sticky='w' + 'e',padx=10, pady=10)  # 居中
    coc_instance_time_night_entry = tk.Entry(root)
    coc_instance_time_night_entry.insert(0,instance_time_night)
    coc_instance_time_night_entry.grid(row=6, column=4,padx=10, pady=10)

    coc_instance_time_morning_lb = tk.Label(root, text='凌晨节点轮询时间（分钟）')
    coc_instance_time_morning_lb.grid(row=6, column=5, sticky='w' + 'e',padx=10, pady=10)  # 居中
    coc_instance_time_morning_entry = tk.Entry(root)
    coc_instance_time_morning_entry.insert(0,instance_time_morning)
    coc_instance_time_morning_entry.grid(row=6, column=6,padx=10, pady=10)

    #查询修改实例状态
    coc_query_id_lb = tk.Label(root, text='查询实例的id')
    coc_query_id_lb.grid(row=7, column=1, sticky='w' + 'e',padx=10, pady=10)  # 居中
    coc_query_id_entry = tk.Entry(root)
    coc_query_id_entry.grid(row=7, column=2,padx=10, pady=10)
    
    #升级实例id
    try:
        levelupids = config.get("coc", "levelupids")
    except configparser.NoOptionError as reason:
        print(reason)
        levelupids = ''
    coc_lvup_id_lb = tk.Label(root, text='升级实例id')
    coc_lvup_id_lb.grid(row=7, column=3, sticky='w' + 'e',padx=10, pady=10)  # 居中
    coc_lvup_id_entry = tk.Entry(root)
    coc_lvup_id_entry.insert(0,levelupids)
    coc_lvup_id_entry.grid(row=7, column=4,padx=10, pady=10)
    
    #跳过实例id
    skipids = config.get("coc", "skipids")
    coc_skip_id_lb = tk.Label(root, text='跳过实例id')
    coc_skip_id_lb.grid(row=8, column=1, sticky='w' + 'e',padx=10, pady=10)  # 居中
    coc_skip_id_entry = tk.Entry(root)
    coc_skip_id_entry.insert(0,skipids)
    coc_skip_id_entry.grid(row=8, column=2 ,columnspan=5,sticky='w'+'e',padx=10, pady=10)
    
    #查询实例状态
    coc_query_bt = tk.Button(root,text='查询实例状态',command=query,width=15)
    coc_query_bt.grid(row=7,column=5,
        padx=10,pady=10)
    coc_save_bt = tk.Button(root,text='保存配置',command=save_config,width=15)
    coc_save_bt.grid(row=7,column=6,
        padx=10,pady=10)
        
    coc_query_status_lb = tk.Label(root, text='实例状态')
    coc_query_status_lb.grid(row=9, column=1, sticky='w' + 'e',padx=10, pady=10)  # 居中
    coc_query_status_entry = tk.Entry(root)
    coc_query_status_entry.grid(row=9, column=2,columnspan=5,sticky='w'+'e',padx=10, pady=10)

    root.mainloop()

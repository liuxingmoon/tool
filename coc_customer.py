import datetime
import csv
import os
import tkinter as tk
import easygui as g

def select_tb(tbname):
    # 判断是否存在文件
    if tbname not in os.listdir():
        print('%s 不存在，请确认！' %(tbname))
    else:
        # 创建文件对象
        f = open(tbname,'r',encoding='gb2312',newline="")
        # 基于文件对象构建 csv写入对象
        csv_reader = csv.reader(f)
        # 保存表结果
        table = []
        for line in f:
            table.append(line)
        # 关闭文件
        f.close()
        print(table)
        return (table)

def create_tb(tbname,values):
    # 排查是否已存在同名文件
    if tbname in os.listdir():
        print('%s 已存在，不需要创建！' %(tbname))
    else:
        # 创建文件对象
        f = open(tbname,'w',encoding='gb2312',newline="")
        # 基于文件对象构建 csv写入对象
        csv_writer = csv.writer(f)
        # 构建列表头
        csv_writer.writerow(values)
        # 关闭文件
        f.close()

def insert_tb(tbname,values):
    # values为列表格式
    # 判断是否存在文件
    if tbname not in os.listdir():
        create_tb(tbname)
    # 新建行存储新用户信息
    # 创建文件对象
    f = open('coc_customer.csv','a',encoding='gb2312',newline="")
    # 基于文件对象构建 csv写入对象
    csv_writer = csv.writer(f)
    # 写入csv文件内容
    csv_writer.writerow(values)
    # 关闭文件
    f.close()

def update_tb(tbname,values):
    table = select_tb(tbname)
    # 核对用户部落名
    index = -1  # 记录用户的index
    coc_clan_name = values[2]
    for column in table:
        info = column.split(',')
        if coc_clan_name == info[2]:
            index += 1
            break  # 出现后立刻跳出
        else:
            index += 1
    #替换需要替换的字段：结束服务时间,总服务时间,总消费金额

    info = table[index].split(',')
    srv_time = int(info[5]) + int(values[5])
    money = int(info[6]) + int(values[6])
    table[index] = table[index].replace(info[4],values[4])
    table[index] = table[index].replace(info[5],str(srv_time))
    table[index] = table[index].replace(info[6],str(money))
    #将更新后的table直接覆盖写入到表中
    # 创建文件对象
    with open('coc_customer.csv','w',encoding='gb2312',newline="") as f:
    # 基于文件对象构建 csv写入对象
    #csv_writer = csv.writer(f)
        for column in table:
            column = column.replace('\r\n','')
            insert_tb(tbname,column.split(','))
        # 写入csv文件内容
        #.writerow(column.split(','))
    #print(table)

#获取模拟器信息（模拟器id，部落名称，服务月数，收入金额）
def get_coc_info():
    coc_id = coc_id_ny.get()
    coc_clan_name = coc_clan_name_ny.get()
    srv_month = coc_srv_month_ny.get()
    money = coc_money_ny.get()
    return (int(coc_id),coc_clan_name,int(srv_month),int(money))

#根据模拟器id获取信息
def get_coc_name(coc_id):
    coc_config = r'D:\Program Files\DundiEmu\DundiData\avd\dundi%d\config.ini' % (coc_id)
    with open(coc_config, 'r') as file:
        configlines = file.readlines()
        for configline in configlines:
            if 'EmulatorTitleName' in configline:
                coc_name = configline.split('=')[-1].rstrip('\n')
    return (coc_name)

#计算并输出截止时间
def deadtime(month):
    #month==租的月数
    # 当前时间
    start_time = datetime.datetime.now()
    start_time_hr = start_time.strftime('%Y-%m-%d %H:%M')
    #捐兵服务时间31天算一个月
    srv_days_hr = 31 * month
    srv_days = datetime.timedelta(days=srv_days_hr)
    #结束时间
    dead_time = start_time + srv_days
    dead_time_hr = dead_time.strftime('%Y-%m-%d %H:%M')
    #打印结果
    g.msgbox(msg='尊敬的用户，您的服务已经开始为您服务！\n服务开始时间为：%s\n一共服务时间：%d 天\n服务结束时间：%s\n祝您游戏愉快！' %(start_time_hr,srv_days_hr,dead_time_hr),title='用户信息')
    print('尊敬的用户，您的服务已经开始为您服务！\n服务开始时间为：%s\n一共服务时间：%d 天\n服务结束时间：%s' %(start_time_hr,srv_days_hr,dead_time_hr))
    return (start_time_hr,dead_time_hr,srv_days_hr)

#续费
def renewal(month,values):
    #获取原始信息
    start_time_hr = values[3]
    dead_time_hr = values[4]
    coc_clan_name = values[2]
    #转换原截止时间
    #print(dead_time_hr)
    dead_time = datetime.datetime.strptime(str(dead_time_hr),'%Y-%m-%d %H:%M')
    #dead_tiem = datetime.datetime.strptime()
    #捐兵服务时间31天算一个月
    srv_days_hr = 31 * month
    srv_days = datetime.timedelta(days=srv_days_hr)
    #结束时间
    dead_time = dead_time + srv_days
    dead_time_hr = dead_time.strftime('%Y-%m-%d %H:%M')
    #打印结果
    g.msgbox(msg='尊敬的用户，您的部落 %s\n捐兵服务已经续费成功！\n续费服务时间：%d 天\n服务结束时间：%s\n祝您游戏愉快！' %(coc_clan_name,srv_days_hr,dead_time_hr), title='用户信息')
    print('尊敬的用户，您的服务已经续费成功！\n续费服务时间：%d 天\n服务结束时间：%s\n祝您游戏愉快！' %(srv_days_hr,dead_time_hr))
    return (start_time_hr,dead_time_hr,srv_days_hr)

#提醒续费
def clarm():
    # 当前时间
    now_time = datetime.datetime.now()
    table = select_tb('coc_customer.csv')
    #去除表头
    table.pop(0)
    for column in table:
        info = column.split(',')
        #截止时间
        dead_time_hr = info[4]
        #部落名称
        coc_clan_name = info[2]
        #转换截止时间
        dead_time = datetime.datetime.strptime(str(dead_time_hr), '%Y-%m-%d %H:%M')
        #一周时提醒
        if (dead_time - now_time) <= datetime.timedelta(days=7):
            g.msgbox(msg='尊敬的用户，您的部落 %s\n捐兵服务在一周内即将到期！\n服务结束时间：%s\n祝您游戏愉快！' %(coc_clan_name,dead_time_hr))

#提交信息，保存到csv表中
def submit():
    clarm()
    # 获取输入信息
    info = get_coc_info()
    coc_id = info[0]
    coc_name = get_coc_name(coc_id)
    coc_clan_name = info[1]
    srv_month = info[2]
    money = info[3]
    #判断是否存在coc_customer.csv
    if 'coc_customer.csv' in os.listdir():
        # 如果存在表
        # 判断表中是否已经存在该客户信息，存在就更新数据，不存在就插入数据
        table = select_tb('coc_customer.csv')
        # 去除表头
        # table.pop(0)
        # 核对用户部落名
        index = -1 #记录用户的index
        flag = False #记录是否有该用户名称

        for column in table:
            info = column.split(',')
            if coc_clan_name == info[2]:
                flag = True
                index += 1
                break#出现后立刻跳出
            else:
                index += 1
        if flag == True:
            # 有用户，更新
            values = table[index].split(',')
            time_srv = renewal(srv_month,values)
            #print(time_srv)
            start_time_hr = time_srv[0]
            dead_time_hr = time_srv[1]
            srv_days_hr = time_srv[2]
            update_tb('coc_customer.csv',[coc_id, coc_name, coc_clan_name, start_time_hr, dead_time_hr, srv_days_hr, money])
        elif flag == False: #新用户，插入新数据
                # 插入新用户信息
                time_srv = deadtime(srv_month)
                start_time_hr = time_srv[0]
                dead_time_hr = time_srv[1]
                srv_days_hr = time_srv[2]
                insert_tb('coc_customer.csv',[coc_id, coc_name, coc_clan_name, start_time_hr, dead_time_hr, srv_days_hr, money])
    else:
        # 如果不存在表，就直接建表，并插入数据
        # 插入新用户信息
        time_srv = deadtime(srv_month)
        start_time_hr = time_srv[0]
        dead_time_hr = time_srv[1]
        srv_days_hr = time_srv[2]
        create_tb('coc_customer.csv',["模拟器id", "模拟器别名", "用户部落名", "开始服务时间", "结束服务时间", "总服务时间(天)", "总消费金额"])
        insert_tb('coc_customer.csv',[coc_id, coc_name, coc_clan_name, start_time_hr, dead_time_hr, srv_days_hr, money])
        select_tb('coc_customer.csv')

def start():
    try:
        root = tk.Tk()
        root.title('部落冲突客户信息')
        #模拟器id
        coc_id_lb = tk.Label(root, text='模拟器的ID')
        coc_id_lb.grid(row=0, column=1, sticky='w',padx=10,pady=10)  # 左对齐
        global coc_id_ny,coc_clan_name_ny,coc_srv_month_ny,coc_money_ny
        coc_id_ny = tk.Entry(root)
        coc_id_ny.insert(0,'6')#插入初始化文本
        coc_id_ny.grid(row=0, column=2,padx=10)
        #客户部落名称
        coc_clan_name_lb = tk.Label(root, text='客户部落名称')
        coc_clan_name_lb.grid(row=1, column=1, sticky='w',padx=10,pady=10)  # 左对齐
        coc_clan_name_ny = tk.Entry(root)
        coc_clan_name_ny.insert(0,'叙利亚军团')#插入初始化文本
        coc_clan_name_ny.grid(row=1, column=2,padx=10)
        #服务月数
        coc_srv_month_lb = tk.Label(root, text='服务月数')
        coc_srv_month_lb.grid(row=2, column=1, sticky='w',padx=10,pady=10)  # 左对齐
        coc_srv_month_ny = tk.Entry(root)
        coc_srv_month_ny.insert(0,1)#插入初始化文本
        coc_srv_month_ny.grid(row=2, column=2,padx=10)
        #收入金额
        coc_money_lb = tk.Label(root, text='收入金额')
        coc_money_lb.grid(row=3, column=1, sticky='w',padx=10,pady=10)  # 左对齐
        coc_money_ny = tk.Entry(root)
        coc_money_ny.insert(0,50)#插入初始化文本
        coc_money_ny.grid(row=3, column=2,padx=10)
        #确认按钮
        coc_submit_bt = tk.Button(root,text='提交',width = 20,command=submit)
        coc_submit_bt.grid(row=4, column=1,columnspan=3,sticky='w'+'e',padx=10,pady=10)

        root.mainloop()
    except:
        root.destroy()

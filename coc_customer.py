import datetime
from csv_ctrl import *
import os
import tkinter as tk
import easygui as g

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
    #替换需要替换的字段：奶号id，奶号名字，结束服务时间,总服务时间,总消费金额，状态
    table[index] = table[index].replace('\r\n','')
    info = table[index].split(',')
    coc_id = str(values[0])
    coc_name = str(values[1])
    coc_clan_name = str(values[2])
    start_time = values[3]
    dead_time = values[4]
    srv_time = int(info[5]) + int(values[5])
    money = int(info[6]) + int(values[6])
    status = values[7]
    table[index] = table[index].replace(info[0],coc_id)
    table[index] = table[index].replace(info[1],coc_name)
    table[index] = table[index].replace(info[3],start_time)
    table[index] = table[index].replace(info[4],dead_time)
    table[index] = table[index].replace(info[5],str(srv_time))
    table[index] = table[index].replace(info[6],str(money))
    table[index] = table[index].replace(info[7],str(status))
    #将更新后的table直接覆盖写入到表中
    # 创建文件对象
    with open(tbname,'w',encoding='gb2312',newline="") as f:
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
    if (coc_id,coc_clan_name,srv_month) == (None,None,None) and money != None:
        coc_id,coc_clan_name,srv_month = 0,'部落首领转让',0
    return (int(coc_id),coc_clan_name,int(srv_month),int(money))

#根据模拟器id获取信息
def get_coc_name(coc_id):
    coc_config = r'D:\Program Files\DundiEmu\DundiData\avd\dundi%d\config.ini' % (coc_id)
    with open(coc_config, 'r') as file:
        configlines = file.readlines()
        for configline in configlines:
            if 'EmulatorTitleName' in configline:
                coc_name = configline.split('=')[-1].rstrip('\n')
    #coc_name = '星陨'
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
    g.msgbox(msg='尊敬的用户，您的服务已经开始为您服务！\n服务开始时间为：%s\n一共服务时间：%d 天\n服务结束时间：%s\n用户须知：\n1、每天凌晨0:30 - 6:00是打资源时间段；\n2、默认兵种：胖子、法师、气球、皮卡、飞龙、飞龙宝宝、雷龙、雪怪、野猪骑士、女武神；攻城武器：车、气球；可以指定兵种，也可以识别文字，如果文字识别失败默认捐气球；\n默认药水：雷电、狂暴、冰冻、毒药、地震、急速；\n3、如果游戏版本更新，我们会尽快在当天实现版本更新为您提供服务；\n4、为了不影响其他用户，原则上捐兵兵种仅在晚上做变更，兵种种类(包含攻城武器)<=14,总兵力<=500，药水种类<=7,总药水<=20；\n5、在线4小时会自动下线，会有15分钟强制下线时间，请等待20分钟，如果还是未上线，详情请联系我。\n有疑问请随时联系我,祝您游戏愉快！' %(start_time_hr,srv_days_hr,dead_time_hr),title='用户信息')
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
    now_time = datetime.datetime.now()#当前时间
    if now_time > dead_time:#当前时间已经超过了截止时间，从当前时间+续费时间
        dead_time = now_time + srv_days
    else:
        #结束时间
        dead_time = dead_time + srv_days
    dead_time_hr = dead_time.strftime('%Y-%m-%d %H:%M')
    #打印结果
    g.msgbox(msg='尊敬的用户，您的部落 %s\n捐兵服务已经续费成功！\n续费服务时间：%d 天\n服务结束时间：%s\n祝您游戏愉快！' %(coc_clan_name,srv_days_hr,dead_time_hr), title='用户信息')
    print('尊敬的用户，您的服务已经续费成功！\n续费服务时间：%d 天\n服务结束时间：%s\n祝您游戏愉快！' %(srv_days_hr,dead_time_hr))
    return (start_time_hr,dead_time_hr,srv_days_hr)

#提醒续费
def clarm(tbname):
    # 当前时间
    now_time = datetime.datetime.now()
    table = select_tb(tbname)
    #去除表头
    table.pop(0)
    for column in table:
        column = column.replace('\r\n','')
        info = column.split(',')
        coc_id = info[0]
        coc_name = info[1]#部落对应奶号
        coc_clan_name = info[2]#部落名称
        start_time_hr = info[3]#开始时间
        dead_time_hr = info[4]#截止时间
        srv_days_hr = 0 #不改变服务时间
        money = 0 #不改变收入
        try:
            status = info[7]
        except:
            status = 'running'
        #转换截止时间
        dead_time = datetime.datetime.strptime(str(dead_time_hr), '%Y-%m-%d %H:%M')
        #一周时提醒
        if status == 'running':#状态为正常运行服务的用户才需要提醒
            if datetime.timedelta(days=6) <= (dead_time - now_time) <= datetime.timedelta(days=7):
                g.msgbox(msg='尊敬的用户，您的部落 %s ，奶号 %s\n捐兵服务在一周内即将到期！\n服务结束时间：%s\n为了不影响您正常捐收兵，还请及时续费，很高兴为您服务，祝您游戏愉快！' %(coc_clan_name,coc_name,dead_time_hr))
            elif datetime.timedelta(days=0) <= (dead_time - now_time) <= datetime.timedelta(days=1):
                g.msgbox(msg='尊敬的用户，您的部落 %s ，奶号 %s\n捐兵服务在 24 小时内 即将到期！\n服务结束时间：%s\n为了不影响您正常捐收兵，还请及时续费，很高兴为您服务，祝您游戏愉快！' %(coc_clan_name,coc_name,dead_time_hr))
            elif (dead_time - now_time) < datetime.timedelta(days=0):#过期如果不点击已停止，会一直提醒
                flag_deadtime = g.buttonbox(msg='部落 %s ，奶号 %s\n捐兵服务已经到期！\n服务结束时间：%s\n确认是否已停止！'%(coc_clan_name,coc_name,dead_time_hr), title='确认停止服务',
                            choices=('已停止', '暂不停止服务'))
                if flag_deadtime == '已停止':
                    status = 'stop'
                    update_tb(tbname, [coc_id, coc_name, coc_clan_name, start_time_hr, dead_time_hr, srv_days_hr, money, status])

#查询信息
def query(tbname):
    clarm(tbname)
    table = select_tb(tbname)
    # 去除表头
    # table.pop(0)
    money = 0#统计总金额
    table_new = []
    for column in table:
        info = column.split(',')
        try:
            money += int(info[6])
        except ValueError as reason:
            print('没有该数据：%s' %(reason))
        column_new = column.replace('\r\n', '\n')
        table_new.append(column_new)
    table_new.append('总收入金额：%d' %(money))
    g.msgbox(table_new)

#提交信息，保存到csv表中
def submit(tbname):
    clarm(tbname)
    # 获取输入信息
    info = get_coc_info()
    coc_id = info[0]
    coc_name = get_coc_name(coc_id)
    coc_clan_name = info[1]
    srv_month = info[2]
    money = info[3]
    #判断是否存在coc_customer.csv
    if tbname in os.listdir():
        # 如果存在表
        # 判断表中是否已经存在该客户信息，存在就更新数据，不存在就插入数据
        table = select_tb(tbname)
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
            status = 'running'#续费后更新为running
            #print(time_srv)
            start_time_hr = time_srv[0]
            dead_time_hr = time_srv[1]
            srv_days_hr = time_srv[2]
            update_tb(tbname,[coc_id, coc_name, coc_clan_name, start_time_hr, dead_time_hr, srv_days_hr, money, status])
        elif flag == False: #新用户，插入新数据
                # 插入新用户信息
                status = 'running'
                time_srv = deadtime(srv_month)
                start_time_hr = time_srv[0]
                dead_time_hr = time_srv[1]
                srv_days_hr = time_srv[2]
                insert_tb('coc_customer.csv',[coc_id, coc_name, coc_clan_name, start_time_hr, dead_time_hr, srv_days_hr, money, status])
    else:
        # 如果不存在表，就直接建表，并插入数据
        # 插入新用户信息
        status = 'running'
        time_srv = deadtime(srv_month)
        start_time_hr = time_srv[0]
        dead_time_hr = time_srv[1]
        srv_days_hr = time_srv[2]
        create_tb('coc_customer.csv',["模拟器id", "模拟器别名", "用户部落名", "开始服务时间", "结束服务时间", "总服务时间(天)", "总消费金额","运行状态"])
        insert_tb('coc_customer.csv',[coc_id, coc_name, coc_clan_name, start_time_hr, dead_time_hr, srv_days_hr, money, status])
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
        coc_id_ny.insert(0,'0')#插入初始化文本
        coc_id_ny.grid(row=0, column=2,padx=10,pady=10)
        #客户部落名称
        coc_clan_name_lb = tk.Label(root, text='客户部落名称')
        coc_clan_name_lb.grid(row=1, column=1, sticky='w',padx=10,pady=10)  # 左对齐
        coc_clan_name_ny = tk.Entry(root)
        coc_clan_name_ny.insert(0,'天空之城')#插入初始化文本
        coc_clan_name_ny.grid(row=1, column=2,padx=10,pady=10)
        #服务月数
        coc_srv_month_lb = tk.Label(root, text='服务月数')
        coc_srv_month_lb.grid(row=2, column=1, sticky='w',padx=10,pady=10)  # 左对齐
        coc_srv_month_ny = tk.Entry(root)
        coc_srv_month_ny.insert(0,1)#插入初始化文本
        coc_srv_month_ny.grid(row=2, column=2,padx=10,pady=10)
        #收入金额
        coc_money_lb = tk.Label(root, text='收入金额')
        coc_money_lb.grid(row=3, column=1, sticky='w',padx=10,pady=10)  # 左对齐
        coc_money_ny = tk.Entry(root)
        coc_money_ny.insert(0,50)#插入初始化文本
        coc_money_ny.grid(row=3, column=2,padx=10,pady=10)
        #查询按钮
        coc_query_bt = tk.Button(root,text='查询',width = 20,command=lambda :query('coc_customer.csv'))
        coc_query_bt.grid(row=4, column=1,sticky='w'+'e',padx=10,pady=10)
        #提交按钮
        coc_submit_bt = tk.Button(root,text='提交',width = 20,command=lambda :submit('coc_customer.csv'))
        coc_submit_bt.grid(row=4, column=2,sticky='w'+'e',padx=10,pady=10)

        root.mainloop()
    except:
        root.destroy()

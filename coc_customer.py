import datetime
from csv_ctrl import *
import os
import tkinter as tk
import easygui as g
import win32gui
import win32con
import win32clipboard as w
import win32api,subprocess
import time
from pandas import read_excel 
from rreplace import rreplace
from xlsx_ctrl import *
from config_ctrl import *

reportFile = r"部落冲突客户信息.xlsx"
cocSheet = r"部落冲突"
try:
    donateids_for_paid_server01 = config_read(r'\\server01\\tool\\Config.ini','coc','donateids_for_paid').split()
    donateids_for_paid_server02 = config_read(r'\\server02\\tool\\Config.ini','coc','donateids_for_paid').split()
except:
    donateids_for_paid_server01 = [ "9","10","11" ]
    donateids_for_paid_server02 = [ "1","2","3","4","5","6","7","8" ]
    
def get_server(coc_id):
    coc_id = str(coc_id)
    if coc_id == 0:
        server_name = ""
    elif coc_id in donateids_for_paid_server01:
        server_name = "server_01"
    elif coc_id in donateids_for_paid_server02:
        server_name = "server_02"
    else:
        server_name = "server_03"
    return (server_name)

def openfile(excelFile):
    subprocess.Popen(excelFile,shell=True)
    
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
    if coc_id in [0,'0','']:#id为空不更新id和coc_name
        coc_id = info[0]
        coc_name = info[1]
    coc_clan_name = str(values[2])
    start_time = values[3]
    dead_time = values[4]
    srv_time = int(info[5]) + int(values[5])
    money_last = int(values[6]) #本月收入替换上月收入
    money_all = int(info[7]) + int(values[7])
    status = values[8]
    coc_customer = values[9]
    server_name = values[10]
    table[index] = table[index].replace(info[0],coc_id,1)
    table[index] = table[index].replace(info[1],coc_name,1)
    table[index] = table[index].replace(info[3],start_time,1)
    table[index] = table[index].replace(info[4],dead_time,1)
    table[index] = table[index].replace(info[5],str(srv_time),1)
    table[index] = table[index].replace(info[6],str(money_last),1)#加上替换次数，不然会因为第一个月收入与总收入一致导致把总收入也替换了
    table[index] = rreplace(table[index],info[7],str(money_all),1)#从右往左替换，不然第一个月总收入和收入一致导致只替换第一个月收入
    table[index] = table[index].replace(info[8],str(status),1)
    #table[index] = table[index].replace(info[9],str(coc_customer),1) 用户续费自然不更新用户
    if server_name != "":#不为空才替换
        table[index] = table[index].replace(info[10],str(server_name),1)
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
    money_last = coc_money_ny.get()
    coc_customer = coc_customer_ny.get()
    server_name = get_server(coc_id)
    if (coc_id,coc_clan_name,srv_month) == ("","","") and money_last != "":
        coc_id,coc_clan_name,srv_month = 0,'部落首领转让',0
    return (int(coc_id),coc_clan_name,float(srv_month),int(money_last),coc_customer,server_name)

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
def deadtime(month,coc_name):
    #month==租的月数
    # 当前时间
    start_time = datetime.datetime.now()
    start_time_hr = start_time.strftime('%Y-%m-%d %H:%M')
    #捐兵服务时间31天算一个月
    srv_days_hr = int(31 * month)
    srv_days = datetime.timedelta(days=srv_days_hr)
    #结束时间
    dead_time = start_time + srv_days
    dead_time_hr = dead_time.strftime('%Y-%m-%d %H:%M')
    #打印结果
    message = '尊敬的用户，捐兵奶号：%s 已经开始为您服务！\n服务开始时间为：%s\n一共服务时间：%d 天\n服务结束时间：%s\n用户须知：\n1、每天凌晨0:00 - 6:30是打资源时间段；\n2、默认兵种：胖子、法师、气球、皮卡、飞龙、飞龙宝宝、雷龙、雪怪、野猪骑士、女武神；攻城武器：车、气球；可以指定兵种，也可以识别文字，如果文字识别失败默认捐气球；\n默认药水：雷电、狂暴、冰冻、毒药、地震、急速；\n3、如果游戏版本更新，我们会尽快在当天实现版本更新为您提供服务；\n4、为了不影响其他用户，原则上捐兵兵种仅在晚上做变更，兵种种类(包含攻城武器)<=14,总兵力<=500，药水种类<=7,总药水<=20；\n5、在线4小时会自动下线，会有15分钟强制下线时间，请等待20分钟，如果还是未上线，详情请联系我。\n有疑问请随时联系我,祝您游戏愉快！' %(coc_name,start_time_hr,srv_days_hr,dead_time_hr)
    g.msgbox(msg=message,title='用户信息')
    setText(message)
    return (start_time_hr,dead_time_hr,srv_days_hr)

def setText(message):   #重设剪贴板文本
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_UNICODETEXT, message)
    w.CloseClipboard()    
    
def send_qq(message):   #发送消息给QQ用户
    setText(message)
    hwnd_title = dict()    
    def get_all_hwnd(hwnd,mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            hwnd_title.update({hwnd:win32gui.GetWindowText(hwnd)})
    
    win32gui.EnumWindows(get_all_hwnd, 0)
    for h,t in hwnd_title.items():
        if t != "":                    
            hwnd = win32gui.FindWindow('TXGuiFoundation', t)    # 获取qq窗口句柄    
            if hwnd != 0:
                #win32gui.SendMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)    #虽然可以还原最小化的会话窗口，但经过测试发现并不能解决还原后不发送消息的问题。
                win32gui.ShowWindow(hwnd,win32con.SW_SHOW)
                time.sleep(1)
                win32gui.SetForegroundWindow(hwnd)
                win32gui.SetActiveWindow(hwnd)
                time.sleep(3)
                win32gui.SendMessage(hwnd,770, 0, 0)    # 将剪贴板文本发送到QQ窗体
                # win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)  #模拟按下回车键
                # win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)  #模拟松开回车键
                
    
def open_windows(coc_clan_dict):     #打开QQ和wechat会话窗口，发送消息
    try:
        qq_hwnd = win32gui.FindWindow(None, 'QQ') 
        wechat_hwnd = win32gui.FindWindow(None, '微信') 
        print("捕捉到QQ主窗体的句柄为:"+str(qq_hwnd))
        print("捕捉到微信主窗体的句柄为:"+str(wechat_hwnd))
        win32gui.ShowWindow(qq_hwnd,win32con.SW_SHOW)
        #win32gui.ShowWindow(wechat_hwnd,win32con.SW_SHOW)
        print("正在打开会话窗口...\n")
        time.sleep(1)
        for coc_clan_name in coc_clan_dict:
            #打开会话窗口
            setText(coc_clan_name)
            win32api.keybd_event(13, 0, 0, 0)
            win32gui.SetForegroundWindow(qq_hwnd)
            win32gui.SetActiveWindow(qq_hwnd)
            time.sleep(1)
            win32gui.SendMessage(qq_hwnd,770, 0, 0)
            time.sleep(1)
            win32gui.SetForegroundWindow(qq_hwnd)
            win32gui.SetActiveWindow(qq_hwnd)
            win32api.keybd_event(0x0D, win32api.MapVirtualKey(0x0D, 0), 0, 0)   
            win32api.keybd_event(0x0D, win32api.MapVirtualKey(0x0D, 0), win32con.KEYEVENTF_KEYUP, 0)
            #发送信息
            send_qq(coc_clan_dict[coc_clan_name])
    except:
        print("没有找到QQ或微信程序")
#续费
def renewal(month,values):
    #获取原始信息
    start_time_hr = values[3]
    dead_time_hr = values[4]
    coc_clan_name = values[2]
    coc_customer = values[9]#用户名
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
    coc_clan_dict = {}#续费部落和信息 {'用户名':'信息'}
    #打印结果
    message = '尊敬的用户，您的部落 %s\n捐兵服务已经续费成功！\n续费服务时间：%d 天\n服务结束时间：%s\n祝您游戏愉快！' %(coc_clan_name,srv_days_hr,dead_time_hr)
    coc_clan_dict[coc_customer] = message#添加到续费部落和信息 {'用户名':'信息'}
    g.msgbox(msg=message, title='用户信息')
    open_windows(coc_clan_dict)#打开对应部落冲突部落QQ和wechat会话窗口，并发送消息
    setText(message)
    return (start_time_hr,dead_time_hr,srv_days_hr)


#提醒续费
def clarm(tbname):
    # 当前时间
    now_time = datetime.datetime.now()
    table = select_tb(tbname)
    #去除表头
    table.pop(0)
    coc_clan_dict = {}#到期部落和信息 {'部落':'信息'}
    for column in table:
        column = column.replace('\r\n','')
        info = column.split(',')
        coc_id = info[0]
        coc_name = info[1]#部落对应奶号
        coc_clan_name = info[2]#部落名称
        start_time_hr = info[3]#开始时间
        dead_time_hr = info[4]#截止时间
        srv_days_hr = info[5]
        money_last = info[6]
        money_all = info[7]
        try:
            status = info[8]
        except:
            status = 'running'
        coc_customer = info[9]#用户名
        #转换截止时间
        dead_time = datetime.datetime.strptime(str(dead_time_hr), '%Y-%m-%d %H:%M')
        #3天时提醒
        if status == 'running':#状态为正常运行服务的用户才需要提醒
            if datetime.timedelta(days=2) <= (dead_time - now_time) <= datetime.timedelta(days=3):
                message = '尊敬的用户：%s，您的部落 %s : %s ，奶号 %s\n捐兵服务在3天内即将到期！\n服务结束时间：%s\n为了不影响您正常捐收兵，还请及时续费，续费金额：%s元\n很高兴为您服务，祝您游戏愉快！' %(coc_customer,coc_id,coc_clan_name,coc_name,dead_time_hr,money_last)
                coc_clan_dict[coc_customer] = message#添加到到期部落和信息 {'用户名':'信息'}
                g.msgbox(msg=message)
                open_windows(coc_clan_dict)#打开对应部落冲突部落QQ和wechat会话窗口，并发送消息
                setText(message)
            elif datetime.timedelta(days=0) <= (dead_time - now_time) <= datetime.timedelta(days=1):
                message = '尊敬的用户：%s，您的部落 %s : %s ，奶号 %s\n捐兵服务在 24 小时内 即将到期！\n服务结束时间：%s\n为了不影响您正常捐收兵，还请及时续费，续费金额：%s元\n很高兴为您服务，祝您游戏愉快！' %(coc_customer,coc_id,coc_clan_name,coc_name,dead_time_hr,money_last)
                coc_clan_dict[coc_customer] = message#添加到到期部落和信息 {'用户名':'信息'}
                g.msgbox(msg=message)
                open_windows(coc_clan_dict)#打开对应部落冲突部落QQ和wechat会话窗口，并发送消息
                setText(message)
            elif (dead_time - now_time) < datetime.timedelta(days=0):#过期如果不点击已停止，会一直提醒
                flag_deadtime = g.buttonbox(msg='部落 %s : %s ，奶号 %s\n捐兵服务已经到期！\n服务结束时间：%s\n确认是否已停止！'%(coc_id,coc_clan_name,coc_name,dead_time_hr), title='确认停止服务',
                            choices=('已停止', '暂不停止服务'))
                if flag_deadtime == '已停止':
                    status = 'stop'
                    update_tb(tbname, [coc_id, coc_name, coc_clan_name, start_time_hr, dead_time_hr, srv_days_hr, money_last, 0, status,coc_customer,server_name])

        elif status == 'stop':
            pass

    
#查询信息
def query(tbname):
    clarm(tbname)
    table = select_tb(tbname)
    # 去除表头
    # table.pop(0)
    deleteWS(reportFile,cocSheet)
    money_income_all = 0#统计总金额
    table_new = []
    for column in table:
        info = column.split(',')
        try:
            money_income_all += int(info[7])
        except ValueError as reason:
            print('没有该数据：%s' %(reason))
        column_new = column.replace('\r\n', '\n')
        table_new.append(column_new)
        writeXlsx(reportFile,column_new.split(","))
    #table_new.append('总收入金额：%d' %(money_income_all))
    openfile(reportFile)
    g.msgbox('总收入金额：%d' %(money_income_all))

#提交信息，保存到csv表中
def submit(tbname):
    #clarm(tbname)
    # 获取输入信息
    info = get_coc_info()
    coc_id = info[0]
    coc_name = get_coc_name(coc_id)#获取账号的部落冲突名
    coc_clan_name = info[1]
    srv_month = info[2]
    money_last = info[3]
    money_all = info[3]
    coc_customer = info[4]
    if coc_customer == "":#不输入用户名默认是部落名
        coc_customer = coc_clan_name
    server_name = info[5]
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
            update_tb(tbname,[coc_id, coc_name, coc_clan_name, start_time_hr, dead_time_hr, srv_days_hr, money_last, money_all, status,coc_customer,server_name])
        elif flag == False: #新用户，插入新数据
                # 插入新用户信息
                status = 'running'
                time_srv = deadtime(srv_month,coc_name)
                start_time_hr = time_srv[0]
                dead_time_hr = time_srv[1]
                srv_days_hr = time_srv[2]
                insert_tb('coc_customer.csv',[coc_id, coc_name, coc_clan_name, start_time_hr, dead_time_hr, srv_days_hr, money_last, money_all, status,coc_customer,server_name])
    else:
        # 如果不存在表，就直接建表，并插入数据
        # 插入新用户信息
        status = 'running'
        time_srv = deadtime(srv_month,coc_name)
        start_time_hr = time_srv[0]
        dead_time_hr = time_srv[1]
        srv_days_hr = time_srv[2]
        create_tb('coc_customer.csv',["模拟器id", "模拟器别名", "用户部落名", "开始服务时间", "结束服务时间", "总服务时间(天)", "上次消费金额", "总消费金额","运行状态","服务器名"])
        insert_tb('coc_customer.csv',[coc_id, coc_name, coc_clan_name, start_time_hr, dead_time_hr, srv_days_hr, money_last, money_all, status,coc_customer,server_name])
        select_tb('coc_customer.csv')

def start():
    try:
        root = tk.Tk()
        root.title('部落冲突客户信息')
        #模拟器id
        coc_id_lb = tk.Label(root, text='模拟器的ID')
        coc_id_lb.grid(row=0, column=1, sticky='w',padx=10,pady=10)  # 左对齐
        global coc_id_ny,coc_clan_name_ny,coc_srv_month_ny,coc_money_ny,coc_customer_ny
        coc_id_ny = tk.Entry(root)
        coc_id_ny.insert(0,'0')#插入初始化文本
        coc_id_ny.grid(row=0, column=2,padx=10,pady=10)
        #客户名称
        coc_customer_lb = tk.Label(root, text='客户名称')
        coc_customer_lb.grid(row=1, column=1, sticky='w',padx=10,pady=10)  # 左对齐
        coc_customer_ny = tk.Entry(root)
        coc_customer_ny.grid(row=1, column=2,padx=10,pady=10)
        #客户部落名称
        coc_clan_name_lb = tk.Label(root, text='客户部落名称')
        coc_clan_name_lb.grid(row=2, column=1, sticky='w',padx=10,pady=10)  # 左对齐
        coc_clan_name_ny = tk.Entry(root)
        coc_clan_name_ny.insert(0,'天空之城')#插入初始化文本
        coc_clan_name_ny.grid(row=2, column=2,padx=10,pady=10)
        #服务月数
        coc_srv_month_lb = tk.Label(root, text='服务月数')
        coc_srv_month_lb.grid(row=3, column=1, sticky='w',padx=10,pady=10)  # 左对齐
        coc_srv_month_ny = tk.Entry(root)
        coc_srv_month_ny.insert(0,1)#插入初始化文本
        coc_srv_month_ny.grid(row=3, column=2,padx=10,pady=10)
        #收入金额
        coc_money_lb = tk.Label(root, text='收入金额')
        coc_money_lb.grid(row=4, column=1, sticky='w',padx=10,pady=10)  # 左对齐
        coc_money_ny = tk.Entry(root)
        coc_money_ny.insert(0,50)#插入初始化文本
        coc_money_ny.grid(row=4, column=2,padx=10,pady=10)
        #查询按钮
        coc_query_bt = tk.Button(root,text='查询',width = 20,command=lambda :query('coc_customer.csv'))
        coc_query_bt.grid(row=5, column=1,sticky='w'+'e',padx=10,pady=10)
        #提交按钮
        coc_submit_bt = tk.Button(root,text='提交',width = 20,command=lambda :submit('coc_customer.csv'))
        coc_submit_bt.grid(row=5, column=2,sticky='w'+'e',padx=10,pady=10)

        root.mainloop()
    except:
        root.destroy()

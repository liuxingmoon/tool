# -*-coding:utf-8-*-
import ssl
import urllib.request
import easygui as g
import tkinter as tk
from csv_ctrl import *
import datetime,os

def query_k():
    host = 'http://stock.market.alicloudapi.com'
    path = '/sz-sh-stock-history'
    method = 'GET'
    appcode = 'ad4f8f46057e479a97476f3a4357272a'
    query = g.multenterbox(msg='输入需要查询的时间和股票代码',title='股票K线查询',fields=['股票代码','开始时间','结束时间'],values=['','',''])
    querys = 'begin=%s&code=%s&end=%s' %(query[1],query[0],query[2])
    bodys = {}
    url = host + path + '?' + querys

    request = urllib.request.Request(url)
    request.add_header('Authorization', 'APPCODE ' + appcode)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    response = urllib.request.urlopen(request, context=ctx)
    content = response.read().decode('utf-8')
    g.msgbox(msg=content)

#获取信息
def get_info():
    money = money_ny.get()
    market_value = market_value_ny.get()
    return (money,market_value)

#查询信息
def query(tbname):
    table = select_tb(tbname)
    # 去除表头
    # table.pop(0)
    '''
    money = 0.0#统计总金额
    table_new = []
    for column in table:
        info = column.split(',')
        try:
            money += float(info[1])
        except ValueError as reason:
            print('没有该数据：%s' %(reason))
        column_new = column.replace('\r\n', '\n')
        table_new.append(column_new)
    table_new.append('总本金：%.2f' %(money))
    '''
    values = table[-1].split(',')
    principal = float(values[2])
    market_value = float(values[3])
    profit_amount = float(values[4])
    profit_percentage = values[5]
    g.msgbox('本金：%.2f\n当前市值：%.2f\n盈亏金额：%.2f\n盈亏百分比：%s' %(principal,market_value,profit_amount,profit_percentage))

def get_time():
    # 当前时间
    now_time = datetime.datetime.now()
    now_time_hr = now_time.strftime('%Y-%m-%d')
    return (now_time_hr)

def update(tbname):
    # 判断是否存在文件
    if tbname not in os.listdir():
        create_tb(tbname, ["汇入时间", "汇入金额", "本金", "当前市值", "盈亏金额", "盈亏百分比"])
        update(tbname)
    else:
        table = select_tb(tbname)
        # 去除表头
        table.pop(0)
        now_time = get_time()
        info = get_info()
        money = info[0]
        market_value = info[1]
        #如果输入没有输入市值，只输入了汇款金额，市值复制上一条数据
        if (money != '') and (market_value == ''):
            values = table[-1].split(',')
            market_value = float(values[3])
        #如果输入没有输入汇款金额，只输入了市值，当前市值更新覆盖上一条市值
        elif (money == '') and (market_value != ''):
            values = table[-1].split(',')
            now_time = values[0]
            money = values[1]
            #删掉最后一条数据
            table.pop(-1)
        #插入新数据
        principal = 0.0
        for column in table:
            info = column.split(',')
            try:
                principal += float(info[1])
            except ValueError as reason:
                print('该字段数据：%s 不是正确格式' % (reason))
        principal += float(money) #加上本次资金
        profit_amount = float(market_value) - principal
        #除数不能为0
        if principal == 0.0:
            profit_percentage = '0%'
        else:
            profit_percentage = format((profit_amount/principal), '.2%')
        values=[now_time,money,principal,market_value,profit_amount,profit_percentage]
        insert_tb(tbname,values)
    print('update')

def start():
    try:
        root = tk.Tk()
        root.title('股票信息')
        global money_ny, market_value_ny
        #汇入本金
        money_lb = tk.Label(root,text='汇入本金')
        money_lb.grid(row=0, column=1, sticky='w'+'e', padx=10, pady=10)    # 居中
        money_ny = tk.Entry(root)
        money_ny.grid(row=0, column=2, padx=10,pady=10)
        #当前市值
        market_value_lb = tk.Label(root,text='当前市值')
        market_value_lb.grid(row=1, column=1, sticky='w'+'e', padx=10, pady=10)    # 居中
        market_value_ny = tk.Entry(root)
        market_value_ny.grid(row=1, column=2, padx=10,pady=10)
        #查询
        query_bt = tk.Button(root,text='查询',width = 20,command=lambda :query('stock_info.csv'))
        query_bt.grid(row=3, column=1,sticky='w'+'e',padx=10,pady=10)
        #更新
        update_bt = tk.Button(root,text='更新',width = 20,command=lambda :update('stock_info.csv'))
        update_bt.grid(row=3, column=2,sticky='w'+'e',padx=10,pady=10)
        root.mainloop()
    except:
        root.destroy()



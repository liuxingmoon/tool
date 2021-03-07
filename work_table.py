# -*-coding:utf-8-*-
import easygui as g
import tkinter as tk
from csv_ctrl import *
import subprocess


#获取信息
def get_info():
    row = row_ny.get().split()
    column = column_ny.get().split()
    row = [int(x) for x in row]#转为int
    column = [int(x) for x in column]#转为int
    return (row,column)

def input_info(tb_all):
    subprocess.Popen(r"start %s"%(tb_all),shell=True)

def select_info(tb_all,tb_select):
    '''row和column都是一个列表，[行1，行2……]，[列1，列2……]'''
    row = get_info()[0]
    column = get_info()[1]
    table = select_tb(tb_all,[row,column])
    print(table)
    with open(tb_select, 'w', encoding='gb2312', newline="") as f:
        print("直接清空表tb_select")
    #将更新后的table直接覆盖写入到表中
    # 创建文件对象
    with open(tb_select,'w',encoding='gb2312',newline="") as f:
    # 基于文件对象构建 csv写入对象
        for line in table:
            if isinstance(line,list):#列表就直接插入
                insert_tb(tb_select,line)
            else:
                line = line.replace('\r\n','')
                insert_tb(tb_select,line.split(','))
    subprocess.Popen(r"start %s" %(tb_select),shell=True)

def start():
    try:
        root = tk.Tk()
        root.title('筛选表格')
        global row_ny, column_ny
        #汇入本金
        row_lb = tk.Label(root,text='输入行')
        row_lb.grid(row=0, column=1, sticky='w'+'e', padx=10, pady=10)    # 居中
        row_ny = tk.Entry(root)
        row_ny.grid(row=0, column=2, padx=10,pady=10)
        #当前市值
        column_lb = tk.Label(root,text='输入列')
        column_lb.grid(row=1, column=1, sticky='w'+'e', padx=10, pady=10)    # 居中
        column_ny = tk.Entry(root)
        column_ny.insert(0,'0 1 2 3 4')
        column_ny.grid(row=1, column=2, padx=10,pady=10)
        #查询
        query_bt = tk.Button(root,text='输入信息',width = 20,command=lambda :input_info('work.csv'))
        query_bt.grid(row=3, column=1,sticky='w'+'e',padx=10,pady=10)
        #更新
        update_bt = tk.Button(root,text='筛选信息',width = 20,command=lambda :select_info('work.csv','work_select.csv'))
        update_bt.grid(row=3, column=2,sticky='w'+'e',padx=10,pady=10)
        root.mainloop()
    except:
        root.destroy()



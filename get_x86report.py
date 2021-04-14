#!python3
# --*-- coding: utf-8 --*--

import os
import glob
from openpyxl import load_workbook
import xlrd
import pdb
from file_ctrl import *
import threading
import datetime

weekReportDir = r"D:\Program Files\Python38\works\tool\weekReport"
weekReportDir_tradition = r"D:\SVNdata\Public\01.AB组周报\传统架构组\2021年"
weekReportDir_cloud = r"D:\SVNdata\Public\01.AB组周报\云平台组周报"
totalFile = r"C:\Users\Administrator.PC-20200904VSVM\Desktop\x86_weekreport.txt"

def turnStr(L):
    """ 把列表里所有元素转换为字符串型 """
    tmpL = list(map(lambda x: str(x), L))
    return tmpL

def readXls(excelFile):
    row_pd = 0
    row_ha = 0
    row_prog = 0
    row_tool = 0
    row_special = 0
    row_other = 0
    row_end = 0
    wb = xlrd.open_workbook(excelFile)
    ws = wb.sheets()[0]
    nrows = ws.nrows
    # 
    data = []
    for row_num in range(1,nrows):
        celldata = ws.cell_value(row_num,1)
        if celldata:
            if celldata == "上周安排工作完成情况":
                data.append(celldata)
                break
            else:
                data.append(celldata)
        else:
            continue
    # 
    for ind,celldata in enumerate(data):
        #print("{} === {}".format(ind, celldata))
        if celldata == "生产运行保障":
            row_pd = ind
        if celldata == "高可用性管理":
            row_ha = ind  
        if celldata == "项目支持":
            row_prog = ind 
        if celldata == "工具建设":
            row_tool = ind
        if celldata == "专项工作":
            row_special = ind
        if celldata == "其他工作":
            row_other = ind
        if celldata == "上周安排工作完成情况":
            row_end = ind
            break

    excelData = [
        data[(row_pd +1):row_ha],
        data[(row_ha +1):row_prog],
        data[(row_prog +1):row_tool],
        data[(row_tool +1):row_special],
        data[(row_special +1):row_other],
        data[(row_other +1):row_end],
    ]
    return excelData


def readXlsx(excelFile):
    row_pd = 0
    row_ha = 0
    row_prog = 0
    row_tool = 0
    row_special = 0
    row_other = 0
    
    wb = load_workbook(excelFile)
    ws = wb.active
    
    for c in ws.rows:
        if c[1].value:
            if c[1].value == "生产运行保障":
                row_pd = c[1].row + 1
            elif c[1].value == "高可用性管理":
                row_ha = c[1].row + 1
            elif c[1].value == "项目支持":
                row_prog = c[1].row + 1
            elif c[1].value == "工具建设":
                row_tool = c[1].row + 1
            elif c[1].value == "专项工作":
                row_special = c[1].row + 1
            elif c[1].value == "其他工作":
                row_other = c[1].row + 1          
            elif c[1].value == "上周安排工作完成情况":
                break
            else:
                continue
        else:
            continue
        
    return [
        ws.cell(row_pd, 2).value.split("\n") if ws.cell(row_pd, 2).value else [],
        ws.cell(row_ha, 2).value.split("\n") if ws.cell(row_ha, 2).value else [],
        ws.cell(row_prog, 2).value.split("\n") if ws.cell(row_prog, 2).value else [],
        ws.cell(row_tool, 2).value.split("\n") if ws.cell(row_tool, 2).value else [],
        ws.cell(row_special, 2).value.split("\n") if ws.cell(row_special, 2).value else [],
        ws.cell(row_other, 2).value.split("\n") if ws.cell(row_other, 2).value else [],
        ]

def clean_weekdir():
    os.chdir(weekReportDir)
    filelist = os.listdir()
    rm_filelist = [x for x in filelist if x != "x86_weekreport.txt"]
    for rm_file in rm_filelist:
        os.remove(rm_file)
        
        
def getfilelist(filedir):
    os.chdir(filedir)
    last_dir = max([ datetime.datetime.strptime( dir_name, '%Y-%m-%d') for dir_name in os.listdir() ])#最新的时间的目录
    last_dir = last_dir.strftime("%Y-%m-%d")
    os.chdir(last_dir)#进入到最新的目录
    file_list = os.listdir()#周报列表
    return(last_dir,file_list)
    
def copy_file_to_weekdir(filedir):
    last_dir = getfilelist(filedir)[0]
    file_list = getfilelist(filedir)[1]
    for filename in file_list:
        thread_copyfile =threading.Thread(target=copy_file,args=(filename,filedir + os.sep + last_dir,weekReportDir))#从当前目录拷贝文件到汇总目录
        thread_copyfile.start()
    
def start():
    # TODO: 检查周报是否交齐,
    # x86_members = ["任德强","张文强","刁强",]
    
    work = {"生产运行保障":[], 
        "高可用性管理":[], 
        "项目支持":[],
        "工具建设":[],
        "专项工作": [],
        "其他工作":[]
    }
    
    clean_weekdir()#清空周报文件
    copy_file_to_weekdir(weekReportDir_tradition)#复制周报文件
    copy_file_to_weekdir(weekReportDir_cloud)#复制周报文件
    
    os.chdir(weekReportDir)
    for excel in glob.glob('工作周报-*.xls*'):
        print(f"正在处理 {excel} ...")
        if os.path.splitext(excel)[-1] == ".xlsx":  
            data = readXlsx(excel)
        elif os.path.splitext(excel)[-1] == ".xls":  
            data = readXls(excel)
        else:
            print(f"{excel} excel格式不支持...")
            continue
            
        if data[0]:
            work["生产运行保障"] += data[0]
        if data[1]:        
            work["高可用性管理"] += data[1]
        if data[2]: 
            work["项目支持"] += data[2]
        if data[3]: 
            work["工具建设"] += data[3]
        if data[4]: 
            work["专项工作"] += data[4]
        if data[5]:
            work["其他工作"] += data[5]
    ignore_keywords = ["","无","暂无","不涉及","本周不涉及","上周安排工作完成情况"] + list(work.keys())
    with open(totalFile, "w") as fw:
        fw.write("农信x86组周报\n")
        for work_type, work_contents in work.items():
            fw.write("\n")
            fw.write("[{}]\n".format(work_type))
            if work_contents:
                for line in set(turnStr(work_contents)):
                    if line.strip() not in ignore_keywords or "本周主要工作内容如下" in line:
                        fw.write("{}\n".format(line.strip()))
            fw.write("\n")
    os.system("start %s" %(totalFile))
    os.chdir(weekReportDir)
        

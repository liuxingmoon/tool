#统计故障磁盘
from xlsx_ctrl import *
from config_ctrl import config_read
import easygui as g
import time,re,os

configpath = "Config.ini"
excelFile = config_read(configpath,'work','硬件故障记录')
print(excelFile)
excelFile = os.path.abspath(excelFile)

#excelFile = r"C:\Users\Administrator.PC-20200904VSVM\Desktop\export\disk_error_info.xlsx"
print(excelFile)

def start():
    disk_error_info = g.textbox(msg='输入损坏磁盘信息',title='硬件故障记录')
    hostname = re.findall("Local_hostname:.*",disk_error_info)[0].split(": ")[1]
    devicename = None
    nc_sn = re.findall("Serial Number:.*",disk_error_info)[0].split(": ")[1]
    factory_name = None
    rack_info = re.findall(".*\"- \".*",disk_error_info)[0].split("\"")
    room = rack_info[1] + "-" + rack_info[3]
    rack_unit = rack_info[5] + "-" + rack_info[7]
    error_dev = "硬盘：" + re.findall("\/disk.*",disk_error_info)[0].strip("\/")
    worker = "刘兴"
    time_found = time.strftime("%Y/%m/%d", time.localtime())
    time_report = time.strftime("%Y/%m/%d", time.localtime())
    time_fix = None
    fix_status = "在保"
    environment = "生产"
    cluster = re.findall("Local_cluster:.*",disk_error_info)[0].split(": ")[1]
    error_exp = "硬盘故障"
    remarks = "TAC巡检-硬盘故障,更换硬盘"
    disk_model = re.findall("Device Model:.*",disk_error_info)[0].split(":     ")[1]
    disk_sn = re.findall("Serial Number:.*",disk_error_info)[1].split(":    ")[1]
    disk_info = disk_model + "\n" + disk_sn
    data = [hostname,devicename,nc_sn,factory_name,room,rack_unit,error_dev,worker,
    time_found,time_report,time_fix,fix_status,environment,cluster,error_exp,remarks,disk_info]
    writeXlsx(excelFile,data)

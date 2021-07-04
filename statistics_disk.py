#农信统计故障设备
from xlsx_ctrl import *
from config_ctrl import config_read
import easygui as g
import time,re,os,datetime
import subprocess
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

configpath = "Config.ini"
excelFile = config_read(configpath,'work','硬件故障记录')
commit_person = config_read(configpath,'work','commit_person')
cmdb_url = r"http://10.128.128.238/report/cmdb/v_server"
wps_url = r"http://10.0.28.95/view/p/25882"
search_xpath = r"/html/body/div[2]/div[2]/div/div[2]/label/input"
factory_name_xpath = r"/html/body/div[2]/div[2]/div/div[3]/div[2]/table/tbody/tr/td[1]"
devicename_xpath = r"/html/body/div[2]/div[2]/div/div[3]/div[2]/table/tbody/tr/td[2]"
environment_xpath = r"/html/body/div[2]/div[2]/div/div[3]/div[2]/table/tbody/tr/td[11]"
fix_start_time_xpath = r"/html/body/div[2]/div[2]/div/div[3]/div[2]/table/tbody/tr/td[30]"
fix_end_time_xpath = r"/html/body/div[2]/div[2]/div/div[3]/div[2]/table/tbody/tr/td[31]"
fix_year_path = r"/html/body/div[2]/div[2]/div/div[3]/div[2]/table/tbody/tr/td[32]"

excelFile = r"%s" %(excelFile)
#excelFile = repr(excelFile)
#excelFile = excelFile.replace("\\","\\").replace("\t","\\t")
#excelFile = r"W:\工单\硬件故障记录.xlsx"

#excelFile = r"C:\Users\Administrator.PC-20200904VSVM\Desktop\export\device_error_info.xlsx"

def openfile(excelFile):
    subprocess.Popen(excelFile,shell=True)
    
def open_wps_cloud(wps_url):
    driver.get(wps_url)

def get_info_cmdb(nc_sn):
    global driver
    # 启用带插件的浏览器
    option = webdriver.ChromeOptions()
    #option.add_argument("headless")#无浏览器界面运行
    #option.add_argument("--disable_gpu")
    option.add_argument("--user-data-dir=" + r"C:\Users\user\AppData\Local\Google\Chrome\User Data\\")
    driver = webdriver.Chrome(chrome_options=option)   # 打开chrome浏览器
    driver.get(cmdb_url)
    driver.refresh()
    time.sleep(7)
    driver.find_element_by_xpath(search_xpath).send_keys(nc_sn)#搜索cmdb
    time.sleep(3)
    factory_name = driver.find_element_by_xpath(factory_name_xpath).text
    devicename = driver.find_element_by_xpath(devicename_xpath).text
    environment = driver.find_element_by_xpath(environment_xpath).text
    '''
    fix_start_time = driver.find_element_by_xpath(fix_start_time_xpath).text
    fix_start_time = datetime.datetime.strptime(str(fix_start_time),'%Y-%m-%d') #转换时间为datetime
    fix_year = int(driver.find_element_by_xpath(fix_year_path).text)
    srv_days = datetime.timedelta(days=fix_year*365)#维保服务时间天数
    '''
    fix_end_time = driver.find_element_by_xpath(fix_end_time_xpath).text
    fix_end_time = datetime.datetime.strptime(str(fix_end_time),'%Y-%m-%d') #转换时间为datetime
    now_time = datetime.datetime.now()#当前时间
    if now_time > fix_end_time:#当前时间已经超过了截止时间，不在保
        fix_status = "不在保"
    else:
        fix_status = "在保"
    return ([factory_name,devicename,environment,fix_status])
    
def start():
    subprocess.Popen('taskkill /f /t /im chrome.exe',shell=True)#关闭chrome的浏览器，不然会报错
    device_error_info = g.textbox(msg='输入故障设备信息',title='硬件故障统计')
    #devicename = None
    
    #factory_name = None
    rack_info = re.findall(".*\"- \".*",device_error_info)[0].split("\"")
    room = rack_info[1] + "-" + rack_info[3]
    rack_unit = rack_info[5] + "-" + rack_info[7]
    try:#getinfo 对接3个参数的磁盘信息
        cluster = re.findall("Local_cluster:.*",device_error_info)[0].split(": ")[1]
        hostname = re.findall("Local_hostname:.*",device_error_info)[0].split(": ")[1]
        nc_sn = re.findall("Serial Number:.*",device_error_info)[0].split(": ")[1]
        disk_dev = re.findall("\.*disk.?/sd.*",device_error_info)[0].strip("\/")
        error_dev = "硬盘：" + re.findall("\.*disk.?/sd.*",device_error_info)[0].strip("\/")
        error_exp = "硬盘故障"
        remarks = "TAC巡检-硬盘故障,更换硬盘"
        disk_model = re.findall("Device Model:.*",device_error_info)[0].split(":     ")[1]
        disk_sn = re.findall("Serial Number:.*",device_error_info)[1].split(":    ")[1]
        disk_info = disk_model + "\n" + disk_sn
        error_dev_info = disk_info
    except IndexError as reason:
        print ("无磁盘信息，损坏的设备不是磁盘")
        hostname = re.findall(".*服务器hostname.*\n.*",a)[0].split("\"")[1]
        nc_sn = re.findall(".*服务器SN.*\n.*",a)[0].split("\"")[1]
        cluster = re.findall(".*服务器集群.*\n.*",a)[0].split("\"")[1]
        error_dev = None
        error_exp = None
        remarks = None
        error_dev_info = None
    worker = commit_person
    time_found = time.strftime("%Y/%m/%d", time.localtime())
    time_report = time.strftime("%Y/%m/%d", time.localtime())
    time_fix = None
    #fix_status = "在保"
    #environment = "生产"
    info = get_info_cmdb(nc_sn)
    factory_name,devicename,environment,fix_status = info
    data = [hostname,devicename,nc_sn,factory_name,room,rack_unit,error_dev,worker,
    time_found,time_report,time_fix,fix_status,environment,cluster,error_exp,remarks,error_dev_info]
    print(data)
    writeXlsx(excelFile,data)
    openfile(excelFile)
    open_wps_cloud(wps_url)
    #subprocess.Popen('taskkill /f /t /im chromedriver.exe',shell=True)#关闭chromedriver的控制台
    #driver.quit()
    
#农信统计故障设备
from xlsx_ctrl import *
from config_ctrl import config_read
from file_ctrl import copy_file,RemoteWord
import easygui as g
import time,re,os,datetime
import subprocess
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import win32gui
from win32.lib import win32con

configpath = "Config.ini"
workdir = config_read(configpath,'work','workdir')
excelFile = "硬件故障记录.xlsx"
pangudisk_template = "pangu磁盘白屏更换流程.docx"
commit_person = config_read(configpath,'work','commit_person')
cmdb_url = r"http://10.128.128.238/report/cmdb/v_server"
wps_url_dev_report = r"http://10.0.28.95/view/p/57001"
wps_url_report = r"http://10.0.28.95/view/p/57002"
search_xpath = r"/html/body/div[2]/div[2]/div/div[2]/label/input"
factory_name_xpath = r"/html/body/div[2]/div[2]/div/div[3]/div[2]/table/tbody/tr/td[1]"
devicename_xpath = r"/html/body/div[2]/div[2]/div/div[3]/div[2]/table/tbody/tr/td[2]"
room_xpath = r"/html/body/div[2]/div[2]/div/div[3]/div[2]/table/tbody/tr/td[6]"
rack_xpath = r"/html/body/div[2]/div[2]/div/div[3]/div[2]/table/tbody/tr/td[7]"
environment_xpath = r"/html/body/div[2]/div[2]/div/div[3]/div[2]/table/tbody/tr/td[11]"
fix_start_time_xpath = r"/html/body/div[2]/div[2]/div/div[3]/div[2]/table/tbody/tr/td[30]"
fix_end_time_xpath = r"/html/body/div[2]/div[2]/div/div[3]/div[2]/table/tbody/tr/td[31]"
fix_year_path = r"/html/body/div[2]/div[2]/div/div[3]/div[2]/table/tbody/tr/td[32]"
workdir = r"%s" %(workdir)
programdir = os.getcwd()

def openfile(excelFile):
    subprocess.Popen(excelFile,shell=True)
    
def close_windows(close_name):
    close_window = win32gui.FindWindow(None, close_name)
    try:
        win32gui.PostMessage(close_window, win32con.WM_CLOSE, 0, 0)
    except:
        print ("配额不足，无法处理，跳过！")
        pass
    
def open_wps_cloud(url):
    driver.get(url)

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
    room = driver.find_element_by_xpath(room_xpath).text
    rack_cmdb = driver.find_element_by_xpath(rack_xpath).text.split('-')[-1]
    if rack_cmdb.isdigit():#只由数字，加上倒数第二个字符
        rack_cmdb = driver.find_element_by_xpath(rack_xpath).text.split('-')[-2] + rack_cmdb
    environment = driver.find_element_by_xpath(environment_xpath).text
    '''
    fix_start_time = driver.find_element_by_xpath(fix_start_time_xpath).text
    fix_start_time = datetime.datetime.strptime(str(fix_start_time),'%Y-%m-%d') #转换时间为datetime
    fix_year = int(driver.find_element_by_xpath(fix_year_path).text)
    srv_days = datetime.timedelta(days=fix_year*365)#维保服务时间天数
    '''
    now_time = datetime.datetime.now()#当前时间
    fix_end_time = driver.find_element_by_xpath(fix_end_time_xpath).text
    if fix_end_time == "":
        fix_status = "无截止时间"
    else:
        fix_end_time = datetime.datetime.strptime(str(fix_end_time),'%Y-%m-%d') #转换时间为datetime
        if now_time > fix_end_time:#当前时间已经超过了截止时间，不在保
            fix_status = "不在保"
        else:
            fix_status = "在保"
    return ([factory_name,devicename,environment,fix_status,room,rack_cmdb])
    
def start():
    subprocess.Popen('taskkill /f /t /im chrome.exe',shell=True)#关闭chrome的浏览器，不然会报错
    device_error_info = g.textbox(msg='输入故障设备信息',title='硬件故障统计')
    #print(device_error_info)
    #devicename = None
    #factory_name = None
    rack_info = re.findall(".*\"- \".*",device_error_info)[0].split("\"")
    rack_ali = rack_info[5]
    rack_unit_ali = rack_info[5] + "-" + rack_info[7]
    #room = rack_info[1] + "-" + rack_info[3]

    try:#getinfo 对接3个参数的磁盘信息
        cluster = re.findall("Local_cluster:.*",device_error_info)[0].split(": ")[1]
        hostname = re.findall("Local_hostname:.*",device_error_info)[0].split(": ")[1]
        IP_address = re.findall("Local_address:.*",device_error_info)[0].split(": ")[1]
        nc_sn = re.findall("Serial Number:.*",device_error_info)[0].split(": ")[1]
        try:
            disk_dev = re.findall(".*disk.*/sd.*",device_error_info)[0].strip("\/")
            disk_num = re.findall("\d+",disk_dev)[0]
            disk_name = re.findall("sd.*",disk_dev)[0]
        except IndexError as reason:
            disk_dev = re.findall(".*dev sd.*",device_error_info)[1].split(', ')[1]
        error_dev = "硬盘"
        error_exp = "硬盘故障"
        remarks = "TAC/铜雀巡检发现硬盘故障"
        try:
            disk_model = re.findall("Device Model:.*",device_error_info)[0].split(":     ")[1]
            disk_sn = re.findall("Serial Number:.*",device_error_info)[1].split(":    ")[1]
        except IndexError as reason:
            disk_model = "无法查询"
            disk_sn = "无法查询"
        disk_info = disk_model + "\n" + disk_sn
        error_dev_info = disk_dev + "\n" + disk_info
    except IndexError as reason:
        print ("无磁盘信息，损坏的设备不是磁盘：%s" %(reason))
        if "Memory" in device_error_info:#内存故障
            try:
                error_dev = "内存: " + re.findall("DIMM location:.*",device_error_info)[0].split(": ")[-1]
            except:
                error_dev = "内存"
                print("没有找到内存故障位置!")
            error_exp = "内存故障"
            remarks = "TAC/封神榜巡检发现内存故障"
        else:
            error_dev = None
            error_exp = None
            remarks = None
        error_dev_info = None
        hostname = re.findall(".*服务器hostname.*\n.*",device_error_info)[0].split("\"")[1]
        nc_sn = re.findall(".*服务器SN.*\n.*",device_error_info)[0].split("\"")[1]
        cluster = re.findall(".*服务器集群.*\n.*",device_error_info)[0].split("\"")[1]

    worker = commit_person
    time_found = time.strftime("%Y/%m/%d", time.localtime())
    time_report = time.strftime("%Y/%m/%d", time.localtime())
    time_fix = None
    #fix_status = "在保"
    #environment = "生产"
    info = get_info_cmdb(nc_sn)
    factory_name,devicename,environment,fix_status,room,rack_cmdb = info
    print(rack_cmdb,rack_ali)
    if (rack_cmdb == rack_ali):
        rack_unit = rack_unit_ali
    else:
        rack_unit = rack_cmdb
    data = [hostname,devicename,nc_sn,factory_name,room,rack_unit,error_dev,worker,
    time_found,time_report,time_fix,fix_status,environment,cluster,error_exp,remarks,error_dev_info]
    print(data)
    try:
        writeXlsx(excelFile,data)
    except PermissionError as reason:
        close_windows(r"硬件故障记录.xlsx - WPS 表格")
        close_windows(r"硬件故障记录.xlsx")
        time.sleep(2)
        writeXlsx(excelFile,data)
    openfile(excelFile)
    open_wps_cloud(wps_url_dev_report)
    driver.execute_script('window.open("","_blank");') # 新开标签页
    driver.switch_to.window(driver.window_handles[1]) # 转到第2个标签
    open_wps_cloud(wps_url_report)
    driver.switch_to.window(driver.window_handles[0]) # 转到第1个标签
    #subprocess.Popen('taskkill /f /t /im chromedriver.exe',shell=True)#关闭chromedriver的控制台
    #driver.quit()
    #保存报告信息
    report_itsm_info = r'%s环境更换云平台%s集群%s %s的机器%s的%s %s' %(environment,cluster,room,rack_unit,devicename,error_dev,error_dev_info)
    report_daily_info = r'%s服务器%s,于%s经%s，涉及%s云%s集群，于 %s 更换故障硬盘后恢复正常，未影响系统可用性。' %(factory_name,devicename,time_report,remarks,environment,cluster,time_fix)
    if error_dev == "硬盘":
        today_time = datetime.datetime.today().strftime("%Y%m%d")
        filename = "%s-%s %s硬盘故障"%(today_time,hostname,disk_dev)
        filename = filename.replace("/"," ")
        global workdir,programdir
        workdir = workdir + os.sep + filename
        copy_file(pangudisk_template,programdir,workdir)
        filename_new = workdir + os.sep + pangudisk_template
        pos = room + " " + rack_unit
        doc = RemoteWord(filename_new)  # 初始化一个doc对象
        doc.replace_doc("生产", environment)
        doc.replace_doc("ECS-IO8River-B-5de2", cluster)
        doc.replace_doc("nxba09506.cloud.a14.qm500", hostname)
        doc.replace_doc("14.0.0.66", IP_address)
        doc.replace_doc("$disk_num", disk_num)
        doc.replace_doc("西信-西区 1F-NXBW-A-14",pos)
        doc.replace_doc("819603773",nc_sn)
        doc.replace_doc("sdm",disk_name)
        doc.replace_doc("disk12","disk%s"%(disk_num))
        doc.replace_doc("SA5212A074",devicename)
        doc.replace_doc("ST8000NM0055-1RM112",disk_model)
        doc.replace_doc("ZA1HBDEB",disk_sn)
        doc.close()
    with open('report_dev.txt','w') as rp:
        rp.write(report_itsm_info + '\n' + report_daily_info)
    os.system('report_dev.txt')


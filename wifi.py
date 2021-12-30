import tkinter as tk
import subprocess as pcs
import configparser
from read_config import configpath

config = configparser.ConfigParser()
config.read(configpath, encoding="utf-8")

#用于开启临时热点
def start():
    try:
        def getinfo():
            ssid = id_entry.get()
            pwd = pwd_entry.get()
            return (ssid,pwd)
        def startWifi():
            ssid = getinfo()[0]
            pwd = getinfo()[1]
            pcs.Popen(r'netsh wlan set hostednetwork mode=allow ssid=%s key=%s' %(ssid,pwd))
            pcs.Popen(r'netsh wlan start hostednetwork')
        def stopWifi():
            pcs.Popen(r'netsh wlan stop hostednetwork')

        root = tk.Tk()
        root.title('热点管理')
        ssid_default = config.get("wifi", "ssid")
        pwd_default = config.get("wifi", "pwd")
        id_label = tk.Label(root, text='热点id')
        id_label.grid(row=0, column=1, sticky='w',padx=10,pady=10)  # 左对齐
        id_entry = tk.Entry(root)
        id_entry.insert(0,ssid_default)#插入初始化文本
        id_entry.grid(row=0, column=2,padx=10,pady=10)
        pwd_label = tk.Label(root, text='热点密码')
        pwd_label.grid(row=1, column=1, sticky='w',padx=10,pady=10)  # 左对齐
        pwd_entry = tk.Entry(root,show='*')
        pwd_entry.insert(0,pwd_default)#插入初始化文本
        pwd_entry.grid(row=1, column=2,padx=10,pady=10)
        id_start_bt = tk.Button(root,text='开启热点', width=10, command=startWifi)
        id_start_bt.grid(row=2,column=1,padx=10,pady=10)
        id_stop_bt = tk.Button(root,text='关闭热点', width=10, command=stopWifi)
        id_stop_bt.grid(row=2, column=2,padx=10,pady=10)

        root.mainloop()
    except:
        root.destroy()
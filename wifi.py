import tkinter as tk
import subprocess as pcs


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

        id_label = tk.Label(root, text='热点id')
        id_label.grid(row=0, column=1, sticky='w')  # 左对齐
        id_entry = tk.Entry(root)
        id_entry.grid(row=0, column=2)
        pwd_label = tk.Label(root, text='热点密码')
        pwd_label.grid(row=1, column=1, sticky='w')  # 左对齐
        pwd_entry = tk.Entry(root)
        pwd_entry.grid(row=1, column=2)
        id_start_bt = tk.Button(root,text='开启热点', width=10, command=startWifi)
        id_start_bt.grid(row=2,column=1)
        id_stop_bt = tk.Button(root,text='关闭热点', width=10, command=stopWifi)
        id_stop_bt.grid(row=2, column=2)

        root.mainloop()
    except:
        root.destroy()
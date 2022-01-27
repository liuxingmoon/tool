#ecs初始化命令辅助
import tkinter as tk
import win32gui,subprocess,base64
from clip_ctrl import clip
import easygui as g
from format_ctrl import *

mapping = {
    "蜀信云":"SX",
    "信创云":"XC",
    "非生产环境":"Dev",
    "生产环境":"Prod",
    "统信系统":"UOS",
    "麒麟系统":"KylinOS",
    "CentOS7.6":"CentOS7.6"
}

def get_info(language):
    ''' True:映射en False:不映射cn '''
    cloud = cloud_listbox.get(cloud_listbox.curselection())
    environment = environment_listbox.get(environment_listbox.curselection())
    os = os_listbox.get(os_listbox.curselection())
    script = script_text.get('1.0','end')
    if language == 'en':
        cloud = mapping[cloud]
        environment = mapping[environment]
        os = mapping[os]
    return (cloud,environment,os,script)
    
def put_script(filename):
    script_text.delete('1.0','end')#清空
    with open(filename,'r') as f:
        messages = f.readlines()
    for message in messages:
        script_text.insert('end',message)
    code = "".join(messages).encode('utf-8')
    code = base64.b64encode(code)
    clip(code.decode('utf-8'))
    g.msgbox(msg=code,title='base64编码')
    
def change_script():
    cloud,environment,os,script = get_info('cn')
    code = base64.b64encode(script.encode('utf-8'))
    code = code.decode('utf-8')
    #写入base64码到文件中
    filename_cn = r'InitEcs%s%s%s.txt' %(cloud,os,environment)
    with open(filename_cn,'w') as f:
        messages = f.write(code)
    #将文件格式从windows转换为unix
    to_lf(filename_cn, True, encoding = 'utf-8')
    cloud,environment,os,script = get_info('en')
    filename_en = r'InitEcs%s%s%s.sh' %(cloud,os,environment)
    #写入源码到脚本中
    with open(filename_en,'w') as f:
        messages = f.write(script)
    g.msgbox(msg='已成功修改文件',title=filename_cn)
    
def sub_info():
    cloud,environment,os,script = get_info('en')
    filename_en = r'InitEcs%s%s%s.sh' %(cloud,os,environment)
    put_script(filename_en)#显示脚本文本


def start():
    root = tk.Toplevel()
    root.title('ecs初始化命令辅助')
    global cloud_listbox,environment_listbox,os_listbox,script_text
    #环境
    cloud_frame = tk.Frame(root)
    cloud_frame.grid(row=0,column=1,padx=10,pady=10)
    environmentlist_frame = tk.Frame(root)
    environmentlist_frame.grid(row=0,column=2,padx=10,pady=10)
    os_frame = tk.Frame(root)
    os_frame.grid(row=0,column=3,padx=10,pady=10)
    button_frame = tk.Frame(root)
    button_frame.grid(row=0,column=4,padx=10,pady=10)
    script_frame = tk.Frame(root,padx=10,pady=10)
    script_frame.grid(row=1,column=1,columnspan=4,sticky='w'+'e')
    #滚动条
    cloud_scrollerbar = tk.Scrollbar(cloud_frame)
    cloud_scrollerbar.pack(side='right',fill='y')#靠右填充
    cloud_listbox = tk.Listbox(cloud_frame,selectmode='single',#单选
                         exportselection='False',#可以让多个选择框选择互不影响
                         height=3,  # 默认只有10行，如果选项大于10项会被遮蔽
                         yscrollcommand=cloud_scrollerbar.set)#设置启用滚动条，可以滚轮滚动列表
    cloud_listbox.insert('end','蜀信云')
    cloud_listbox.insert('end','信创云')
    cloud_listbox.pack(side='left',fill='both')
    cloud_scrollerbar.config(command=cloud_listbox.yview)#绑定滚动条给列表框的y轴view（可以鼠标点击拉动滚动条）
    #滚动条
    environment_scrollerbar = tk.Scrollbar(environmentlist_frame)
    environment_scrollerbar.pack(side='right',fill='y')#靠右填充
    environment_listbox = tk.Listbox(environmentlist_frame,selectmode='single',#单选
                         exportselection='False',#可以让多个选择框选择互不影响
                         height=3,  # 默认只有10行，如果选项大于10项会被遮蔽
                         yscrollcommand=environment_scrollerbar.set)#设置启用滚动条，可以滚轮滚动列表
    environment_listbox.insert('end','非生产环境')
    environment_listbox.insert('end','生产环境')
    environment_listbox.pack(side='left',fill='both')
    environment_scrollerbar.config(command=environment_listbox.yview)#绑定滚动条给列表框的y轴view（可以鼠标点击拉动滚动条）
    #滚动条
    os_scrollerbar = tk.Scrollbar(os_frame)
    os_scrollerbar.pack(side='right',fill='y')#靠右填充
    os_listbox = tk.Listbox(os_frame,selectmode='single',#单选
                         exportselection='False',#可以让多个选择框选择互不影响
                         height=3,  # 默认只有10行，如果选项大于10项会被遮蔽
                         yscrollcommand=os_scrollerbar.set)#设置启用滚动条，可以滚轮滚动列表
    os_listbox.insert('end','CentOS7.6')
    os_listbox.insert('end','统信系统')
    os_listbox.insert('end','麒麟系统')
    os_listbox.pack(side='left',fill='both')
    os_scrollerbar.config(command=os_listbox.yview)#绑定滚动条给列表框的y轴view（可以鼠标点击拉动滚动条）
    #修改按钮
    change_script_bt = tk.Button(button_frame,text='修改',command=change_script,width=15)
    change_script_bt.pack(side='top',anchor='center')
    #确定按钮
    enter_bt = tk.Button(button_frame,text='确定',command=sub_info,width=15)
    enter_bt.pack(side='bottom',anchor='center')
    
    #文本交互窗口
    script_text = tk.Text(script_frame)
    script_text.pack(anchor='center',fill='both')
    

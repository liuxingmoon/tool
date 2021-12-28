#odps赋权命令
import subprocess as sub
import tkinter as tk
import win32gui,subprocess
from clip_ctrl import clip
import easygui as g

odpsag_dev = r'vm014000005145'
odpsag_prod = r'vm010026006174'
admin_dev = r'ram$ascm-org-1587955260536'
admin_prod = r'ram$ascm-org-1591667515392'


def sub_info():
    environment = environment_listbox.get(environment_listbox.curselection())
    right = right_listbox.get(right_listbox.curselection())
    users = user_text.get('1.0','end').split()
    space = spacebox.get()
    print(environment,right,space,users)
    if environment == r"测试环境":
        odpsag = odpsag_dev
        admin = admin_dev
    elif environment == r"生产环境":
        odpsag = odpsag_prod
        admin = admin_prod
    if right == r'只读权限':
        right = r'role_project_ro'
    elif right == r'开发权限':
        right = r'role_project_dev'
    elif right == r'管理权限':
        right = r'role_project_admin'
    messages = r'use %s;' %(space)
    for user in users:
        messages += r"add user %s:%s;"%(admin,user)
        messages += r"grant %s to %s:%s;"%(right,admin,user)
    g.msgbox(msg=messages,title='odps命令')
    #clip("ssh %s '/apsara/odps_tools/clt/bin/odpscmd --config=/apsara/odps_tools/clt/conf/odps_config.ini.shengshe -e \"%s\"'" %(odpsag,messages))
    clip(messages)
    
def start():
    root = tk.Toplevel()
    root.title('ODPS授权命令辅助')
    global environment_listbox,right_listbox,spacebox,user_text
    #环境
    environmentlist_frame = tk.Frame(root)
    environmentlist_frame.grid(row=0,column=1,padx=10,pady=10)
    right_frame = tk.Frame(root)
    right_frame.grid(row=0,column=2,padx=10,pady=10)
    space_frame = tk.Frame(root)
    space_frame.grid(row=0,column=3,padx=10,pady=10)
    user_frame = tk.Frame(root)
    user_frame.grid(row=1,column=1,columnspan=3,padx=10,pady=10)
    #滚动条
    environment_scrollerbar = tk.Scrollbar(environmentlist_frame)
    environment_scrollerbar.pack(side='right',fill='y')#靠右填充
    environment_listbox = tk.Listbox(environmentlist_frame,selectmode='single',#单选
                         exportselection='False',#可以让多个选择框选择互不影响
                         height=3,  # 默认只有10行，如果选项大于10项会被遮蔽
                         yscrollcommand=environment_scrollerbar.set)#设置启用滚动条，可以滚轮滚动列表
    environment_listbox.insert('end','测试环境')
    environment_listbox.insert('end','生产环境')
    environment_listbox.pack(side='left',fill='both')
    environment_scrollerbar.config(command=environment_listbox.yview)#绑定滚动条给列表框的y轴view（可以鼠标点击拉动滚动条）
    #滚动条
    right_scrollerbar = tk.Scrollbar(right_frame)
    right_scrollerbar.pack(side='right',fill='y')#靠右填充
    right_listbox = tk.Listbox(right_frame,selectmode='single',#单选
                         exportselection='False',#可以让多个选择框选择互不影响
                         height=3,  # 默认只有10行，如果选项大于10项会被遮蔽
                         yscrollcommand=right_scrollerbar.set)#设置启用滚动条，可以滚轮滚动列表
    right_listbox.insert('end','只读权限')
    right_listbox.insert('end','开发权限')
    right_listbox.insert('end','管理权限')
    right_listbox.pack(side='left',fill='both')
    right_scrollerbar.config(command=right_listbox.yview)#绑定滚动条给列表框的y轴view（可以鼠标点击拉动滚动条）
    #项目空间输入框
    spacebox = tk.Entry(space_frame)
    spacebox.pack(side='top',anchor='center')
    spacebox.insert(0,'项目空间名')#插入初始化文本
    #确定按钮
    enter_bt = tk.Button(space_frame,text='确定',command=sub_info)
    enter_bt.pack(side='bottom',anchor='center',fill='both')
    
    
    user_text = tk.Text(user_frame)#宽30字符，高10行
    user_text.pack()
    user_text.insert('end',
                 '写入需要赋权的用户名\n')
    
    '''
    with open('odps_grant.txt','w') as rp:
        rp.write(  + '\n')
        rp.write(report_itsm_info + '\n')
    os.system('odps_grant.txt')
    '''

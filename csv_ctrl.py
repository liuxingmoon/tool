import csv,os

def select_tb(tbname):
    # 判断是否存在文件
    if tbname not in os.listdir():
        print('%s 不存在，请确认！' %(tbname))
    else:
        # 创建文件对象
        f = open(tbname,'r',encoding='gb2312',newline="")
        # 基于文件对象构建 csv写入对象
        csv_reader = csv.reader(f)
        # 保存表结果
        table = []
        for line in f:
            table.append(line)
        # 关闭文件
        f.close()
        print(table)
        return (table)

def create_tb(tbname,values):
    # 排查是否已存在同名文件
    if tbname in os.listdir():
        print('%s 已存在，不需要创建！' %(tbname))
    else:
        # 创建文件对象
        f = open(tbname,'w',encoding='gb2312',newline="")
        # 基于文件对象构建 csv写入对象
        csv_writer = csv.writer(f)
        # 构建列表头
        csv_writer.writerow(values)
        # 关闭文件
        f.close()

def insert_tb(tbname,values):
    # values为列表格式
    # 判断是否存在文件
    if tbname not in os.listdir():
        create_tb(tbname)
    # 新建行存储新用户信息
    # 创建文件对象
    f = open(tbname,'a',encoding='gb2312',newline="")
    # 基于文件对象构建 csv写入对象
    csv_writer = csv.writer(f)
    # 写入csv文件内容
    csv_writer.writerow(values)
    # 关闭文件
    f.close()

def update_tb(tbname,values):
    table = select_tb(tbname)
    # 核对用户部落名
    index = -1  # 记录用户的index
    coc_clan_name = values[2]
    for column in table:
        info = column.split(',')
        if coc_clan_name == info[2]:
            index += 1
            break  # 出现后立刻跳出
        else:
            index += 1
    #替换需要替换的字段：结束服务时间,总服务时间,总消费金额

    info = table[index].split(',')
    srv_time = int(info[5]) + int(values[5])
    money = int(info[6]) + int(values[6])
    table[index] = table[index].replace(info[4],values[4])
    table[index] = table[index].replace(info[5],str(srv_time))
    table[index] = table[index].replace(info[6],str(money))
    #将更新后的table直接覆盖写入到表中
    # 创建文件对象
    with open(tbname,'w',encoding='gb2312',newline="") as f:
    # 基于文件对象构建 csv写入对象
    #csv_writer = csv.writer(f)
        for column in table:
            column = column.replace('\r\n','')
            insert_tb(tbname,column.split(','))
        # 写入csv文件内容
        #.writerow(column.split(','))
    #print(table)

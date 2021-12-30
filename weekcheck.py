#生成周报
import pandas as pd
import configparser
import os
from read_config import configpath

config = configparser.ConfigParser()
config.read(configpath, encoding="utf-8")

dailycheckPath = config.get("work", "dailycheckPath")
weekcheckPath = config.get("work", "weekcheckPath")

#打开日报，复制空行以上的信息
with open(dailycheckPath,mode='r') as dailycheckfile:
    lines = dailycheckfile.readlines()
    lineendindex = lines.index('\n')
    line=[]
    for n in range(0,lineendindex):
        line.append(lines[n])
    print(line)

os.chdir(weekcheckPath)
df = pd.read_excel(r'工作周报-刘兴20200917.xlsx',sheet_name=0)
print(df)
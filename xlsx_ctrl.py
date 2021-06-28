#读写xlsx文件
from openpyxl import load_workbook


def turnStr(L):
    """ 把列表里所有元素转换为字符串型 """
    tmpL = list(map(lambda x: str(x), L))
    return tmpL

#读取xlsx文件
def readXlsx(excelFile):
    wb = load_workbook(excelFile)
    ws = wb.active
    data = []
    column_index = 0#用于定位行数
    for columons in ws.rows:
        data.append([])
        for member in columons:
            data[column_index].append(member.value)
        column_index += 1
    return (data)
    
#写入xlsx文件，以list格式写入到最后一行
def writeXlsx(excelFile,data):
    wb = load_workbook(excelFile)
    ws = wb.active
    ws.append(data)
    wb.save(excelFile)

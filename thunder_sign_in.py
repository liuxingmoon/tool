import thunder.sign_in as s
import time as t
from user import user


def start():
#分隔符
    log = open(r'E:\log\thunder_logging.txt','a')
    log.write('===========================================\n')

    # 执行登录迅雷签到积分
    for u in ('td1','td2'):
        flag = s.thunder(user[u][0],user[u][1])
        endtime = t.strftime("%Y-%m-%d %H:%M:%S", t.localtime())
        log.write('%s %s 签到时间: %s\n' %( u , flag , endtime))

    for u in ('qq1','qq2','qq3','qq4','qq5'):
        flag = s.thunder_qq(user[u][0],user[u][1])
        endtime = t.strftime("%Y-%m-%d %H:%M:%S", t.localtime())
        log.write('%s %s 签到时间: %s\n' %( u , flag , endtime))

    #芯次元签到
    flag = s.xcy(user['xcy'][0],user['xcy'][1])
    endtime = t.strftime("%Y-%m-%d %H:%M:%S", t.localtime())
    log.write('芯次元 %s 签到时间: %s\n' %(flag , endtime))

    log.close()#关闭日志文件

def test():
    # 执行登录迅雷签到积分
    s.xcy(user['xcy'][0],user['xcy'][1])


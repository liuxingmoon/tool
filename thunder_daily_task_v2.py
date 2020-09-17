import time
from user import user
from thunder.phone_sign_in_v2 import Thunder as t
#执行登录迅雷签到积分

def start():
    # 分隔符
    global log
    log = open(r'E:\log\thunder_logging.txt', 'a')
    log.write('===========================================\n')
    # 开始执行操作
    # 获取手机ID
    t().start()
    # 静音
    t().silence()
    # 初始化
    t().format_thunder()

    # 打开迅雷
    t().open_thunder()
    t().login_mail(user['td1'][0], user['td1'][1])
    task()
    prize_mail('td1')

    t().open_thunder()
    t().login_mail(user['td2'][0], user['td2'][1])
    task_qq()
    prize_mail('td2')

    '''
    for u in ('td1','td2'):
        #打开迅雷
        t().open_thunder()
        t().login_mail(user[u][0],user[u][1])
        task()
        prize_mail(u)
    '''

    '''
    t().open_thunder()
    t().login_mail(user['td2'][0],user['td2'][1])
    task()
    prize_mail()
    '''

    for u in (range(1, 6)):
        # 获取手机ID并打开迅雷
        t().open_thunder()
        print(u)
        t().login_qq(u)
        task_qq()
        prize_qq(u)
    '''
    t().open_thunder()
    t().login_qq(5)
    task()
    prize_qq()
    '''

    log.close()  # 关闭日志文件
    t().silence()  # 恢复声音
    t().close()  # 退出

#执行任务
def task():
    #t().task1()
    t().task2()
    t().task3()
    t().task4()
    t().task5()
    #金币页面
    t().gold()
    t().gold1()
    t().gold4()

def task_qq():
    #t().task1()
    t().task2()
    t().task3()
    t().task4()
    t().task5()
    #金币页面
    t().gold()
    #t().gold1()
    t().gold4()

def prize_mail(u):
    #领取金币
    t().gold()
    t().prize_mail_2()
    #退出登录
    t().logout()
    #关闭
    #t().close()
    endtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log.write('%s 签到时间: %s\n' %( u , endtime))

def prize_qq(u):
    #领取金币
    t().gold()
    t().prize_qq_2()
    #退出登录
    t().logout()
    #关闭
    #t().close()
    endtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log.write('qq%s 签到时间: %s\n' %( u , endtime))



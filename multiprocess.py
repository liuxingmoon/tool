import multiprocessing    #导入包
import time
def task1():
    for n in range(5):
        print('task1')
        time.sleep(1)
def task2():
    for n in range(5):
        print('task2')
        time.sleep(1)
if __name__ == '__main__':
    process_1 = multiprocessing.Process(target=task1)    #创建进程对象
    process_2 = multiprocessing.Process(target=task2)    #创建进程对象
    process_1.start()    #启动进程执行任务
    process_2.start()    #启动进程执行任务
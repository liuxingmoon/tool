from pynput.keyboard import Key, Listener
import threading
import inspect
import ctypes


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

def start_listener(thread_listener,func):
    ''' thread_listener:线程名（str） func:函数 '''
    thread_listener = Listener(on_press=func)
    thread_listener.daemon = True
    thread_listener.start()
    return (thread_listener)
        
def start_thread(thread,func,name):
    ''' thread:线程名（str） func:函数  name：线程名称（str） '''
    thread = threading.Thread(target=func, name=name)
    thread.daemon = True
    thread.start()
    return (thread)
    
def stop_thread(thread):
    ''' thread:线程名 '''
    _async_raise(thread.ident , SystemExit)
    return (thread.ident)



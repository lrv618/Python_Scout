#!/usr/bin/env python3
from multiprocessing import Queue
import requests
import threading
import re





# 隧道域名:端口号
#tunnel = "f536.kdltps.com:15818"

# 用户名密码方式
# username = "t19073117948076"
# password = "znaaxgzr"
# proxies = {
#     "http": f"http://{username}:{password}@{tunnel}/",
#     "https": f"http://{username}:{password}@{tunnel}/"
# }



#创建一个子域名扫描器的类
class DomainScan(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue    #实列化队列
    
    def run(self):
        # 获取队列中的url
        while not self.queue.empty():    #在队列不为空的情况下一直执行,检查队列是否为空
            url = self.queue.get()       #从队列中获取一个URL，并将其赋值给变量url
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"
            }
            requests.head = headers
            requests.get(url=url,headers=headers,timeout=1)
            print(f"[*]{url}")   
        except:
            pass
          



def go(dom_name, file_path, count):
    queue = Queue()

    with open(file_path) as file:
        lines = file.read().splitlines()
        for sub in lines:
            queue.put('https://' + sub + '.' + dom_name)   

    # 多线程
    threads = []   #创建了一个空列表，用于存储线程对象。
    thread_count = int(count)
    for i in range(thread_count):      #根据指定的线程数，创建了 thread_count 个 DirScan 对象(每个对象代表一个线程)
        threads.append(DomainScan(queue))  #在循环中，将新创建的 DirScan 对象添加到 threads 列表中

    for t in threads:   #循环遍历 threads 列表中的线程对象。
        t.start()   #启动线程的执行。一旦线程启动，它将开始执行 DirScan 类的 run() 方法中的代码。

    for t in threads:   # 用于等待所有线程执行结束。
        t.join()   # 对每个线程对象调用 join() 方法,阻塞主线程，直到对应线程执行完成。


if __name__ == '__main__':
    dom_name = input("enter the domain name :")
    count = input("请输入线程数（必须是阿拉伯数字）：")
    file_path = "F:/subdomain/subdomain.txt"
    go(dom_name,file_path, count)    






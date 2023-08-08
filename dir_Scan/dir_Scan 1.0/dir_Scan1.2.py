from collections.abc import Callable, Iterable, Mapping
from multiprocessing import Queue
from typing import Any
import requests
import threading
from fake_useragent import UserAgent
import re

rua = UserAgent()

# 隧道域名:端口号
tunnel = "xxxxx:xxxxxxxxx"

# 用户名密码方式
username = "xxxxxxxxxxxxxxxxx"
password = "xxxxxxx"
proxies = {
    "http": f"http://{username}:{password}@{tunnel}/",   
    "https": f"http://{username}:{password}@{tunnel}/"  
}


#创建一个敏感路径扫描器
class DirScan(threading.Thread):  
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue    #实列化队列

    def run(self):
        # 获取队列中的url
        while not self.queue.empty():    #在队列不为空的情况下一直执行,检查队列是否为空
            url = self.queue.get()       #从队列中获取一个URL，并将其赋值给变量url

            try:
                headers = {
                    "User-Agent": rua.random
                }
                response = requests.get(url=url,headers=headers,proxies=proxies,timeout=1)
                if response.status_code == 200:
                    print(f'[*] {url}')
                else:
                    #print("没有此路径\n")
                    pass
            except:
                pass

def go(url, file_path, count):
    queue = Queue()

    with open(file_path) as file:
        lines = file.read().splitlines()
        for line in lines:
            #print(url + line.rstrip('\n'))
            queue.put(url + line)  #将url和文件行里面的路径合并        
    # 多线程
    threads = []   #创建了一个空列表，用于存储线程对象。
    thread_count = int(count)
    for i in range(thread_count):      #根据指定的线程数，创建了 thread_count 个 DirScan 对象(每个对象代表一个线程)
        threads.append(DirScan(queue))  #在循环中，将新创建的 DirScan 对象添加到 threads 列表中

    for t in threads:   #循环遍历 threads 列表中的线程对象。
        t.start()   #启动线程的执行。一旦线程启动，它将开始执行 DirScan 类的 run() 方法中的代码。

    for t in threads:   # 用于等待所有线程执行结束。
        t.join()   # 对每个线程对象调用 join() 方法,阻塞主线程，直到对应线程执行完成。

if __name__ == '__main__':
    while True:
        try:
            url = input("请输入URL地址（格式如 (http)https://www.baidu.com）：")
            if re.match(r'^https?://[^\s/]+$', url):
                break
            elif re.match(r'^http?://[^\s/]+$', url):
                break
            else:
                raise ValueError
        except ValueError:
            print("输入的URL格式不正确，请重新输入。")

    file_path = 'F:\\asp.txt'

    while True:
        try:
            count = input("请输入线程数（必须是阿拉伯数字）：")
            count = int(count)
            if count <= 0:
                raise ValueError
            break
        except ValueError:
            print("线程数必须是大于零的阿拉伯数字！")

    go(url, file_path, count)

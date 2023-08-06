from collections.abc import Callable, Iterable, Mapping
from multiprocessing import Queue
from typing import Any
import requests
import threading
from fake_useragent import UserAgent
import re

rua = UserAgent()

#创建一个敏感路径扫描器
class DirScan(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        # 获取队列中的url
        while not self.queue.empty():
            url = self.queue.get()

            try:
                headers = {
                    "User-Agent": rua.random
                }
                r = requests.get(url=url, headers=headers, timeout=1)
                if r.status_code == 200:
                    print(f'[*] {url}')
                else:
                    # print("没有此路径\n")
                    pass
            except:
                pass

def start(url, file_path, count):
    queue = Queue()

    with open(file_path, 'r') as file:
        lines = file.read().splitlines()
        for line in lines:
            print(url + line.rstrip('\n'))
            queue.put(url + line)
            

    # 多线程
    threads = []
    thread_count = int(count)
    for i in range(thread_count):
        threads.append(DirScan(queue))

    for t in threads:
        t.start()

    for t in threads:
        t.join()

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

    start(url, file_path, count)

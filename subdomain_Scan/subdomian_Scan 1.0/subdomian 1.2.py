#!/usr/bin/env python3

import requests
import concurrent.futures   
from fake_useragent import UserAgent   

rua = UserAgent()    #创建一个随机User-Agent生成器

# 隧道域名:端口号
tunnel = "xxxx.xxxxxx.com:xxxx"

# 用户名密码方式
username = "xxxxxxxxxxxxxxxxx"
password = "xxxxxxx"
proxies = {
    "http": f"http://{username}:{password}@{tunnel}/",   
    "https": f"http://{username}:{password}@{tunnel}/"  
}


# domain_name:主域名  sub_names:子域名列表  sub:子域名 
#定义了一个域名扫描器的类
class DomainScanner:  
    def __init__(self, domain_name, sub_names):  
        self.domain_name = domain_name   
        self.sub_names = sub_names

    def scan_subdomain(self, sub):
        url = f"https://{sub}.{self.domain_name}"
        headers = {
           "User-Agent" : rua.random
        }
        try:
            requests.get(url, proxies=proxies,headers=headers,timeout=2)
            print(f"[*] {url}")   
        except requests.ConnectionError:
            pass

    def start_scan(self):  
        with concurrent.futures.ThreadPoolExecutor() as executor: 
            executor.map(self.scan_subdomain, self.sub_names)   
           
if __name__ == '__main__':
    dom_name = input("请输入域名：")

    with open("F:\\subdomain\\subdomain.txt") as file:
        sub_name = file.read()
        sub_dom = sub_name.splitlines()  

    scanner = DomainScanner(dom_name, sub_dom)
    scanner.start_scan()

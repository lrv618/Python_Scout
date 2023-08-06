#!/usr/bin/env python3

import requests


# 隧道域名:端口号
tunnel = "fxxx.xxxxxxx.com:xxxxx"

# 用户名密码方式
username = "xxxxxxxxxxxxxx"
password = "xxxxx"
proxies = {
    "http": f"http://{username}:{password}@{tunnel}/",
    "https": f"http://{username}:{password}@{tunnel}/"
}


#domain_name:主域名  sub_names:子域名列表  sub:子域名  
#创建一个自定义函数
def domain_scan(domain_name,sub_names):
    for sub in sub_names:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"
        }
        url = f"https://{sub}.{domain_name}"  
        try:
            requests.head = headers
            requests.get(url,proxies=proxies)
            print(f"[*]{url}")   
        except requests.ConnectionError:
          
            pass    


if __name__ == '__main__':
    dom_name = input("enter the domain name :")


    with open("F:/subdomain/subdomain.txt") as file:
        sub_name = file.read().splitlines()  
    domain_scan(dom_name,sub_name)    






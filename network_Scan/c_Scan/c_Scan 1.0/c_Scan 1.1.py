import threading
import ipaddress
import re
from multiprocessing import Queue
from subprocess import Popen, PIPE

#创建一个C类扫描器
class CScan(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while not self.queue.empty():
            ip = self.queue.get()
            try:
                check_ping = Popen(f"ping {ip} -n 1\n", stdin=PIPE, stdout=PIPE, shell=True) 
                data = check_ping.stdout.read()
                if "TTL" in str(data):
                    print(ip + " 在线\n")
                else:
                    pass
            except Exception as e:
                print(f"检查 {ip} 时发生错误: {e}")

def start(count, network, subnet_mask):
    queue = Queue()

    # 根据用户输入的网段和子网掩码计算IP地址范围
    net = ipaddress.IPv4Network(network + '/' + subnet_mask, strict=False)
    for ip in net.hosts():
        queue.put(str(ip))

    # 根据用户输入或系统资源来决定线程数
    thread_count = min(count, queue.qsize())

    # 启动线程
    threads = [CScan(queue) for _ in range(thread_count)]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

if __name__ == '__main__':
    try:
        count = int(input("请输入线程数 (默认为10): ") or 10)
        network = input("请输入网段 (例如，192.168.1.0): ")
        subnet_mask = input("请输入子网掩码 (例如，24): ")

        # 验证输入的网段和子网掩码格式是否正确
        if not re.match(r'^\d+\.\d+\.\d+\.\d+/\d{1,2}$', network + '/' + subnet_mask):
            print("输入的网段或子网掩码格式无效，请重新输入。")
        else:
            print("正在扫描，请稍等...")
            start(count, network, subnet_mask)
    except ValueError:
        print("线程数必须是一个整数。")

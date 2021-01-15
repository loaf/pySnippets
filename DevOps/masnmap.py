#!/usr/bin/python
# coding=utf-8

# https://github.com/starnightcyber/masnmap
'''
masnmap
masscan + nmap 快速端口存活检测和服务识别。

思路很简单，将masscan在端口探测的高速和nmap服务探测的准确性结合起来，达到一种相对比较理想的效果。 先使用masscan以较高速率对ip存活端口进行探测，再以多进程的方式，使用nmap对开放的端口进行服务探测。

安装依赖
需先安装masscan 、nmap和python-nmap库。 masscan和nmap请自行安装，python-nmap库可通过如下命令安装。

pip3 install python-nmap -i https://pypi.douban.com/simple/
目前其版本为：python-nmap==0.6.1

文件说明
简要文件说明如下：

masnmap.py: masscan + nmap结合快速端口存活和服务探测脚本；
ips.txt: 需探测的ip地址列表，每行一个ip地址；
services.txt: 保存探测的结果，以"序号：ip：端口：服务名" msg = '{}:{}:{}:{}'.format(index, ip, port, service)
参数配置说明
简要参数说明如下：

ip_file = 'ips.txt' # ip地址文件
masscan_exe = '/usr/bin/masscan' # masscan可执行文件路径
masscan_rate = 1000000 # masscan扫描速率
masscan_file = 'masscan.json' # masscan扫描结果文件
process_num = 800 # 执行nmap扫描的进程数量
具体参数值可以自行调优。
'''

import nmap
import datetime
import json
from queue import Queue
from multiprocessing import Pool
import os


ip_file = 'ips.txt'
# masscan_exe = '/usr/local/bin/masscan'
masscan_exe = '/usr/bin/masscan'
masscan_rate = 2000
masscan_file = 'masscan.json'
task_queue = Queue()
result_queue = Queue()
process_num = 50
total_ports = 0
services_info = []


def run_masscan():
    command = 'sudo {} -iL {} -p 1-65535 -oJ {} --rate {}'.format(masscan_exe, ip_file, masscan_file, masscan_rate)
    msg = 'executing ==> {}'.format(command)
    print(msg)
    os.system(command)
    pass


def extract_masscan():
    """
    extract masscan result file masscan.json into ip:port format, and add to queue
    """
    with open(masscan_file, 'r') as fr:
        tmp_lines = fr.readlines()
        lines = tmp_lines[1:-1]
        global total_ports
        total_ports = len(lines)
        for line in lines:
            tmp = line.strip(',\n')
            line_json = json.loads(tmp)
            # print(line_json)
            # extract ip & port
            ip = line_json['ip']
            port = line_json['ports'][0]['port']

            # combine ip:port, and add to queue
            ip_port = '{}:{}'.format(ip, port)
            task_queue.put(ip_port)
            print(ip_port)
            # exit()
    pass


def nmap_scan(ip_port, index):
    # print('scan ==> {}'.format(ip_port))
    try:
        ip, port = ip_port.split(':')
        nm = nmap.PortScanner()
        ret = nm.scan(ip, port, arguments='-Pn,-sS')
        service = ret['scan'][ip]['tcp'][int(port)]['name']
        msg = '{}:{}:{}:{}'.format(index, ip, port, service)
        print(msg)
        return msg
    except:
        print('sth bad happen ...')


def setcallback(msg):
    services_info.append(msg)


def run_nmap():
    pool = Pool(process_num)  # 创建进程池
    index = 0
    while not task_queue.empty():
        index += 1
        ip_port = task_queue.get(timeout=1.0)
        pool.apply_async(nmap_scan, args=(ip_port, index), callback=setcallback)
    pool.close()
    pool.join()


def save_results():
    print('save_results ...')
    print("services {} lines".format(len(services_info)))
    with open("services.txt", 'w') as fw:
        for line in services_info:
            fw.write(line+'\n')


def main():
    # Step 1, run masscan to detect all the open port on all ips
    run_masscan()

    # Step 2, extract masscan result file:masscan.json to ip:port format
    extract_masscan()

    # Step 3, using nmap to scan ip:port
    run_nmap()

    # Step 4, save results
    save_results()


if __name__ == '__main__':
    start = datetime.datetime.now()
    main()
    end = datetime.datetime.now()
    spend_time = (end - start).seconds
    msg = 'It takes {} process {} seconds to run ... {} tasks'.format(process_num, spend_time, total_ports)
    print(msg)

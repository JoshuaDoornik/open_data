import socket
import multiprocessing
import subprocess
import os
import sys
import time
import requests
import json
import hashlib


def pinger(job_q, results_q):
    """
    Do Ping
    :param job_q:
    :param results_q:
    :return:
    """
    DEVNULL = open(os.devnull, 'w')
    while True:

        ip = job_q.get()

        if ip is None:
            break

        try:
            subprocess.check_call(['ping', '-c1', ip],
                                  stdout=DEVNULL)
            results_q.put(ip)
        except:
            pass


def get_my_ip():
    """
    Find my IP address
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    print (s.getsockname())
    s.close()
    return ip


def map_network(pool_size=255):
    """
    Maps the network
    :param pool_size: amount of parallel ping processes
    :return: list of valid ip addresses
    """

    ip_list = list()

    # get my IP and compose a base like 192.168.1.xxx
    ip_parts = get_my_ip().split('.')
    base_ip = ip_parts[0] + '.' + ip_parts[1] + '.' + ip_parts[2] + '.'

    # prepare the jobs queue
    jobs = multiprocessing.Queue()
    results = multiprocessing.Queue()

    pool = [multiprocessing.Process(target=pinger, args=(jobs, results)) for i in range(pool_size)]

    for p in pool:
        p.start()

    # cue hte ping processes
    for i in range(1, 255):
        jobs.put(base_ip + '{0}'.format(i))

    for p in pool:
        jobs.put(None)

    for p in pool:
        p.join()

    # collect the results
    while not results.empty():
        ip = results.get()
        ip_list.append(ip)

    return ip_list

def send(lst):
    with open('locationdata.json') as f:
        location = json.load(f)
    location['amount'] = len(lst)
    location['ips'] = lst
    location['timestamp'] = time.time()
    try:
        r = requests.post("http://127.0.0.1:5000/store",json=location)
        print(r.status_code)
    except requests.exceptions.ConnectionError:
        print("couldnt connect to main server")

if __name__ == '__main__':
    devices = subprocess.Popen(['arp -an'],shell=True,stdout=subprocess.PIPE,universal_newlines=True).communicate()[0]
    lst = str(devices).split('\n')
    print(len(lst))
    hash_func = lambda x: hashlib.md5(x.encode('utf-8')).hexdigest()
    lst = list(map(hash_func, lst))
    send(lst)





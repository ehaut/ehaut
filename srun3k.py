#!/usr/bin/env python3
#!Design by zeng-xz
#!Optimized by Noisky
# -*- coding: UTF-8 -*-
import logging
import string,os,sys
import socket
import struct
import threading
import time 
import configparser
from urllib.parse import urlencode
from urllib.request import urlopen

STATUS = 'http://172.16.154.130/cgi-bin/rad_user_info'
PORTAL = 'http://172.16.154.130:69/cgi-bin/srun_portal'
#UDP_PORT1 = ('172.16.154.130', 3338)
#UDP_PORT2 = ('172.16.154.130', 4338)

cf = configparser.ConfigParser()

print("---------------------------------------------\n")
print("         欢迎使用校园网登陆器 py 版         \n")
print("         Made By 曾大佬 & 饭饭  V1.1        \n")
print("  程序会自动检测是否在线，并且掉线自动重连  \n")
print("  如需下线请关闭本窗口，然后使用网页版注销  \n")
print("---------------------------------------------\n")

if os.path.isfile('config.ini'):
    cf.read("config.ini")
else:
    cf.add_section("srun")
    cf.set("srun","username",input("请输入账号:"))
    cf.set("srun","password",input("请输入密码:"))
    cf.write(open("config.ini", "w"))

USERNAME = cf.get("srun","username")
PASSWORD = cf.get("srun","password")

print("您已在线，登录账号为:",USERNAME)

logging.basicConfig(level=logging.INFO, format='[%(asctime)-15s] %(message)s')


def request(url, data=None) -> str:
    with urlopen(url, data) as f:
        return f.read().decode()


def username_encrypt(username):
    result = '{SRUN3}\r\n'
    return result + ''.join([chr(ord(x) + 4) for x in username])


def password_encrypt(password, key='1234567890'):
    result = list()
    for i in range(len(password)):
        ki = ord(password[i]) ^ ord(key[len(key) - i % len(key) - 1])
        _l = chr((ki & 0x0F) + 0x36)
        _h = chr((ki >> 4 & 0x0F) + 0x63)

        if i % 2 == 0: result.extend((_l, _h))
        else: result.extend((_h, _l))
    return ''.join(result)


def udp_keep_alive(username: bytes, mac=b'02:00:00:00:00:00') -> None:
    pack = struct.pack('! 12s 20x 17s 7x', username, mac)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        s.sendto(pack, UDP_PORT1)
        s.sendto(pack, UDP_PORT2)
        logging.debug('udp keep alive')
        time.sleep(30)


def http_keep_login(username: str, password: str) -> None:
    e_username = username_encrypt(username)
    e_password = password_encrypt(password)
    post_data = urlencode({
        'action': 'login',
        'username': e_username,
        'password': e_password,
        'ac_id': 1,
        'drop': 0,
        'pop': 1,
        'type': 10,
        'n': 117,
        'mbytes': 0,
        'minutes': 0,
    }).encode()
    while True:
        if request(STATUS).startswith('not_online'):
            logging.info('Not Online')
            login = request(PORTAL, post_data)
            if login.startswith('login_ok') or login.startswith(
                    'login_error#E2620'):  # You are already online.
                logging.info('Login OK')
            else:
                continue
        time.sleep(1)


if __name__ == '__main__':
    u = USERNAME
    p = PASSWORD
    mac = b'22:76:93:33:b2:a9'
    t1 = threading.Thread(target=http_keep_login, args=(u, p))
    #t2 = threading.Thread(target=udp_keep_alive, args=(u.encode(), mac))
    t1.start()
    #t2.start()
    #t2.join()
    print('End')

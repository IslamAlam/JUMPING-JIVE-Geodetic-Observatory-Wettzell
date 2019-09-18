#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JumpingJIVE Student Task 5
Dynamic Zabbix Map
login.py for Zabbix system login

latest update on 24.03.2019

@author: Jingyao Su
"""
import requests

# default information, no need to change, only need to update in dynamicmap.dy
USER = "Admin"
PASSWORD = "zabbix"
URL = 'http://192.168.1.105/zabbix/api_jsonrpc.php'


def syslogin(user,passwd,url):
    URL = url
    
    LOGIN={
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": user,
            "password": passwd
            },
        "id": 1,
        "auth": None
        }
    
    r = requests.post(url = URL, json = LOGIN, verify = False)
    data = r.json()
    auth = data.get('result')
    return auth
	
def main(user = USER, passwd = PASSWORD, url = URL):
    try:
        authcode = syslogin(user,passwd,url)
    except BaseException:
        print ("Login error or could not connect to server at "+ URL)
        exit(1)
    return authcode
    
    
if __name__ == '__main__':    
    main()
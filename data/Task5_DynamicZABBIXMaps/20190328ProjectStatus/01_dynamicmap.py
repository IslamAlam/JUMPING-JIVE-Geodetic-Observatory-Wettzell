#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JumpingJIVE Student Task 5
Dynamic Zabbix Map
dynamicmap.py

latest update on 25.03.2019

@author: Jingyao Su

Fuction realized:
    1. get host information
    2. create images as background of maps
    3. create Wettzell station map and EVN global map
    4. determine station/antennas location on the map
    5. add or delete stations/antennas on the map
    6. update and delete maps
    7. possibility to switch on/off the antennas on the map

How to use:
    1. firstly input login information: user name and password, "Admin" and 
    "zabbix" as default, as well as the Zabbix server URL and image or map IDs.
    2. Then select which request to be deployed
    3. Above parameters could also be input by updating the definition part of 
    main function in this script or defining in command line, e.g. on linux: "
    python dynamicmap.py request_number user password". see user and developer 
    documantation.
    4. Description of requests:
        - Request 1 get the information of Zabbix server or the host that needs 
        to be monitored, default is current server "Zabbix server"
        - Request 2 defines the image background for Wettzell Station, default 
        is 400*300, in the form of BASE64
        - Request 3 defines the image background for EVN global map, default is 
        2000*1000. capable of illustrating monitoring status.
        - Request 4 defines the map pf Wettzell station, default consists of 
        two hosts (Twin telescopes 1 and 2). Screens and graphs are supposed to 
        be linked
        - Request 5 modifies the map of Wettzell station
        - Request 6 delete the map of Wettzell station
        - Request 7 defines the EVN global map, default includes only Wettzell 
        as a submap button
        - Request 8 modifies the EVN global map
        - Request 9 delete the map of EVN global map
        
for more details see developer and user documentation.

"""

import requests,sys,login,images

# =============================================================================
# Definitions and login account
# =============================================================================
# Zabbix server address, only update here
url = 'http://192.168.1.105/zabbix/api_jsonrpc.php' # test Zabbix server on laptop

# Login information, update here if no extra input from command lines
user = "Admin"
password = "zabbix"    

# system IDs of images or maps in Zabbix, update here if no extra input from command lines
wettzellimageid = 214
wettzellmapid = 33
evnimageid = 215
evnmapid = 34
hostid = 10084
hostid1 = 0
hostid2 = 0
hostname = "Zabbix server"

# images in BASE64 format
image4000_2000 = images.image4000_2000
image2000_1000 = images.image2000_1000
image1000_500 = images.image1000_500
imagewettzell = images.imagewettzell

# =============================================================================
# Request 1: login and get host info
# =============================================================================
def request1(host=hostname):
    # definitions
    global hostid
    
    # get sessionid
    token = login.main()
    
    # request content
    post_data = {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
			"filter": {
				"host": [
					host
				]
			},
            "output": [
                "hostid",
                "host"
            ],
            "selectInterfaces": [
                "interfaceid",
                "ip"
            ]
        },
        "id": 2,
        "auth": token
    }    
    r = requests.post(url, json = post_data, verify = False)
    zabbix_ret = r.json()
    
    if not zabbix_ret.__contains__('result'):
        print ('Request 2 image creates error:',zabbix_ret.get('error')['data'])
    else:
        hostid = zabbix_ret['result'][0]['hostid']
        print ('login succeeds. Your host is', zabbix_ret['result'][0]['host'],'with ID of ',hostid,'. IP address of interfaces is',zabbix_ret['result'][0]['interfaces'][0]['ip'])
                                    # get the current server host information. warnings if login is error.

                    
# =============================================================================
# Request 2: create images as background for Wettzell Station
# =============================================================================
def request2():
    # definitions
    global wettzellimageid
    
    # get sessionid
    token = login.main(user,password,url)
    
    # request content
    post_data = {
        "jsonrpc": "2.0",
        "method": "image.create",
        "params": {
            "imagetype": 2,             # type of background image
            "name": "Wettzell station image",
            "image": imagewettzell
        },
        "auth": token,
        "id": 3
    }
    r = requests.post(url, json = post_data, verify = False)
    zabbix_ret = r.json()

    if not zabbix_ret.__contains__('result'):
        print ('Request 2 image creates error:',zabbix_ret.get('error')['data'])
    else:
        wettzellimageid = zabbix_ret.get('result')['imageids'][0]
        print("Wettzell image created successfully")
        print("Request 2 result: ", zabbix_ret)  

# =============================================================================
# Request 3: create images as background for global network
# =============================================================================
def request3():
    # definitions
    global evnimageid
    
    # get sessionid
    token = login.main(user,password,url)
    
    # request content
    post_data = {
        "jsonrpc": "2.0",
        "method": "image.create",
        "params": {
            "imagetype": 2,             # type of background image
            "name": "EVN global map",
            "image": image2000_1000
        },
        "auth": token,
        "id": 4
    }        
    r = requests.post(url, json = post_data, verify = False)
    zabbix_ret = r.json()

    if not zabbix_ret.__contains__('result'):
        print ("Request 3 image creates error:",zabbix_ret.get('error')['data'])
    else:
        evnimageid = zabbix_ret.get('result')['imageids'][0]
        print("Global map image created successfully")
        print("Request 3 result: ", zabbix_ret) 

# =============================================================================
# Request 4: create map of Wettzell Station
# =============================================================================
def request4(imageid=wettzellimageid,hostid1=hostid,hostid2=hostid):
    # definitions
    global wettzellmapid
    # hostid1 and hostid2 are host IDs of telescopes, to be defined
    
    # get sessionid
    token = login.main(user,password,url)
    
    # request content
    post_data = {
        "jsonrpc": "2.0",
        "method": "map.create",
        "params": {
            "name": "Wettzell Station",
            "width": 400,
            "height": 300,
            "backgroundid": imageid,        # image ID obtained from creation or input
            "expandproblem": 0,             # the problem trigger will be displayed for elements with a single problem. always display the number of problems; 
            "label_type_map": 2,            # Map element label type: default delement name
            "grid_align": 0,                # disable grid aligning to fix station coordinate
            "highlight": 1,                 # icon highlighting is enabled
            "label_location": 0,            # Location of the map element label: bottom as default
            "label_type_host": 0,           # Custom label for host elements. 
            "shapes": [
                {                           # defines the title of map
                    "type": 0,
                    "x": 150,
                    "y": 30,
                    "width": 100,
                    "height": 10,
                    "text": "{MAP.NAME}",
                    "font": 4,
                    "font_size": 11                
                }
            ],
            "selements": [
                {
                    "selementid": "1",      
                    "elements": [
                        {"hostid": hostid1}
                    ],
                    "elementtype": 0,                   # Type of map element: host
                    "application": "Twin Telescope 1",  # application of the host
                    "iconid_off": "143",                # ID of the image used to display the element in default state. 
                    "iconid_disabled": "144",           # ID of the image used to display disabled map elements. Unused for image elements. 
                    "iconid_maintenance": "144",        # ID of the image used to display map elements in maintenance. Unused for image elements. 
                    "iconid_on": "144",                 # ID of the image used to display map elements with problems. Unused for image elements. 
                    "label": "Twin Telescope 1",
                    "label_location": 0,
                    "x": 220,                           # coordinate of telescope
                    "y": 190
                },
                {
                    "selementid": "2",
                    "elements": [
                        {"hostid": hostid2}
                    ],
                    "elementtype": 0,
                    "application": "Twin Telescope 2",
                    "iconid_off": "143",
                    "iconid_disabled": "144",
                    "iconid_maintenance": "144",
                    "iconid_on": "144",
                    "label": "Twin Telescope 2",
                    "label_location": 0,
                    "x": 268,
                    "y": 255
                },         
            ]
        },
        "auth": token,
        "id": 5
    }    
    r = requests.post(url, json = post_data, verify = False)
    zabbix_ret = r.json()

    if not zabbix_ret.__contains__('result'):
        print ("Request 4 map creates error:",zabbix_ret.get('error')['data'])
    else:
        wettzellmapid = zabbix_ret.get('result')['sysmapids'][0]
        print("Wettzell map created successfully")
        print("Request 4 result: ", zabbix_ret) 

# =============================================================================
# Request 5: update map of Wettzell Station
# =============================================================================
def request5(mapid=wettzellmapid,imageid=wettzellimageid,hostid1=hostid,hostid2=hostid):  
    # get sessionid
    token = login.main(user,password,url)
    
    # request content
    post_data = {
        "jsonrpc": "2.0",
        "method": "map.update",
        "params": {
            "sysmapid": mapid,              # map ID obtained from creation or input
            "name": "Wettzell Station",
            "width": 400,
            "height": 300,
            "backgroundid": imageid,        # background image ID
            "expandproblem": 0,             # the problem trigger will be displayed for elements with a single problem. always display the number of problems; 
            "label_type_map": 2,            # Map element label type: default element name
            "grid_align": 0,                # disable grid aligning to fix station coordinate
            "highlight": 1,                 # icon highlighting is enabled
            "label_location": 0,            # Location of the map element label: bottom as default
            "label_type_host": 0,           # Custom label for host elements. 
            "shapes": [
                {                           # defines the title of map
                    "type": 0,
                    "x": 150,
                    "y": 30,
                    "width": 100,
                    "height": 10,
                    "text": "{MAP.NAME}",
                    "font": 4,
                    "font_size": 11                
                }
            ],
            "selements": [
                {
                    "selementid": "1",      
                    "elements": [
                        {"hostid": hostid1}
                    ],
                    "elementtype": 0,                   # Type of map element: host
                    "application": "Twin Telescope 1",  # application of the host
                    "iconid_off": "143",                # ID of the image used to display the element in default state. 
                    "iconid_disabled": "144",           # ID of the image used to display disabled map elements. Unused for image elements. 
                    "iconid_maintenance": "144",        # ID of the image used to display map elements in maintenance. Unused for image elements. 
                    "iconid_on": "144",                 # ID of the image used to display map elements with problems. Unused for image elements. 
                    "label": "Twin Telescope 1",
                    "label_location": 0,
                    "x": 220,                           # coordinate of telescope
                    "y": 190
                },
                {
                    "selementid": "2",
                    "elements": [
                        {"hostid": hostid2}
                    ],
                    "elementtype": 0,
                    "application": "Twin Telescope 2",
                    "iconid_off": "143",
                    "iconid_disabled": "144",
                    "iconid_maintenance": "144",
                    "iconid_on": "144",
                    "label": "Twin Telescope 2",
                    "label_location": 0,
                    "x": 268,
                    "y": 255
                },         
            ]
        },
        "auth": token,
        "id": 6
    }   
    r = requests.post(url, json = post_data, verify = False)
    zabbix_ret = r.json()

    if not zabbix_ret.__contains__('result'):
        print ("Request 5 map updates error:",zabbix_ret.get('error')['data'])
    else:
        print("Wettzell map updated successfully")
        print("Request 5 result: ", zabbix_ret) 

# =============================================================================
# Request 6: delete map of Wettzell station
# =============================================================================
def request6(mapid=wettzellmapid):
    # get sessionid
    token = login.main(user,password,url)
    
    # request content
    post_data = {
        "jsonrpc": "2.0",
        "method": "map.delete",
        "params": [
            mapid # here is the id of map to be deleted
        ],
        "auth": token,
        "id": 7
    }    
    r = requests.post(url, json = post_data, verify = False)
    zabbix_ret = r.json()

    if not zabbix_ret.__contains__('result'):
        print ("Request 6 map deletes error:",zabbix_ret.get('error')['data'])
    else:
        print("Wettzell map deleted successfully")
        print("Request 6 result: ", zabbix_ret) 

# =============================================================================
# Request 7: create map of EVN global network 
# =============================================================================
def request7(imageid=evnimageid,submapid=wettzellmapid):
    # definitions
    global evnmapid
    
    # get sessionid
    token = login.main(user,password,url)
    
    # request content
    post_data = {
        "jsonrpc": "2.0",
        "method": "map.create",
        "params": {
            "name": "EVN Global Network",
            "width": 2000,
            "height": 1000,
            "backgroundid": imageid,
            "label_type_map": 2,    # Map element label type: default delement name
            "expandproblem": 0,     # the problem trigger will be displayed for elements with a single problem. always display the number of problems; 
            "grid_align": 0,        # disable grid aligning to fix station coordinate
            "highlight": 1,         # icon highlighting is enabled
            "label_location": 0,
            "shapes": [
                {                   # defines the title of map
                    "type": 0,
                    "x": 800,
                    "y": 30,
                    "width": 400,
                    "height": 20,
                    "text": "{MAP.NAME}",
                    "font": 4,
                    "font_size": 20  
                }
            ],
            "selements": [
                {
                    "selementid": "1",
                    "elements": [
                        {"sysmapid": submapid}
                    ],
                    "elementtype": 1,           # defines the map element: submap
                    "iconid_off": "144",        # ID of the image used to display the element in default state. 
                    "iconid_disabled": "145",   # ID of the image used to display disabled map elements. Unused for image elements.
                    "iconid_maintenance": "145",# ID of the image used to display map elements in maintenance. Unused for image elements. 
                    "iconid_on": "145",         # ID of the image used to display map elements with problems. Unused for image elements. 
                    "label": "Wettzell",
                    "label_location": 0,
                    "x": 1008,                  # coordinate of telescopes
                    "y": 151
                }
            ]
        },
        "auth": token,
        "id": 8
    }    
    r = requests.post(url, json = post_data, verify = False)
    zabbix_ret = r.json()

    if not zabbix_ret.__contains__('result'):
        evnmapid = zabbix_ret["result"]["sysmapids"][0]
        print ("Request 7 map creates error:",zabbix_ret.get('error')['data'])
    else:
        print("EVN global map created successfully")
        print("Request 7 result: ", zabbix_ret) 

# =============================================================================
# Request 8: update map of EVN global network
# =============================================================================
def request8(mapid=evnmapid,imageid=evnimageid,submapid=wettzellmapid):    
    # get sessionid
    token = login.main(user,password,url)
    
    # request content
    post_data = {
        "jsonrpc": "2.0",
        "method": "map.update",
        "params": {                
            "sysmapid": mapid,      # ID of map to be updated
            "name": "EVN Global Network",
            "width": 2000,
            "height": 1000,
            "backgroundid": imageid,
            "label_type_map": 2,    # Map element label type: default delement name
            "expandproblem": 0,     # the problem trigger will be displayed for elements with a single problem. always display the number of problems; 
            "grid_align": 0,        # disable grid aligning to fix station coordinate
            "highlight": 1,         # icon highlighting is enabled
            "label_location": 0,
            "shapes": [
                {                   # defines the title of map
                    "type": 0,
                    "x": 800,
                    "y": 30,
                    "width": 400,
                    "height": 20,
                    "text": "{MAP.NAME}",
                    "font": 4,
                    "font_size": 20  
                }
            ],
            "selements": [
                {
                    "selementid": "1",
                    "elements": [
                        {"sysmapid": submapid}
                    ],
                    "elementtype": 1,           # defines the map element: aubmap
                    "iconid_off": "144",        # ID of the image used to display the element in default state. 
                    "iconid_disabled": "145",   # ID of the image used to display disabled map elements. Unused for image elements.
                    "iconid_maintenance": "145",# ID of the image used to display map elements in maintenance. Unused for image elements. 
                    "iconid_on": "145",         # ID of the image used to display map elements with problems. Unused for image elements. 
                    "label": "Wettzell",
                    "label_location": 0,
                    "x": 1008,                  # coordinate of telescopes
                    "y": 151
                }
            ]
        },
        "auth": token,
        "id": 9
    }    
    r = requests.post(url, json = post_data, verify = False)
    zabbix_ret = r.json()

    if not zabbix_ret.__contains__('result'):
        print ("Request 8 map updates error:",zabbix_ret.get('error')['data'])
    else:
        print("EVN global map updated successfully")
        print("Request 8 result: ", zabbix_ret) 

# =============================================================================
# Request 9: delete map of EVN global networks
# =============================================================================
def request9(mapid=evnmapid): 
    # get sessionid
    token = login.main(user,password,url)
    
    # request content
    post_data = {
        "jsonrpc": "2.0",
        "method": "map.delete",
        "params": [
            mapid # here is the id of maps to delete, refined later
        ],
        "auth": token,
        "id": 10
    }
    
    r = requests.post(url, json = post_data, verify = False)
    zabbix_ret = r.json()

    if not zabbix_ret.__contains__('result'):
        print ("Request 9 map deletes error:",zabbix_ret.get('error')['data'])
    else:
        print("EVN global map deleted successfully")
        print("Request 9 result: ", zabbix_ret) 

# =============================================================================
# Main function
# =============================================================================   
def main():
    global user,password,request_number,hostid1,hostid2,wettzellimageid
    global evnimageid,wettzellmapid,evnmapid,hostname
    # login through command line
    if len(sys.argv) >= 4: 
        user = sys.argv[2]
        password = sys.argv[3]
            
    # Selection of request to be deployed
    if len(sys.argv) == 1:
        request_number = 1 # defaut request to be deployed,
                           # update here if no extra input from command lines
    else:
        if sys.argv[1].isdigit():
            request_number = int(sys.argv[1])
        else:
            request_number = 0
        
    # deploy the request
    if request_number < 1 or request_number > 9:
        print("request not exists . please check again.")
    else:
        if request_number == 1:
            if len(sys.argv) == 5:
                hostname = int(sys.argv[4])
                request1(hostname)
            else:
                request1()
        if request_number == 2:
            request2()
        if request_number == 3:
            request3()
        if request_number == 4:
            if len(sys.argv) == 7:
                wettzellimageid = int(sys.argv[4])
                hostid1 = int(sys.argv[5]) 
                hostid2 = int(sys.argv[6])
                request4(wettzellimageid,hostid1,hostid2)
            else:
                request4()
        if request_number == 5:            
            if len(sys.argv) == 8:                
                wettzellmapid = int(sys.argv[4])
                wettzellimageid = int(sys.argv[5]) 
                hostid1 = int(sys.argv[6])
                hostid2 = int(sys.argv[7])
                request5(wettzellmapid,wettzellimageid,hostid1,hostid2)
            else:
                request5()
        if request_number == 6:            
            if len(sys.argv) == 5:
                wettzellmapid = int(sys.argv[4])
                request6(wettzellmapid)
            else:
                request6()
        if request_number == 7:            
            if len(sys.argv) == 6:
                evnimageid = int(sys.argv[4])
                wettzellmapid = int(sys.argv[5]) 
                request7(evnimageid,wettzellmapid)
            else:
                request7()
        if request_number == 8:            
            if len(sys.argv) == 7:
                evnmapid = int(sys.argv[4])
                evnimageid = int(sys.argv[5]) 
                wettzellmapid = int(sys.argv[6])
                request8(evnmapid,evnimageid,wettzellmapid)
            else:
                request8()
        if request_number == 9:            
            if len(sys.argv) == 5:
                evnmapid = int(sys.argv[4])
                request9(evnmapid)
            else:
                request9()

# =============================================================================
# Exception handling
# =============================================================================  
if __name__ == '__main__':    
    try:
        main()
    except BaseException:
        print ("request error. see error message.")
        exit(1)
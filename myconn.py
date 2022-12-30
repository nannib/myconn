# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 17:23:05 2022

@author: Nanni Bassetti - https://nannibassetti.com
"""

import psutil
import requests
from datetime import datetime

now = datetime.now()
pids = []
print ("My connections by Nanni Bassetti - https://nannibassetti.com")

filename="report_"+str(now).replace(" ","-").replace(".","_").replace(":","_")

header = "ProcessName :: "+"PID     ::     "+"RemoteIP    ::    "+"Status :: "

header_html="<html><title>"+filename+"</title><body><br><b>My connections by Nanni Bassetti <a href=https://nannibassetti.com target=_blank>https://nannibassetti.com</a></b></br><br><table border=1><tr><td>ProcessName</td><td>PID</td><td>RemoteIP</td><td>Status</td></tr>"

print(header)
db = open("./"+filename+".html", "w")
print(header_html,file=db)

for proc in psutil.process_iter():
    try:
        processName = proc.name()
        processID = proc.pid
        pids.append(proc.pid)
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass
connections = psutil.net_connections()

for con in connections: 
  if con.pid in pids:
        if con.raddr: 
            for pn in psutil.process_iter():
                if con.pid == pn.pid:
                    processName=pn.name()
            #if con.raddr.ip != '127.0.0.1' and ':' not in con.raddr.ip:
            if con.raddr.ip != '127.0.0.1':
                ip_address = con.raddr.ip
                response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
                location_data = {
                    "ip": ip_address,
                    "city": response.get("city"),
                    "region": response.get("region"),
                    "country": response.get("country_name"),
                    "org": response.get("org")
                    }
                    
                
                print('---------------------------')
                print (processName," :: ",con.pid," :: ", con.raddr.ip, " :: ", con.status," :: ",location_data)
                processName_url="<a href=https://google.com/search?q="+processName+" target=_blank>"
                if processName=="System Idle Process":
                    processName_url="<a href=https://google.com/search?q='"+processName+"' target=_blank>"
                    
                riga="<tr><td>"+processName_url+processName+"</a></td><td>"+str(con.pid)+"</td><td>"+con.raddr.ip+"</td><td>"+con.status+"</td><td>"+str(location_data)+"</td></tr>"
                print(str(riga).replace("(","").replace("'","").replace(")",""),file=db)
                   
db.close()
input ("press ENTER to close the application") 
     
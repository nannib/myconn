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
pname = []
location_data=""
print ("My connections by Nanni Bassetti - https://nannibassetti.com")
geoip=input("Do you want IP geolocation (slower)? (y/n)")
while True:
    if geoip.lower() == "y" or geoip.lower() == "n":
        break
    else:
        geoip=input("Do you want IP geolocation (slower)? (y/n)")
        continue
filename="report_"+str(now).replace(" ","-").replace(".","_").replace(":","_")

header = "ProcessName :: "+"PID     ::   "+"LocalPort   ::   "+"RemoteIP    ::    "+"Status :: "

header_html="<html><title>"+filename+"</title><body><br><b>My connections by Nanni Bassetti <a href=https://nannibassetti.com target=_blank>https://nannibassetti.com</a></b></br><br><table border=1><tr><td>ProcessName</td><td>PID</td><td>LocalPort</td><td>RemoteIP</td><td>Status</td></tr>"

print(header)
db = open("./"+filename+".html", "w")
print(header_html,file=db)

for proc in psutil.process_iter():
    try:
        pids.append(proc.pid)
        pname.append(proc.name())
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass
connections = psutil.net_connections()

for con in connections: 
  if con.pid in pids:
      if con.raddr:
            processName=pname[pids.index(con.pid)]
            #if con.raddr.ip != '127.0.0.1' and ':' not in con.raddr.ip:
            if con.raddr.ip != '127.0.0.1':
                ip_address = con.raddr.ip
                if geoip.lower() == "y":
                    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
                    location_data = {
                    "ip": ip_address,
                    "city": response.get("city"),
                    "region": response.get("region"),
                    "country": response.get("country_name"),
                    "org": response.get("org")
                    }
                    
                
                print('---------------------------')
                print (processName," :: ",con.pid," :: ",con.laddr.port," :: ", con.raddr.ip,":",con.raddr.port," :: ", con.status," :: ",location_data)
                processName_url="<a href=https://google.com/search?q="+processName+" target=_blank>"
                if processName=="System Idle Process":
                    processName_url="<a href=https://google.com/search?q="+processName.replace(" ","")+" target=_blank>"
                    
                riga="<tr><td>"+processName_url+processName+"</a></td><td>"+str(con.pid)+"</td><td>"+str(con.laddr.port)+"</td><td>"+con.raddr.ip+":"+str(con.raddr.port)+"</td><td>"+con.status+"</td><td>"+str(location_data)+"</td></tr>"
                print(str(riga).replace("(","").replace("'","").replace(")",""),file=db)
                   
db.close()
input ("press ENTER to close the application") 
     
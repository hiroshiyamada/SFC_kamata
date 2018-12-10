#!/usr/bin/python3
# -*- coding: utf-8 -*-
import cgi
import time
import requests

ev3_ip = "192.168.100.113"

print("Content-Type: text/html\n\n")

#for i in range(int(form.getvalue("key0"))):
#    key = "key" + str(i+1)
#    value = tuple(form.getvalue(key))
#    music.append(value)

form = cgi.FieldStorage()
s = requests.session()
r = s.post("http://" + ev3_ip + "/python/receive.py", data = form)
print(r.text)
#print(form.getvalue("key1"))

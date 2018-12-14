#!/usr/bin/python3

import cgi
import time
import os

form = cgi.FieldStorage()
print("Content-Type: text/html\n\n")
num = form.getvalue("key")
print("RasPI took " + num + ".jpg!")

os.system("./take_annotation.sh " + num)

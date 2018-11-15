#!/usr/bin/python3
# -*- coding: utf-8 -*-
import cgi
from ev3dev.ev3 import *
import time

'''
form = cgi.FieldStorage()
print("Content-Type: text/html\n\n")
print(form.getvalue("key0"))

music = [];
for i in range(6):
    key = "key" + str(i)
    value = tuple(form.getvalue(key))
    music.append(value)
'''

#aa = (('D4', 'e3'),('A4', 'h.'))
aa = (('D4', 'e3'),('D4', 'e3'),('D4', 'e3'),('G4', 'h.'),('D5', 'h.'),('C5', 'e3'))
#aa = tuple(music)
print(aa)

Sound.set_volume(1)
print(Sound.get_volume())
Sound.play_song(aa)

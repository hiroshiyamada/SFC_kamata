import glob
import os

for i in range(14):
    for j in range(4):
        f = "./Images/00" + str(j)
        os.system("cat "+f+" >> OutFile"+ str(j)+".txt")

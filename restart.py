import os
from time import sleep

os.system("sudo pkill -f 'Totem.py'")
sleep(0.5)
os.system("sudo python3 /home/wareid/Totem/Totem.py")

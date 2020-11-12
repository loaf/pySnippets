from telnetlib import Telnet
import time

tn = Telnet("10.10.10.1", port=23, timeout=10)
    # tn.set_debuglevel(2)
tn.read_until(b"Username:")
tn.write(b'admin\n')

tn.read_until(b"Password:")
tn.write(b"admin@123\n")
    #tn.read_until(b"Chaos")
time.sleep(2)

#tn.write(b"system-view\n")
tn.write(b"reboot\n")
tn.read_until(b"System will reboot! Continue?[Y/N]:")
tn.write(b"Y\n")

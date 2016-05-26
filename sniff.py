from scapy.all import *
import netifaces
import time, threading
print "here is your network interfaces list"
ifaces = netifaces.interfaces()
print(ifaces)
num = input("choose a interface")
id = 0;
lock = threading.Lock()
def showit(pack):
	global id,lock
	lock.acquire();
	id = id +1;
	filename = str(id)+'.cap';
	lock.release();
	wrpcap(filename,pack)
	pack.show()
for i in range(10):
	pks = sniff(iface=ifaces[num],filter="", count=1)
 	threading.Thread(target=showit, args=(pks,)).start()
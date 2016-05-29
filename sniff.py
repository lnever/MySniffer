from scapy.all import *
import netifaces
import time, threading
import shutil


from choosenetifacedialog import ChooseNetifaceDialog
from inputdialog import InputDialog

lock = threading.Lock()
id = 0
class recv:
	def __init__(self):
		self.res=""
		self.__console__=sys.stdout
	def write(self,str):
		self.res += str
	def getres(self):
		sys.stdout.write(self.res)
		return self.res
	def flush(self): 
		self.res="" 
 
 	def reset(self): 
 		sys.stdout=self.__console__

class Sniffer():
	

    def __init__(self):
        if os.path.exists("tmp"):
    	   shutil.rmtree("tmp")
    	
        self.iface = ""
        self.filter = ""
        self.count = 1
        
        os.mkdir("tmp")

    def save(self, pack, id):
        filename = "tmp/"+str(id) + '.cap'
        wrpcap(filename, pack)

    def setiface(self):
        option, isOk = ChooseNetifaceDialog.getCheckedOption(netifaces.interfaces())
        self.iface = str(option)
        return option
    
    def setfilter(self):
    	text = "Input filter here"
        option = InputDialog.getInputResult(text)
        self.filter = str(option)
        return option
    
    def showdetail(self):
        text = "Input the package number here"
        option = InputDialog.getInputResult(text)
        if os.path.exists("tmp/"+str(option)+".cap"):
        	pkts = rdpcap("tmp/"+str(option)+".cap")

        	it = recv()
        	sys.stdout = it
        	
        	pkts[0].show()
        	res = it.getres()
        	#sys.stdout = stdout
        	it.flush()
        	it.reset()
        	#print(self.filter)
        	return res

        else :
        	return "Input error or No such file"

    def savepackage(self):
        text = "Input the package number here"
        num = InputDialog.getInputResult(text)
        if os.path.exists("tmp/"+str(num)+".cap"):
        	
        	pkts = rdpcap("tmp/"+str(num)+".cap")
        	
        	text = "Input the filename here"
        	name = InputDialog.getInputResult(text)
        
        	filename = name+".cap"
        	if os.path.exists(filename):
        		filename = name+"(1).cap"
        	wrpcap(filename,pkts[0])
        	return "The no. "+num +" is saved as " +filename 
        
        else :
        	return "Input error or No such file"

        

    def sniff(self):
        if self.iface == "":
            self.iface = netifaces.interfaces()[0]
        #print("!!!!!!!!!!!!!!!!!!!"+self.filter)
        pks = sniff(iface=self.iface, filter=self.filter, count=self.count)[0]
        print(pks.summary())
        global id, lock
        lock.acquire();
        id = id + 1;
        nid = id;
        threading.Thread(target=self.save, args=(pks[0],nid,)).start()
        lock.release();
        return "[" + str(nid) + "] : " + str(pks.summary())


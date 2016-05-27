# -*- coding: UTF-8 -*-
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from scapy.all import *
import netifaces
import time, threading

from choosenetifacedialog import ChooseNetifaceDialog


lock = threading.Lock()
id = 0


class Sniffer():
    def __init__(self):
        self.iface = ""
        self.filter = ""
        self.count = 1

    def save(self, pack, id):
        filename = str(id) + '.cap'
        wrpcap(filename, pack)

    def getiface(self):
        option, isOk = ChooseNetifaceDialog.getCheckedOption(netifaces.interfaces())
        return option

    def setiface(self, num):
        self.iface = netifaces.interfaces()[num]

    def getfilter(self):
        return str

    def setifilter(self, num):
        # sel.iface=netifaces.interfaces()[num]
        pass

    def sniff(self):
        if self.iface == "":
            self.iface = netifaces.interfaces()[0]
        pks = sniff(iface=self.iface, filter="", count=self.count)[0]
        print(pks.summary())
        global id, lock
        lock.acquire();
        id = id + 1;
        nid = id;
        lock.release();
        return "[" + str(nid) + "] : " + str(pks.summary())

    # threading.Thread(target=showit, args=(pks,)).start()


class Form(QDialog):
    def __init__(self, parent=None):

        self.working = False
        self.s = Sniffer()

        super(Form, self).__init__(parent)
        self.browser = QTextBrowser()
        self.biface = QPushButton("Choose netiface")
        self.bfilter = QPushButton("Set filter")
        self.bstart = QPushButton("Start sniffing")
        self.bshow = QPushButton("Show detail")

        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        layout1 = QHBoxLayout()
        layout1.addWidget(self.biface)
        layout1.addWidget(self.bfilter)
        layout1.addWidget(self.bstart)
        # layout1.addWidget(self.bshow)

        layout.addLayout(layout1)

        self.setGeometry(300, 300, 600, 400)
        self.setLayout(layout)
        self.connect(self.biface, SIGNAL('clicked()'), self.setiface)
        self.connect(self.bstart, SIGNAL('clicked()'), self.start)
        self.setWindowTitle("MySniffer")

    def showit(self, message):
        self.browser.append(message)

    def setiface(self):
        self.showit(self.s.getiface())

    def work(self):
        while self.working:
            mess = self.s.sniff()
            threading.Thread(target=self.showit, args=(mess,)).start()
        return

    def start(self):
        if self.working:
            self.working = False
        else:
            self.working = True
            threading.Thread(target=self.work, args=()).start()


app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()

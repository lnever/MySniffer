# -*- coding: UTF-8 -*-
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from scapy.all import *
import netifaces
import time, threading



from sniff import Sniffer






class Form(QDialog):

    def __init__(self, parent=None):

        self.working = False
        self.s = Sniffer()

        super(Form, self).__init__(parent)
        self.browser = QTextBrowser()
        self.biface = QPushButton("Choose netiface")
        self.bfilter = QPushButton("Set filter")
        self.bstart = QPushButton("Start/Stop sniffing")
        self.bdetail= QPushButton("Show detail")
        self.bsave= QPushButton("Save package")



        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        layout1 = QHBoxLayout()
        layout1.addWidget(self.biface)
        layout1.addWidget(self.bfilter)
        layout1.addWidget(self.bstart)
        layout1.addWidget(self.bdetail)
        layout1.addWidget(self.bsave)

        layout.addLayout(layout1)

        self.setGeometry(300, 300, 600, 400)
        self.setLayout(layout)
        self.connect(self.biface, SIGNAL('clicked()'), self.setiface)
        self.connect(self.bstart, SIGNAL('clicked()'), self.start)
        self.connect(self.bfilter, SIGNAL('clicked()'), self.setfilter)
        self.connect(self.bdetail, SIGNAL('clicked()'), self.showdetail)
        self.connect(self.bsave, SIGNAL('clicked()'), self.savepackage)
        self.setWindowTitle("MySniffer")

    def showit(self, message):
        self.browser.append(message)

    def setiface(self):
        res = self.s.setiface()
        self.showit("the netiface is set to :\n"+res)
        #self.s.iface = str(res)

    def setfilter(self):
        res = self.s.setfilter()
        self.showit("the filter is set to :\n"+res)
        #self.s.filter = str(res)

    def showdetail(self):
        if self.working:
            self.showit("Please do it while sniffing is stoped !")
            return
        res = self.s.showdetail()
        self.showit("the detail is :\n"+res)
        self.s.filter = str(res)

    def savepackage(self):
        if self.working:
            self.showit("Please do it while sniffing is stoped !")
            return
        res = self.s.savepackage()
        self.showit("saving... :\n"+res)
        self.s.filter = str(res)


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


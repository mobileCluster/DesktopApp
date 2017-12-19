#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Frontend Imports """

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from datetime import datetime
from datetime import timedelta
import pyqtgraph as pg
import numpy as np
from random import randint
import socket

from thread1 import Thread1
from threadUpdate import ThreadUpdate
from __global__ import my_global
""" Frontend """

class RHM(QWidget):

    ## Main UI Code     
        
    def __init__(self):
        super(RHM, self).__init__()     
        self.initUI()
        
    def initUI(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)
        self.setWindowTitle('Remote Health Monitoring')
        self.grid = QGridLayout()
        self.grid.setContentsMargins(30, 30, 30, 30)
        self.grid.setSpacing(20)
        self.setLayout(self.grid)
        self.interface0()
        self.showFullScreen()

    def interface0(self):
        # global my_global
            
        for i in reversed(range(self.grid.count())): 
            self.grid.itemAt(i).widget().setParent(None)


        # self.setWindowFlags(Qt.FramelessWindowHint)
        # -self.setAttribute(Qt.WA_TranslucentBackground)
    
        font1 = QFont()
        font1.setPointSize(30)
        font1.setFamily("Monospace")

        lbl = QLabel("Waiting for master to connect...")
        self.movie = QMovie("1.gif")
        self.movie.frameChanged.connect(self.repaint)
        lbl.setMovie(self.movie)
        self.movie.start()
        self.grid.addWidget(lbl,1,1,2,1)

        text1 = QTextBrowser(self)
        text1.setFont(font1)
        text1.setText("REMOTE HEALTH MONITORING")
        text1.setStyleSheet("color:lightgrey;border: 0px;padding-top: 30%;background:transparent;")
        text1.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(text1, 0,0,1,3)

        font2 = QFont()
        font2.setPointSize(20)
        font2.setFamily("Monospace")

        text2 = QTextBrowser(self)
        text2.setFont(font2)
        text2.setText("Waiting for master to connect...")
        text2.setStyleSheet("color:lightgrey;border: 0px;padding-top: 50%;background:transparent;")
        text2.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(text2, 3,0,1,3)

        
        add = socket.gethostbyname(socket.gethostname())
        
        text3 = QTextBrowser(self)
        text3.setFont(font2)
        text3.setText("IP : "+str(add))
        text3.setStyleSheet("color:lightgrey;border:0px;background:transparent;")
        text3.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(text3, 4,0,1,3)

        self.thread = Thread1()
        self.connect(self.thread, SIGNAL("interface1()"), self.interface1)
        self.thread.start()
		
        
        self.show()


    def interface1(self):
        self.thread.terminate()
        
        for i in reversed(range(self.grid.count())): 
            self.grid.itemAt(i).widget().setParent(None)

        font1 = QFont()
        font1.setPointSize(30)
        font1.setFamily("Monospace")

        text1 = QTextBrowser(self)
        text1.setFont(font1)
        text1.setText("REMOTE HEALTH MONITORING")
        text1.setStyleSheet("color:lightgrey;border: 0px;padding-top: 30%;background:transparent;")
        text1.setAlignment(Qt.AlignCenter)
        self.grid.addWidget(text1, 1,1,2,4)

        font2 = QFont()
        font2.setPointSize(30)
        font2.setFamily("Monospace")

        self.out = []
        self.plot = []
        self.stat = []

        for i in range(8):
            self.plot.append(0)

            self.out.append([])
        
        font2 = QFont()
        font2.setPointSize(15)
        font2.setFamily("Monospace")

        for i in range(4):
            self.stat.append(QTextBrowser(self))
            self.stat[i].setFont(font2)
            self.stat[i].setText("No Device")
            self.stat[i].setStyleSheet("text-align:center;color:white;background:transparent;")
            self.stat[i].setAlignment(Qt.AlignCenter)
            self.grid.addWidget(self.stat[i], 3,i+1,1,1)
        
        self.plot[0] = pg.PlotWidget(title="CPU USAGE")
        self.grid.addWidget(self.plot[0], 4,1,2,1)
        self.plot[2] = pg.PlotWidget(title="CPU USAGE")
        self.grid.addWidget(self.plot[2], 4,2,2,1)
        self.plot[4] = pg.PlotWidget(title="CPU USAGE")
        self.grid.addWidget(self.plot[4], 4,3,2,1)
        self.plot[6] = pg.PlotWidget(title="CPU USAGE")
        self.grid.addWidget(self.plot[6], 4,4,2,1)
        self.plot[1] = pg.PlotWidget(title="MEMORY USAGE")
        self.grid.addWidget(self.plot[1], 6,1,2,1)
        self.plot[3] = pg.PlotWidget(title="MEMORY USAGE")
        self.grid.addWidget(self.plot[3], 6,2,2,1)
        self.plot[5] = pg.PlotWidget(title="MEMORY USAGE")
        self.grid.addWidget(self.plot[5], 6,3,2,1)
        self.plot[7] = pg.PlotWidget(title="MEMORY USAGE")
        self.grid.addWidget(self.plot[7], 6,4,2,1)

        self.threadUpdate = ThreadUpdate()
        self.connect(self.threadUpdate, SIGNAL("update()"), self.update)
        self.threadUpdate.start()
        
        self.show()

    def update(self):
        global my_global
        for i in range(4):
            if my_global['data'][i]['status']=='online':
                self.out[2*i].append(my_global['data'][i]['cpu'])
                self.out[2*i+1].append(my_global['data'][i]['memory'])
                self.stat[i].setStyleSheet("text-align:center;color:white;background:transparent;")
                self.stat[i].setText(str(my_global['data'][i]['name']))
                self.stat[i].setAlignment(Qt.AlignCenter)
        for i in range(8):
            if len(self.out[i])>40:
                self.out[i].pop(0)
            self.plot[i].clear()
            self.plot[i].setXRange(0,40, padding=0)
            self.plot[i].plot(self.out[i])
            """if len(self.data[i])<40:
                self.plot[i].setXRange(0,40, padding=0)
            else:
                self.plot[i].setXRange(len(self.data[i])-40,len(self.data[i]), padding=0)"""

def main():
    app = QApplication(sys.argv)
    # app.setStyle(QStyleFactory.create("plastique"))
    ex = RHM()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

from PyQt4.QtCore import QThread, SIGNAL
import socket
import json
from __global__ import my_global

class ThreadUpdate(QThread):
    def __init__(self):
        QThread.__init__(self)
    def __del__(self):
        self.wait()

    def run(self):
        global my_global
        while(True):
            data = my_global['conn'].recv(1024)
            data = json.loads(data[2:])
            my_global['data'] = data['Data']
            self.emit(SIGNAL('update()'))
            """
            for i in range(4):
                print("Data for "+str(i))
                print("ID : "+str(data[i]['id']))
                print("Status : "+str(data[i]['status']))
                if str(data[i]['Status']=="Online"):
                    print("CPU : "+str(data[i]['cpu']))
                    print("Memory : "+str(data[i]['memory']))
        	print("")
            """
                        


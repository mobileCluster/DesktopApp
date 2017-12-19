from PyQt4.QtCore import QThread, SIGNAL
import socket
from __global__ import my_global

class Thread1(QThread):
    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        global my_global
        port = 6680
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', port))
        s.listen(1)
        my_global['conn'], my_global['addr'] = s.accept()
        self.emit(SIGNAL('interface1()'))

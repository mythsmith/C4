import unittest
import os

from PyQt4 import QtGui, QtCore

from C4.MainWindow import MainWindow

app = QtGui.QApplication([])

testdb = os.path.expanduser('~/c4test.sqlite')

class TestBoard(unittest.TestCase):
    def tearDown(self):
        if os.path.exists(testdb):
            os.remove(testdb)
    
    def test_exec(self):
        w = MainWindow(testdb)
        w.show()
        QtGui.qApp.exec_()
        
        

if __name__ == "__main__":
    unittest.main()
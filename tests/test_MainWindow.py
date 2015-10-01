import unittest

from PyQt4 import QtGui, QtCore

from C4.MainWindow import MainWindow

app = QtGui.QApplication([])


class TestBoard(unittest.TestCase):
    
    def test_exec(self):
        w = MainWindow()
        w.show()
        QtGui.qApp.exec_()
        
        

if __name__ == "__main__":
    unittest.main()
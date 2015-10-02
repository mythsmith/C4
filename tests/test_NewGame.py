import unittest
import os

from PyQt4 import QtGui, QtCore

from C4.NewGame import NewGame

app = QtGui.QApplication([])

class TestNewGame(unittest.TestCase):
    def test_exec(self):
        w = NewGame()
        w.show()
        QtGui.qApp.exec_()
        
        

if __name__ == "__main__":
    unittest.main()
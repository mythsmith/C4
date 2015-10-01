
import unittest
import sys

from PyQt4 import QtGui, QtCore

from C4.GameMatrix import GameMatrix
from C4.BoardScene import BoardScene


class TestBoard(unittest.TestCase):
    def test_init(self):
        app = QtGui.QApplication(sys.argv)
        m = GameMatrix()
        b = BoardScene(m)
        b.setSceneRect(0,0,500,500)
        v = QtGui.QGraphicsView(b)
        
        
        v.show()
        QtGui.qApp.exec_()
        
        

if __name__ == "__main__":
    unittest.main()

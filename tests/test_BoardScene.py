
import unittest

from PyQt4 import QtGui, QtCore

from C4.GameMatrix import GameMatrix
from C4.BoardScene import BoardScene

app = QtGui.QApplication([])
    

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.m = GameMatrix()
        self.b = BoardScene(self.m)
        self.b.setSceneRect(0,0,700,600)
    
    def test_conversion_factors(self):
        m,b = self.m, self.b
        m = GameMatrix()
        b= BoardScene(m)
        b.setSceneRect(0,0,700,600)
        delta_w, delta_h, mw, mh = b.conversion_factors()
        self.assertEqual(mw, 7)
        self.assertEqual(mh, 6)
        self.assertEqual(delta_h, 100)
        self.assertEqual(delta_w, 100)
        
    def test_get_matrix_coords(self):
        m, b = self.m, self.b
        ret = b.get_matrix_coords(600, 0)
        self.assertEqual(ret, (0, 0))
        ret = b.get_matrix_coords(0, 0)
        self.assertEqual(ret, (5, 0))
        ret = b.get_matrix_coords(600, 700)
        self.assertEqual(ret, (0, 6))       
        ret = b.get_matrix_coords(200, 400)
        self.assertEqual(ret, (3, 4))   
        ret = b.get_matrix_coords(200, 399)
        self.assertEqual(ret, (3, 3))       
    
    def test_get_scene_coords(self):
        m, b = self.m, self.b
        ret = b.get_scene_coords(0, 0)
        self.assertEqual(ret, (0, 500))
        ret = b.get_scene_coords(5, 0)
        self.assertEqual(ret, (0, 0))    
        ret = b.get_scene_coords(0, 6)
        self.assertEqual(ret, (600, 500))   
        ret = b.get_scene_coords(3, 4)
        self.assertEqual(ret, (400, 200))
        ret = b.get_scene_coords(3, 3)
        self.assertEqual(ret, (300, 200))
    
    def test_exec(self):
        m,b = self.m, self.b
        v = QtGui.QGraphicsView(b)
        v.show()
        QtGui.qApp.exec_()
        
        

if __name__ == "__main__":
    unittest.main()

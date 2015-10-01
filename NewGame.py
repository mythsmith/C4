from PyQt4 import QtCore, QtGui

class NewGame(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent=parent)
        self.user1 = QtGui.QLineEdit()
        self.user2 = QtGui.QLineEdit()
        self.width = QtGui.QSpinBox()
        self.width.setValue(7)
        self.width.setRange(1,100)
        self.height = QtGui.QSpinBox()
        self.height.setValue(6)
        self.height.setRange(1,100)
        self.goal = QtGui.QSpinBox()
        self.goal.setValue(4)
        self.goal.setRange(2,10)
        self.start = QtGui.QPushButton('Start!')
        self.start.clicked.connect(self.done)
        lay = QtGui.QFormLayout()
        lay.addRow('User Red:', self.user1)
        lay.addRow('User Green:', self.user2)
        lay.addRow('Width:',self.width)
        lay.addRow('Height:',self.height)
        lay.addRow('Connect Goal:',self.goal)
        lay.addRow('',self.start)
        self.setLayout(lay)
        
        

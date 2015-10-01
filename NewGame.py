from PyQt4 import QtCore, QtGui

class NewGame(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent=parent)
        self.user1 = QtGui.QLineEdit()
        self.user2 = QtGui.QLineEdit()
        lay = QtGui.QFormLayout()
        lay.addRow('User 1:', self.user1)
        lay.addRow('User 2:', self.user2)
        self.setLayout(lay)

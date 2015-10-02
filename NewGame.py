from PyQt4 import QtCore, QtGui

class NewGame(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent=parent)
        self.players = QtGui.QSpinBox()
        self.players.setValue(2)
        self.players.setRange(2,10)
        self.players.valueChanged.connect(self.update_players)
        self.users = []
        
        self.dimensions = QtGui.QSpinBox()
        self.dimensions.setValue(2)
        self.dimensions.setRange(2,10)
        self.dimensions.valueChanged.connect(self.update_dimensions)       
        self.dims = []
        
        self.goal = QtGui.QSpinBox()
        self.goal.setValue(4)
        self.goal.setRange(2,10)
        self.start = QtGui.QPushButton('Start!')
        self.start.clicked.connect(self.done)
        lay = QtGui.QFormLayout()
        lay.addRow('Players:',self.players)
        lay.addRow('Dimensions:',self.dimensions)
        lay.addRow('Connect Goal:',self.goal)
        lay.addRow('',self.start)
        self.setLayout(lay)
        self.update_players()
        
    def update_players(self, *a):
        """Update player name input fields"""
        lay = self.layout()
        for i, wg in enumerate(self.users):
            for col in (0,1):
                item = lay.itemAt(i+1,col)
                lay.removeItem(item)
                item.widget().close()
        n = self.players.value()
        self.users = []
        for i in xrange(1,n+1):
            user = QtGui.QLineEdit()
            lay.insertRow(i, 'User {}'.format(i), user)
            self.users.append(user)
            
    def updae_dimensions(self):
        """Update dimension input fields"""
        lay = self.layout()
        u = self.users.value()
        for i, wg in enumerate(self.dims):
            for col in (0,1):
                item = lay.itemAt(i+1,col)
                lay.removeItem(item)
                item.widget().close()  
        n = self.dimensions.value()
             
            
        
        
        

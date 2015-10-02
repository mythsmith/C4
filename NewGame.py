from PyQt4 import QtCore, QtGui

class NewGame(QtGui.QDialog):
    
    """Configure a new game"""
    
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
        self.update_dimensions()
        
    def update_players(self, *a):
        """Update player name input fields"""
        lay = self.layout()
        base = 0
        for i, wg in enumerate(self.users):
            for col in (0,1):
                item = lay.itemAt(i+base,col)
                lay.removeItem(item)
                item.widget().close()
        n = self.players.value()
        self.users = []
        for i in xrange(n):
            user = QtGui.QLineEdit()
            lay.insertRow(i+base, 'User {}:'.format(i+1), user)
            self.users.append(user)
            
    def update_dimensions(self):
        """Update dimension input fields"""
        lay = self.layout()
        base = self.players.value()
        for i in xrange(lay.rowCount()-3-base-1):
            for col in (0,1):
                item = lay.itemAt(i+base,col)
                print 'removing',i,base,i+base,col,item
                if item is None:
                    continue
                lay.removeItem(item)
                item.widget().close()
        n = self.dimensions.value()
        print 'new dimensions',n
        self.dims = []
        for i in xrange(n):
            dim = QtGui.QSpinBox()
            dim.setRange(2,100)
            if i==0:
                dim.setValue(6)
                label = 'Height ({}):'.format(i)
            elif i==1:
                dim.setValue(7)
                label = 'Width ({}):'.format(i)
            else:
                label = 'Dim ({})'.format(i)
            lay.insertRow(i+base, label, dim)
            self.dims.append(dim)
        print self.dims 
        
        
        

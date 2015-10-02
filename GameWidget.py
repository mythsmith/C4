from PyQt4 import QtCore, QtGui
from time import time
from C4.BoardScene import BoardScene

def diff_coord(val, dims):
    if val>0:
        val-=1
    elif val<dims-1:
        val+=1  
    return val 

class NDimensionPanel(QtGui.QWidget):
    
    """User controls to navigate through N-dimensions"""
    
    coords_changed = QtCore.pyqtSignal(object)
    
    def __init__(self,parent):
        QtGui.QWidget.__init__(self,parent)
        lay=QtGui.QHBoxLayout()
        game = parent.game
        n = game.dims
        self.vars = []
        for i in xrange(n-2):
            var = QtGui.QSpinBox()
            var.setRange(0,game.shape[i+2]-1)
            var.setValue(0)
            var.valueChanged.connect(self.apply)
            self.vars.append(var)
            label = QtGui.QLabel(' Dim {}:'.format(i+2))
            lay.addWidget(label)
            lay.addWidget(var)
        self.setLayout(lay)
            
    def apply(self):
        coords = [0, 0]
        for var in self.vars:
            coords.append(var.value())
        self.coords_changed.emit(coords)
        
        

class GameWidget(QtGui.QWidget):
    def __init__(self, game, user_map, user_uid, parent=None):
        QtGui.QWidget.__init__(self, parent=parent)
        self.game = game
        self.user_map = user_map  # palyer:uid
        self.user_uid = user_uid  # name:uid
    
        users = []
        for player_idx in xrange(1,game.players+1):
            uid = user_map[player_idx]
            i = user_uid.values().index(uid)
            users.append(user_uid.keys()[i])
        self.scene = BoardScene(game, user_names = users)
        self.scene.setSceneRect(0, 0, 700, 600)
        self.view = QtGui.QGraphicsView(self.scene)
        self.view.setMouseTracking(True)
        
        self.stats = QtGui.QLabel('')
        
        lay = QtGui.QVBoxLayout()
        if game.dims>2:
            self.dimensions = NDimensionPanel(self)
            self.dimensions.coords_changed.connect(self.scene.sync)
            lay.addWidget(self.dimensions)
        lay.addWidget(self.view)
        lay.addWidget(self.stats)
        self.setLayout(lay)
        
        # Hook for self-update
        self.scene.signal_new_cell = self.update_clock
        self.timer = QtCore.QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start()
        
    def update_clock(self, *a):
        """Update time game clock"""
        text = 'Game Clock \n'
        names = self.user_uid.keys()
        uids = self.user_uid.values()
        if self.game.winner_idx:
            self.timer.stop()
            return
        # Paused
        if not self.game.zerotime:
            return
        for player, uid in self.user_map.iteritems():
            score = self.game.scores[player]
            i = uids.index(uid)
            name = names[i]
            if player == self.game.player_idx:
                score += time() - self.game.zerotime
            text += ' Player "{}": {}   '.format(name, int(score))
        self.stats.setText(text)
        
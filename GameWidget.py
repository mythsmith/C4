from PyQt4 import QtCore, QtGui
from time import time
from C4.BoardScene import BoardScene

class GameWidget(QtGui.QWidget):
    def __init__(self, game, user_map, user_uid, parent=None):
        QtGui.QWidget.__init__(self, parent=parent)
        self.game = game
        self.user_map = user_map  # palyer:uid
        self.user_uid = user_uid  # name:uid
    
        self.scene = BoardScene(game)
        self.scene.setSceneRect(0, 0, 700, 600)
        self.view = QtGui.QGraphicsView(self.scene)
        self.view.setMouseTracking(True)
        
        self.stats = QtGui.QLabel('')
        
        lay = QtGui.QVBoxLayout()
        lay.addWidget(self.stats)
        lay.addWidget(self.view)
        
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
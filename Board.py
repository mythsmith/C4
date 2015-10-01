from PyQt4 import QtCore, QtGui
import numpy as np


class BoardScene(QtGui.QGraphicsScene):
    signal_new_cell = lambda *a: 0
    signal_winner = lambda *a: 0
    winner_idx = 0
    
    def __init__(self, matrix, parent = None):
        QtGui.QGraphicsScene.__init__(self, parent=parent)
        self.game = matrix
        self.player_idx = 1
        self.item_map = {}
        
    def conversion_factors(self):
        rect = self.sceneRect()
        w, h = float(rect.width()), float(rect.height())
        mh, mw = self.game.shape 
        delta_h, delta_w = h/mh, w/mw
        return delta_w, delta_h, mw, mh   
        
    def get_matrix_coords(self, y, x):
        """Converts scene coords into matrix coords tuple"""
        delta_w, delta_h, mw, mh = self.conversion_factors()
        ix = int(x/delta_w)
        iy = int(y/delta_h)
        return mh-iy-1, ix
    
    def get_scene_coords(self, iy, ix):
        """Converts matrix coords into scene coordinates""" 
        delta_w, delta_h, mw, mh = self.conversion_factors()
        mh, mw = self.game.shape 
        x = (ix)*delta_w
        y = (mh - iy - 1)*delta_h
        return x, y
        
    def occupy(self, coords):
        matrix_coords = self.get_matrix_coords(*coords)
        real_coords = self.game.occupy(matrix_coords, self.player_idx)
        print 'occupy',coords,matrix_coords, real_coords
        if real_coords is False:
            return False
        self.set_cell(real_coords)
        self.signal_new_cell(real_coords, self.player_idx)
        winner = self.game.validate()
        if winner is False:
            self.next_player()
            return True
        self.winner_idx, self.winning_cells = winner
        self.signal_winner(self.winner_idx)
        self.highlight_winner()
        
    def highlight_winner(self):
        pass
    
    def next_player(self):
         # Next player
        self.player_idx += 1
        if self.player_idx > self.game.players:
            self.player_idx = 1       
        
    def mouseDoubleClickEvent(self, *args, **kwargs):
        ret = QtGui.QGraphicsScene.mouseDoubleClickEvent(self, *args, **kwargs)
        # Disable events if we already have a winner
        if self.winner_idx:
            return ret
        event = args[0]
        pos = event.scenePos()
        x, y = pos.x(), pos.y()
        real_coords = self.occupy((y, x))
        if not real_coords:
            return ret
        return ret
    
    def set_cell(self, coords):
        player_idx = self.game.matrix[coords]
        scene_coords = self.get_scene_coords(*coords)
        item = self.item_map.get(coords,False)
        if item:
            print 'item found, removing:',coords, item
            self.removeItem(item)
            self.item_map.pop(coords)
        if not player_idx:
            return False
        print 'set_cell',player_idx, scene_coords
        item = self.addSimpleText(str(player_idx))
        item.setPos(*scene_coords)
        self.item_map[coords] = item
        return player_idx
        
    
    def sync(self):
        """Sync scene with matrix data"""
        it = np.nditer(self.game.matrix, flags=['multi_index','refs_ok'])
        while not it.finished:
            player_idx = self.game.matrix[it.multi_index]
            self.set_cell(it.multi_index)
            it.iternext()
        

        
    
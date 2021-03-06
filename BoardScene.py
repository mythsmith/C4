from PyQt4 import QtCore, QtGui
import numpy as np

from C4.Game2dProxy import Game2dProxy


class BoardScene(QtGui.QGraphicsScene):
    
    """Game UI"""
    signal_new_cell = lambda *a: 0
    signal_winner = lambda *a: 0
    line_width = 4
    
    def __init__(self, game, user_names = False, colors=False, parent=None):
        QtGui.QGraphicsScene.__init__(self, parent=parent)
        self.game = game
        self.game2d = Game2dProxy(self.game)
        self.user_names = user_names
        self.item_map = {}
        if colors is False:
            colors = {p:int(6 + p) for p in range(1, game.players + 1)}
        self.colors = colors
        rect = QtCore.QRectF(0, 0, 0, 0)
        self.mouse_track = self.addRect(rect)
        self.mouse_text = self.addSimpleText('')
        
    def setSceneRect(self, *a, **k):
        r = QtGui.QGraphicsScene.setSceneRect(self, *a, **k)
        self.draw_grid()
        return r
    
    def conversion_factors(self):
        rect = self.sceneRect()
        w, h = float(rect.width()), float(rect.height())
        mh, mw = self.game2d.shape
        delta_h, delta_w = h / mh, w / mw
        return delta_w, delta_h, mw, mh   
    
    def draw_grid(self):
        delta_w, delta_h, mw, mh = self.conversion_factors()
        rect = self.sceneRect()
        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor(0, 0, 0))
        pen.setWidth(self.line_width)
        for i in range(mw + 1):
            x = i * delta_w
            self.addLine(x, 0, x, rect.height(), pen)
        for j in range(mh + 1):  
            y = j * delta_h
            self.addLine(0, y, rect.width(), y, pen)
        
    def get_matrix_coords(self, y, x):
        """Converts scene coords into matrix coords tuple
        Returns y,x cell."""
        delta_w, delta_h, mw, mh = self.conversion_factors()
        ix = int(x / delta_w)
        iy = int(y / delta_h)
        # Enforce boundaries
        if iy == mh: 
            iy = mh - 1
        if ix == mw: 
            ix = mw - 1
        return mh - iy - 1, ix
    
    def get_scene_coords(self, iy, ix):
        """Converts matrix coords into scene coordinates.
        Returns x,y upper-left scene coords.""" 
        delta_w, delta_h, mw, mh = self.conversion_factors()
        mh, mw = self.game2d.shape 
        x = (ix) * delta_w
        y = (mh - iy - 1) * delta_h
        return x, y
        
        
    def occupy(self, coords):
        matrix_coords = self.get_matrix_coords(*coords)
        real_coords = self.game2d.occupy(matrix_coords)
        print 'occupy', coords, matrix_coords, real_coords
        if real_coords is False:
            return False
        self.set_cell(real_coords)
        winner = self.game.validate()
        if winner is not False:
            self.highlight_winner()
        self.signal_new_cell()
        return True
        
    def highlight_winner(self):
        for cell in self.game2d.winning_cells:
            py, px = cell
            item = self.item_map[(py, px)]
            brush = item.brush()
            brush.setStyle(QtCore.Qt.Dense3Pattern)
            item.setBrush(brush)
            pen = item.pen()
            pen.setWidth(10)
            pen.setColor(brush.color())
            item.setPen(pen)
            
    def mouseMoveEvent(self, *args, **kwargs):
        if self.game.winner_idx:
            self.mouse_track.hide()
            self.mouse_text.hide()
            return 
        pos = args[0].scenePos()
        x, y = pos.x(), pos.y()
        delta_w, delta_h, mw, mh = self.conversion_factors()
        w2 = delta_w / 2   
        h2 = delta_h / 2
        max_x = self.sceneRect().width() - w2
        if x < w2:
            x = w2
        elif x > max_x:
            x = max_x
        rect = QtCore.QRectF(x-w2, 0, delta_w, delta_h)
        self.mouse_track.setRect(rect)
        brush = QtGui.QBrush()
        brush.setStyle(QtCore.Qt.SolidPattern)
        brush.setColor(self.colors[self.game.player_idx])
        self.mouse_track.setBrush(brush)
        self.mouse_text.setPos(x+10,y+10)
        if self.user_names:
            txt = self.user_names[self.game.player_idx-1]
            self.mouse_text.setText(txt)
        return 
        
    def mouseDoubleClickEvent(self, *args, **kwargs):
        # Disable events if we already have a winner
        if self.game.winner_idx:
            return 
        event = args[0]
        pos = event.scenePos()
        x, y = pos.x(), pos.y()
        real_coords = self.occupy((y, x))
        if not real_coords:
            return 
        self.mouseMoveEvent(event)
        return 
    
    def set_cell(self, coords):
        """Color cell coords with current player_idx color"""
        player_idx = self.game2d.matrix[coords]
        scene_coords = self.get_scene_coords(*coords)
        item = self.item_map.get(coords, False)
        if item:
            print 'item found, removing:', coords, item
            self.removeItem(item)
            self.item_map.pop(coords)
        if not player_idx:
            return False
        print 'set_cell', player_idx, scene_coords
        delta_w, delta_h, mw, mh = self.conversion_factors()
        margin = self.line_width
        rect = QtCore.QRectF(scene_coords[0] + margin / 2, scene_coords[1] + margin / 2, delta_w - margin, delta_h - margin)
        item = self.addRect(rect)
        brush = QtGui.QBrush()
        brush.setStyle(QtCore.Qt.SolidPattern)
        brush.setColor(self.colors[player_idx])
        item.setBrush(brush)
        self.item_map[coords] = item
        return player_idx
        
    
    def sync(self,coord_mask=False):
        """Sync scene with matrix data"""
        if coord_mask:
            self.game2d.coord_mask=coord_mask
        it = np.nditer(self.game2d.matrix, flags=['multi_index', 'refs_ok'])
        while not it.finished:
            player_idx = self.game2d.matrix[it.multi_index]
            self.set_cell(it.multi_index)
            it.iternext()
        self.game.validate()
        self.highlight_winner()
        

        
    

import numpy as np

class Game2dProxy(object):
    
    """Reduction of N-Dimensional GameMatrix into a 2D slice"""
    
    def __init__(self, game):
        self.game = game
        self.coord_mask = [0] * self.game.dims
        self.coord_y = 0  # index of current y coord in coord_mask
        self.coord_x = 1  # index of current x coord in coord_mask
        
    @property
    def shape(self):
        """Returns the shape of the selected layer"""
        return self.game.shape[self.coord_y], self.game.shape[self.coord_x]
    
    @property
    def mask(self):
        """Masking selection to get 2D plane"""
        mask = self.coord_mask[:]
        mask[self.coord_x] = slice(None, None)
        mask[self.coord_y] = slice(None, None)
        return mask
    
    @property
    def winning_cells(self):
        """Returns only those cells which are visible in the coord_mask plane, in its coordinates"""
        cells = []
        check_coords = self.coord_mask[:]
        check_coords.pop(self.coord_x)
        check_coords.pop(self.coord_y)
        for cell in self.game.winning_cells:
           cell1 = list(cell[:])
           cell1.pop(self.coord_x)
           cell1.pop(self.coord_y)
           cell1 = np.array(cell1)
           # If all coords are equal except coord_x, coord_y,
           # the cell can be displayed
           if (cell1 == check_coords).all():
               cells.append((cell[self.coord_y],cell[self.coord_x]))
        return cells
    
    @property
    def matrix(self):
        """Return the active 2d plane"""
        return self.game.matrix[self.mask]
    
    def occupy(self, coords, player_idx=0):
        """Route occupy by completing the coordinates using the coord_mask"""
        mask = self.coord_mask[:]
        mask[self.coord_y] = coords[0]
        mask[self.coord_x] = coords[1]
        ret = self.game.occupy(tuple(mask), player_idx)
        return ret[self.coord_y],ret[self.coord_x]
    
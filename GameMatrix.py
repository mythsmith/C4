#!/usr/bin/python 

"""Basic Connect4 logic"""
import numpy as np
from time import time 
import scipy
from scipy import spatial
# shape = (y,x)
# slice [y,x]

def iter_matrix_translation(bool_matrix, translation=(1, 0), goal=4):
    """Reiterate `translation` on `bool_matrix` for `goal` times to check if there is at least one cell remaining always True"""
    bool_matrix = bool_matrix.copy()
    translation = np.array(translation)
    positive_slices = []
    negative_slices = []
    for i, v in enumerate(translation):
        if v == 0:
            positive_slices.append(slice(None, None))
            negative_slices.append(slice(None, None))
        else:
            positive_slices.append(slice(v, None))
            negative_slices.append(slice(None, -v))
    positive_slices = tuple(positive_slices)
    negative_slices = tuple(negative_slices)
    for i in xrange(goal - 1):
        positive_matrix = bool_matrix[positive_slices]
        negative_matrix = bool_matrix[negative_slices]
        bool_matrix = positive_matrix * negative_matrix
        print i, bool_matrix
        # If not true cell are left, it means this translation cannot find a solution
        if not bool_matrix.any():
            return False
    # Found a solution. 
    match = np.where(bool_matrix)
    # Collect winning cells by applying the translation goal-times
    coords = np.array(match)[:, 0]
    cells = [tuple(coords)]
    for i in xrange(goal - 1):
        coords += translation
        cells.append(tuple(coords))
    return cells
        
def scan(bool_matrix, goal=4):
    N = len(bool_matrix.shape)
    for i in xrange(1, 2 ** N):
        translation = [int(x) for x in bin(i)[2:]]
        # Pad with zeros if it's to small: a translation must have N-length
        longer = N - len(translation)
        if longer:
            translation = [0] * longer + translation
        print 'scan ', i, translation
        cells = iter_matrix_translation(bool_matrix, translation)
        if cells is not False:
            return cells
    # Nothing found
    return False
    


class GameMatrix(object):
    
    """Core logic of the game"""
    def __init__(self, shape=(6, 7), players=2, goal=4):
        self.matrix = np.zeros(shape)
        self.players = players
        self.goal = 4
        self.player_idx = 1 
        """Current player"""
        self.winner_idx = 0
        """Winner of the game"""
        self.winning_cells = []
        """Cells found as winners"""
        self.startdate = 0
        self.enddate = 0
        self.delta = 0
        self.zerotime = 0
        self.scores = {p:0 for p in range(1, players + 1)}
        
    @property
    def moves(self):
        """Returns current moves count on the matrix"""
        return np.count_nonzero(self.matrix)
    
    @property
    def shape(self):
        return self.matrix.shape
    
    @property
    def dims(self):
        return len(self.matrix.shape)
    
    # SCORES MANAGEMENT
        
    def start(self):
        """Start the game new"""
        self.startdate = time()
        self.zerotime = time()
        self.delta = 0
        
    def pause(self):
        """Pause the game: add to delta for later resume"""
        if not self.zerotime:
            return False
        self.delta += time() - self.zerotime
        self.zerotime = 0
        return True
        
    def resume(self):
        """Resume game: reset zerotime"""
        self.zerotime = time()
        
    def next_player(self):
        """Move turn to the next player"""
        self.scores[self.player_idx] += self.delta + time() - self.zerotime
        self.zerotime = time()
        self.player_idx += 1
        if self.player_idx > self.players:
            print 'resetting player_idx', self.player_idx, self.players
            self.player_idx = 1   
    
    # CELL OCCUPATION MANAGEMENT
    
    def gravity(self, coords):
        """Correct `coords` taking into account the effect of gravity on the first coordinate (y)"""
        coords = list(coords)
        c = coords[:]
        c[0] = slice(None)
        sub = self.matrix[c]
        match = np.where(sub > 0)[0]
        if len(match):
            coords[0] = max(match) + 1
        else:
            coords[0] = 0
        return tuple(coords)
    
    def occupy(self, coords, player_idx=0):
        """Occupy requested coords with player_idx. 
        Returns coords really occupied."""
        if not self.zerotime:
            self.zerotime = time()
        if self.matrix[coords] != 0:
            print "Coordinates are already occupied!"
            return False
        # Check for gravity
        real_coords = self.gravity(coords)
        if player_idx:
            self.player_idx = player_idx
        self.matrix[real_coords] = self.player_idx
        self.next_player()
        return real_coords
    
    # WINNER IDENTIFICATION
    
    def validate_player(self, player_idx):
        """Checks if player_idx is winning somewhere"""
        if self.moves < 4:
            return False
        print 'validate_player', player_idx
        bool_matrix = self.matrix == player_idx
        # No moves by this player
        if bool_matrix.sum() < self.goal:
            return False
        
        cells = scan(bool_matrix, self.goal)
        if not cells:
            return False
        
        self.winning_cells = cells
        self.enddate = time()
        self.winner_idx = player_idx
        print 'The winner is:', player_idx
        return cells

        
    def validate(self):
        """Finds adjacent occupied cells. 
        Returns False if we have no winner, otherwise return winner name and matched cells"""
        if self.moves < 4:
            return False
        print self.matrix
        for player_idx in range(1, self.players + 1):
            r = self.validate_player(player_idx)
            if r is False: continue
            return player_idx, r
        return False
        

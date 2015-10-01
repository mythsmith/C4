#!/usr/bin/python 

"""Basic Connect4 logic"""
import numpy as np

# shape = (y,x)
# slice [y,x]

def diff_match(d, start, goal=4):
    """Check for rising/stable match"""
    sublen = goal - 1
    sub = d[ start:start + sublen]
    rising = sub == [1]*sublen
    if rising.all():
        return 2
    rising = sub == [-1]*sublen
    if rising.all():
        return 2    
    stable = sub[:] == [0]*(sublen)
    if stable.all():
        return 1
    return 0

class GameMatrix(object):
    
    def __init__(self, shape=(6,7), players=2, goal=4):
        self.matrix = np.zeros(shape)
        self.players = 2
        self.goal  = 4
        self.player_idx = 1 
        """Current player"""
        self.winner_idx = 0
        """Winner of the game"""
        self.winning_cells = []
        """Cells found as winners"""
        
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
    
    def next_player(self):
         # Next player
        self.player_idx += 1
        if self.player_idx > self.players:
            self.player_idx = 1   
    
    def gravity(self, coords):
        """Correct `coords` taking into account the effect of gravity on the first coordinate (y)"""
        coords = list(coords)
        c = coords[:]
        c[0] = slice(None)
        sub = self.matrix[c]
        match = np.where(sub > 0)[0]
        if len(match):
            coords[0] = max(match)+1
        else:
            coords[0] = 0
        return tuple(coords)
    
    def occupy(self, coords, player_idx=0):
        """Occupy requested coords with player_idx. 
        Returns coords really occupied."""
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
        
    def validate_player(self, player_idx):
        """Checks if player_idx is winning somewhere"""
        if self.moves < 4:
            return False
        matches = np.where(self.matrix == player_idx)
        print 'matches',matches
        # No moves by this player
        if not len(matches):
            return False
        # No enough moves by this player
        if len(matches[0]) < self.goal:
            return False
        diffs = []
        for m in matches:
            d = np.diff(m)
            diffs.append(d)
        print 'diffs',diffs
        # Moving window iteration
        solution = None
        for i in xrange(len(d)-self.goal+1):
            rising = 0
            stable = 0
            for d in diffs:
                r = diff_match(d, i, self.goal)
                if r == 2: rising += 1
                if r == 1: stable += 1
                else: break
                if rising > 1 and stable > 1:
                    print 'not a possible solution'
                    break
            print 'index',i,rising,stable
            if rising == self.dims or rising == 1 and stable == (self.dims - 1):
                solution = i
                break
        
        if solution is not None:
            self.winner_idx = player_idx
            print 'The winner is:',player_idx
            end = solution + self.goal
            ret = []
            coords = []
            for m in matches:
                m = m[solution:end]
                ret.append(m)
            self.winning_cells = ret
            return ret
        return False
        
    def validate(self):
        """Finds adjacent occupied cells. 
        Returns False if we have no winner, otherwise return winner name and matched cells"""
        if self.moves < 4:
            return False
        print self.matrix
        for player_idx in range(1, self.players+1):
            r = self.validate_player(player_idx)
            if r is False: continue
            return player_idx, r
        return False
        
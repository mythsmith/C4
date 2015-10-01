#!/usr/bin/python 

"""Basic Connect4 logic"""
import numpy as np
from time import time 

# shape = (y,x)
# slice [y,x]

def diff_match(d, start, goal=4):
    """Check for rising/stable match"""
    sublen = goal - 1
    sub = d[ start:start + sublen]
    print 'diff_match',sub,sublen
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

def sort_matches(matches):
    """Iteratively sort matches"""
    ind = np.lexsort(matches)
    ret = []
    for m in matches:
        m = m[ind]
    return matches
        

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
        self.startdate = 0
        self.enddate = 0
        self.delta = 0
        self.zerotime = 0
        self.scores = {p:0 for p in range(1, players+1)}
        
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
        self.scores[self.player_idx]+= self.delta + time() - self.zerotime
        self.zerotime = time()
        self.player_idx += 1
        if self.player_idx > self.players:
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
            coords[0] = max(match)+1
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
        print 'validate_player',player_idx
        matches = np.where(self.matrix == player_idx)
        print 'unsorted',matches
        matches = sort_matches(matches)
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
        for i in xrange(len(d)-self.goal+2):
            rising = 0
            stable = 0
            for d in diffs:
                r = diff_match(d, i, self.goal)
                print 'diff_match',r
                if r == 2: rising += 1
                elif r == 1: stable += 1
                else: break
                print 'rising, stable', rising,stable
                if rising > 1 and stable > 1:
                    print 'not a possible solution'
                    break
            print 'index',i,rising,stable
            if rising == self.dims or rising == 1 and stable == (self.dims - 1):
                print 'found solution',i
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
            self.enddate = time()
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
        
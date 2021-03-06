import unittest
import numpy as np

from C4.GameMatrix import GameMatrix, diff_match, iter_matrix_translation


class TestGameMatrix(unittest.TestCase):
    def test_init(self):
        m = GameMatrix()
        self.assertEqual(m.shape, (6, 7))

    def test_moves(self):
        m = GameMatrix()
        self.assertEqual(m.moves, 0)
        m.matrix[1, 1] = 1
        self.assertEqual(m.moves, 1)
        m.matrix[2, 2] = 2
        self.assertEqual(m.moves, 2)
        m.matrix[3, 3] = 1
        self.assertEqual(m.moves, 3)
        
    def test_gravity(self):
        m = GameMatrix()
        self.assertEqual(m.gravity((0, 0)), (0, 0))
        self.assertEqual(m.gravity((1, 0)), (0, 0))
        self.assertEqual(m.gravity((1, 1)), (0, 1))
        
        m.matrix[0, 0] = 1
        self.assertEqual(m.gravity((3, 0)), (1, 0))
        
    def test_next_player(self):
        m = GameMatrix(players=3)
        self.assertEqual(m.player_idx,1)
        m.next_player()
        self.assertEqual(m.player_idx,2)
        m.next_player()
        self.assertEqual(m.player_idx,3)
        m.next_player()
        self.assertEqual(m.player_idx,1)
        
    def test_occupy(self):
        m = GameMatrix()
        r = m.occupy((0, 0), 1)
        self.assertEqual(r, (0, 0))
        self.assertEqual(m.matrix[0, 0], 1)
        # Already occupied cell
        r = m.occupy((0, 0), 1)
        self.assertFalse(r)
        
        # Test gravity
        r = m.occupy((3, 0), 1)
        # Should fall on the first free cell on x slot
        self.assertEqual(r, (1, 0))
        
        
    def test_iter_matrix_translation(self):
        m = np.zeros((6,7))
        r = iter_matrix_translation(m, [1,0])
        self.assertFalse(r)
        m[0,0] = 1
        m[1,0] = 1
        m[2,0] = 1
        r = iter_matrix_translation(m, [1,0])
        self.assertFalse(r)      
        m[3,0] = 1
        r = iter_matrix_translation(m, [1,0])
        self.assertEqual(r, [(0, 0), (1, 0), (2, 0), (3, 0)])      
        
    def test_diff_match(self):
        r = diff_match(np.array([0, 1, 0, 1, 2, 1, 0]), 0)
        self.assertEqual(r, 0)
        # Stable
        r = diff_match(np.array([0, 0, 0, 1, 2, 1, 0]), 0)
        self.assertEqual(r, 1)
        r = diff_match(np.array([1, 2, 1, 0, 0, 0]), 3)
        self.assertEqual(r, 1)
        
        # Rising
        # Short sequence
        r = diff_match(np.array([0, 0, 2, 1, 1, 0, 0]), 0)
        self.assertEqual(r, 0)
        
        r = diff_match(np.array([0, 1, 0, 1, 1, 1, 1]), 3)
        self.assertEqual(r, 2)  
        r = diff_match(np.array([1, 1, 1, 0, 1, 0]), 0)
        self.assertEqual(r, 2)           
        
        
        
        
    def test_validate_player(self):
        m = GameMatrix()
        # low moves
        self.assertFalse(m.validate_player(1))
        # low moves by player
        m.matrix[0, 0] = 1
        m.matrix[0, 1] = 1
        m.matrix[0, 2] = 1
        m.matrix[1, 2] = 2
        self.assertFalse(m.validate_player(1))
        # pattern not found
        m.matrix[1, 0] = 1
        self.assertFalse(m.validate_player(1))
        # Flat pattern
        m.matrix[0, 3] = 1
        cells = m.validate_player(1)
        self.assertNotEqual(cells, False)
        # Verify winning points
        self.assertEqual(cells, [(0, 0), (0, 1), (0, 2), (0, 3)])
        
        # From 1
        m.matrix[0, 0] = 2
        m.matrix[0, 4] = 1
        r = m.validate_player(1)
        self.assertNotEqual(r, False)
        self.assertEqual(r, [(0, 1), (0, 2), (0, 3), (0, 4)])
        
        # Different order
        m.matrix[0, 4] = 2
        m.matrix[1, 0] = 2
        m.matrix[1, 1] = 2
        m.matrix[1, 2] = 2
        m.matrix[1, 3] = 2
        r = m.validate_player(2)
        self.assertNotEqual(r, False) 

        # Rising in the middle
        m = GameMatrix()
        m.matrix[0, 1] = 2
        m.matrix[1, 2] = 2
        m.matrix[2, 3] = 2
        m.matrix[3, 4] = 2
        r = m.validate_player(2)
        self.assertNotEqual(r, False)
        self.assertEqual(r,[(0, 1), (1, 2), (2, 3), (3, 4)])     
    
    def test_validate_player_3d(self):
        m = GameMatrix(shape=(5,5,5))
        m.matrix[1,1,1] = 1
        self.assertFalse(m.validate_player(1))
        m.matrix[2,1,1] = 1
        m.matrix[3,1,1] = 1
        m.matrix[4,1,1] = 1
        r = m.validate_player(1)
        self.assertNotEqual(r, False) 
        self.assertEqual(r, [(1, 1, 1), (2, 1, 1), (3, 1, 1), (4, 1, 1)])
        
        
        
if __name__ == "__main__":
    unittest.main()

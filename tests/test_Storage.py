import unittest
import os
from C4.GameMatrix import GameMatrix
from C4.Storage import Storage
    
testdb = os.path.expanduser('~/c4test.sqlite')

class TestStorage(unittest.TestCase):
    def setUp(self):
        if os.path.exists(testdb):
            os.remove(testdb)
        self.s = Storage(testdb)
        self.assertTrue(os.path.exists(testdb))
        self.add_users()
        
    def add_users(self):
        umap = self.s.add_users(['pippo', 'franco'])
        self.assertEqual(umap['pippo'], 1)
        self.assertEqual(umap['franco'], 2)
        r = self.s.add_users(['pippo'])
        self.assertEqual(r['pippo'], 1)
        
    def test_save_game(self):
        g = GameMatrix()
        gid = self.s.save_game(g, {1:1, 2:2}, {'a':1, 'b':2})
        self.assertEqual(gid, 1)
        gid = self.s.save_game(g, {1:1, 2:2}, {'a':1, 'b':2})
        self.assertEqual(gid, 2)
        # Overwrite
        g.gid = 1
        gid = self.s.save_game(g, {1:1, 2:2}, {'a':1, 'b':2})
        self.assertEqual(gid, 1)
        
    def test_parse_game(self):
        g = GameMatrix()
        g.matrix[1, 1] = 2
        gid = self.s.save_game(g, {1:1, 2:2}, {'pippo':1, 'franco':2})
        g1, user_map, user_uid = self.s.search_gid(1)
        self.assertEqual(g1.matrix[1, 1], 2) 
        self.assertEqual(user_map, {1:1, 2:2})
        self.assertEqual(user_uid, {'pippo':1, 'franco':2})
        self.assertEqual(g1.gid, 1)
    
        

if __name__ == "__main__":
    unittest.main()

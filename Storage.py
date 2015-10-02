import sqlite3
import os
from cPickle import dumps, loads
import collections
import datetime 

from C4.GameMatrix import GameMatrix

users_def = '''(name text, victories integer, score real)'''
games_def = '''(status text, startdate date, enddate date,
    winner integer, score real, players_names text, goal integer, players integer, shape text, matrix text)'''
game_user_def = '''(gid integer, uid integer, pid integer, score real)'''



date_converter = lambda x: str(datetime.datetime.fromtimestamp(int(x)))

class Storage(object):
    def __init__(self, database=False):
        if not database:
            database = os.path.expanduser("~/.c4.sqlite")
        self.database = database
        self.create()
        
    def create(self):
        """Create initial database structure"""
        conn, cur = self.connect()
        cur.execute("create table if not exists users " + users_def)
        cur.execute("create table if not exists games " + games_def)
        cur.execute("create table if not exists game_user " + game_user_def)
        conn.commit()
        conn.close()      
        
    def reset(self):
        """Delete database file and recreate empty one"""
        if os.path.exists(self.database):
            print 'deleting',self.database
            os.remove(self.database)
        self.create()
        
    def connect(self):
        """Connects to db file returning connection and cursor"""
        conn = sqlite3.connect(self.database)
        cur = conn.cursor()
        return conn, cur
    
    def _query_user_by_name(self, name, cur):
        """Fetches user row by user name"""
        cur.execute('select ROWID,name,victories,score from users where name=?', (name,))
        r = cur.fetchone() 
        if r is None:
            return False
        return r
    
    def query_user_by_name(self, name):
        conn, cur = self.connect()
        return self._query_user_by_name(name, cur)
    
    def _query_user_by_uid(self,uid, cur):
        """Fetches user row by user uid"""
        cur.execute('select ROWID,name,victories,score from users where ROWID=?', (uid,))
        r = cur.fetchone()
        if r is None:
            return False
        return r
    
    def add_users(self, users):
        """Add users if need and returns a user_map {name:uid}"""
        conn, cur = self.connect()
        users_ids = {}
        for name in users:
            name = unicode(name)
            r = self._query_user_by_name(name, cur)
            if r is not False:
                print 'existing user', name, r
                users_ids[name] = r[0]
                continue
            cur.execute('insert into users values (?, ? ,?)', (name, 0, 0))
            r = cur.fetchall()
            print r
            users_ids[name] = cur.lastrowid
            print 'added user', name, cur.lastrowid
        conn.commit()
        conn.close()
        return users_ids

        
    def save_game(self, game, user_map, user_uid, gid=None):
        """Save `game` GameMatrix object with `user_map` dictionary correlating player_idx:uid"""
        conn, cur = self.connect()
        info = collections.OrderedDict()
        info['status'] = 'finished' if game.winner_idx else 'paused'
        info['startdate'] = date_converter(game.startdate)
        info['enddate'] = date_converter(game.enddate) if game.enddate else ''
        if game.winner_idx:
            info['winner'] = user_map[game.winner_idx]
            info['score'] = game.scores[game.winner_idx]
        else:
            info['winner'], info['score'] = 0, 0
        info['players_names'] = ', '.join(user_uid.keys())
        info['goal'] = game.goal
        info['players'] = game.players
        info['shape'] = dumps([int(d) for d in game.shape])
        info['matrix'] = dumps(game.matrix)
        
        if gid is None:
            # Build and execute the insert string
            v = info.values()
            cmd = '?,' * len(v)
            cmd = 'insert into games values (' + cmd[:-1] + ')'
            print cmd, v
            cur.execute(cmd, v)
            cur.fetchall()
            gid = cur.lastrowid
        else:
            # Build and execute the update string
            cmd = ''
            for p in info.iterkeys():
                cmd += p + ' = :' + p + ', '
            cmd = 'update games set ' + cmd[:-2]
            cur.execute(cmd, info)
            cur.fetchall()
        
        # Insert related game_user rows
        cur.execute('delete from game_user where gid=?', (gid,))
        cur.fetchall()
        cmd = 'insert into game_user values (?,?,?,?)'
        for player_idx, score in game.scores.iteritems():
            cur.execute(cmd, [gid, user_map[player_idx], player_idx, score])
        conn.commit()
        
        # Update the score
        for player_idx, uid in user_map.iteritems():
            if not game.scores.has_key(player_idx):
                continue
            cur.execute('select victories,score from users where ROWID=?', (uid,))
            victories, score = cur.fetchone()
            
            score += game.scores[player_idx]
            victories += player_idx == game.winner_idx
            cur.execute('update users set victories=?, score=? where ROWID=?', (victories, score, uid))
            cur.fetchall()
        
        conn.commit()
        conn.close()
        return gid
    
    def parse_game(self, row):
        """Restore a GameMatrix instance from a row"""
        startdate, enddate = row[1], row[2]
        goal = row[5]
        players = row[6]
        matrix = loads(str(row[-1]))
        shape = matrix.shape
        game = GameMatrix(shape=shape, players=players, goal=goal)
        game.matrix = matrix
        return game
        
    def search_gid(self, gid):
        """Search game by id and load it. 
        Returns GameMatrix and user mapping {player_idx:uid}"""
        conn, cur = self.connect()
        cmd = 'select * from games where ROWID=?'
        cur.execute(cmd, (gid,))
        row = cur.fetchone()
        if row is None:
            print 'No game found for id', gid
            return False
        
        user_map = {}
        user_uid = {}
        cur.execute('select * from game_user where gid=?', (gid,))
        r = cur.fetchall()
        for rel in r:
            gid, uid, pid, score = rel
            user_map[pid] = uid
            user = self._query_user_by_uid(uid, cur)
            user_uid[user[1]] = user[0]
        
        conn.close()
        game = self.parse_game(row)
        return game, user_map, user_uid
        

    
        

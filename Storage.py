import sqlite3
from os.path import expanduser
from cPickle import dumps, loads
import collections

from C4 import GameMatrix

usersColumn = ('name', 'score')
gamesColumn = ('status', 'startdate', 'enddate', 'winner', 'score', 'goal', 'players', 'shape', 'matrix')
game_userColumn = ('gid', 'uid', 'pid', 'score')


users_def = '''(name text, score real)'''
games_def = '''(status text, startdate date, enddate date,
    name text, score real, goal integer, shape text, matrix text)'''
game_user_def = '''(gid integer, uid integer, pid integer, score real)'''



date_converter = lambda x: str(datetime.datetime.fromtimestamp(int(x)))


usersColConverter = {}
for i, n in enumerate(usersColumn):
    usersColConverter[n] = colConverter[testColDef[i]]

gamesColConverter = {}
for i, n in enumerate(gamesColumn):
    gamesColConverter[n] = colConverter[testColDef[i]]
    
game_userColConverter = {}
for i, n in enumerate(game_userColumn):
    game_userColConverter[n] = colConverter[testColDef[i]]

class Storage(object):
    def __init__(self, database=False):
        if not database:
            database = expanduser("~/.c4.sqlite")
        self.database = database
        conn, cur = self.connect()
        cur.execute("create table if not exists users " + users_def)
        cur.execute("create table if not exists games " + games_def)
        cur.execute("create table if not exists game_user " + game_user_def)
        conn.commit()
        conn.close()
        
    def connect(self):
        conn = sqlite3.connect(self.database)
        cur = conn.cursor()
        return conn, cur
    
    def add_users(self, users):
        conn, cur = self.connect()
        users_ids = {}
        for name in users:
            cur.execute('select ROWID from users where name=?', v)
            r = cur.fetchone()
            if len(r):
                print 'existing user', name, r
                continue
            cur.execute('insert into users (? ,?)', (name, 0))
            r = cur.fetchone()
            user_ids[name] = cur.lastrowid
            
        return users_ids

        
    def save_game(self, game, user_map, gid=None):
        conn, cur = self.connect()
        info = collections.OrderedDict()
        info['status'] = 'finished' if game.winner_idx else 'paused'
        info['startdate'] = date_converter(game.startdate)
        info['enddate'] = date_converter(game.enddate)
        info['winner'] = user_map[game.winner_idx]
        info['score'] = game.score[game.winner_idx]
        info['goal'] = game.goal
        info['players'] = game.players
        info['shape'] = dumps(game.shape)
        info['matrix'] = dumps(game.matrix)
        
        if gid is None:
            # Build and execute the insert string
            v = info.values()
            cmd = '?,' * len(v)
            cmd = 'insert into games (' + cmd[:-1] + ')'
            cur.execute(cmd, v)
            cur.fetchall()
            gid = cur.lastrowid
        else:
            # Build and execute the update string
            cmd = ''
            for p in info.iterkeys():
                cmd += p + ' = :' + p + ', '
            cmd = 'update games set ' + cmd[:-1]
            cur.execute(cmd, info)
            cur.fetchall()
        
        # Insert related game_user rows
        cur.execute('delete from game_user where gid=?', (gid,))
        cur.fetchall()
        cmd = 'insert into game_user (?,?,?)'
        for player_idx, score in game.scores.iteritems():
            cur.execute(cmd, [gid, user_map[player_idx], player_idx, score])
        conn.commit()
        
        # Update the score
        for player_idx, uid in user_map.iteritems():
            if not game.scores.has_key(player_idx):
                continue
            cur.execute('select score from users where ROWID={}'.format(uid))
            score = cur.fetchone()[0]
            score += game.scores[player_idx]
            cur.execute('update users set score={} where ROWID={}'.format(score, uid))
            cur.fetchall()
        
        conn.commit()
        conn.close()
        return gid
        
    def search_gid(self, gid):
        conn, cur = self.connect()
        cmd = 'SELECT * from test WHERE ' + cnd + 'ORDER BY zerotime DESC'
        cur.execute(cmd, vals)
        r = self.cur.fetchone()
        
    def parse_game(self, row):
        """Restore a GameMatrix instance from a row"""
        startdate, enddate = row[1], row[2]
        goal = row[5]
        players = row[6]
        matrix = loads(row[-1])
        shape = matrix.shape
        game = GameMatrix(shape=shape, players=players, goal=goal)
        game.matrix = matrix
        

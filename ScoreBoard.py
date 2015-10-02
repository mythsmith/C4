from PyQt4 import QtCore, QtGui, QtSql
from time import time
from C4.BoardScene import BoardScene

    
class ScoreBoard(QtGui.QTableView):

    def __init__(self, database, parent=None):
        QtGui.QTableView.__init__(self, parent=parent)
        self.resize(200,500)
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.database = database
        db.setDatabaseName(database)
        db.open()
        model = QtSql.QSqlTableModel()
        model.setTable('users')
        model.select()
        self.setModel(model)
  
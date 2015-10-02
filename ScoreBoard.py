from PyQt4 import QtCore, QtGui, QtSql
    
class ScoreBoard(QtGui.QTableView):
    
    """Lists scores by all users"""

    def __init__(self, database, parent=None):
        QtGui.QTableView.__init__(self, parent=parent)
        self.resize(300,400)
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.database = database
        db.setDatabaseName(database)
        db.open()
        model = QtSql.QSqlTableModel()
        model.setTable('users')
        model.select()
        self.setModel(model)
  
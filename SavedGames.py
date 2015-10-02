from PyQt4 import QtCore, QtGui, QtSql
    
class SavedGames(QtGui.QTableView):
    resume_game = QtCore.pyqtSignal(int)
    
    def __init__(self, database, parent=None):
        QtGui.QTableView.__init__(self, parent=parent)
        self.resize(800,200)
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.database = database
        db.setDatabaseName(database)
        db.open()
        model = QtSql.QSqlTableModel()
        model.setTable('games')
        model.select()
        self.setModel(model)
        self.selection = QtGui.QItemSelectionModel(self.model())
        self.setSelectionModel(self.selection)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.doubleClicked.connect(self.open)
        
    def open(self, index):
        rowid = index.row()+1
        self.resume_game.emit(rowid)
        
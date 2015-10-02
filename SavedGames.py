from PyQt4 import QtCore, QtGui, QtSql
    
class SavedGames(QtGui.QTableView):
    
    """Explore saved games and select which one to load"""
    
    resume_game = QtCore.pyqtSignal(int)
    
    def __init__(self, database, parent=None):
        QtGui.QTableView.__init__(self, parent=parent)
        self.resize(600,200)
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.database = database
        db.setDatabaseName(database)
        db.open()
        model = QtSql.QSqlRelationalTableModel()
        model.setTable('games')
        relation = QtSql.QSqlRelation('users', 'ROWID', 'name')
        model.setRelation(3, relation)
        model.setHeaderData(3, QtCore.Qt.Horizontal, 'winner')
        model.setHeaderData(5, QtCore.Qt.Horizontal, 'players')
        model.select()
        self.setModel(model)
        for i in (6,7,8,9):
            self.hideColumn(i)
        self.selection = QtGui.QItemSelectionModel(self.model())
        self.setSelectionModel(self.selection)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.doubleClicked.connect(self.open)
        
    def open(self, index):
        rowid = index.row()+1
        self.resume_game.emit(rowid)
        
from bitfinexclient import BitfinexClient as BitfinexTradeClient
from bitfinexclient import BitfinexClient as BitfinexInfoClient
from datetime import time
from datetime import timedelta

'''Class where we will save 
all data that we need to 
demonstrate, also there we 
will read  and write data files
'''
"""TODO:  """

class Ohlc:
    def __init__(self, symbol, timeframe):
        self.symbol = symbol
        self.timeframe = timeframe
        pass

class SymbolOhlc:
    def __init__(self, symbol):

        self.data = {
            '1m' :  Ohlc(symbol, '1m') ,
            '5m' : Ohlc(symbol, '5m'),

        }
"""{'id': 138259326, 'symbol': 'ethbtc', 'status': 'ACTIVE', 'base': '0.04101', 'amount': '-0.1',
 'timestamp': '1535849072.0', 'swap': '0.0', 'pl': '-0.0000083022'}
"""
'''
tableList = {
    updateTime = [
        table,
        updateTime
                             ],
    positions = {'id' = 'int',
                 'symbol' = 'string',
                  'status' = 'string',
                    'base' = ,
                    'amount' = ,
                    'timestamp' = ,
                    'swap' = ,
                    'pl' = ,

                    }

}
'''

class Database(): #work with database
    DBFILE = 'data.db'
    def __init__(self):
        self.dbfile = DBFILE
        conn = sqlite3.connect(self.dbfile)
        self.cursor = conn.cursor()
        cursor = self.cursor
        self.tableList = ['positions', 'valuts', 'tikers', 'updatetime'] #TODO table list
        self.dbinit()

    def checkTable(self, tableName):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        if tableName in self.cursor.fetchall():
            return True
        else:
            return False

    def makeTable(self, table):
        tableName = table['tablename']
        rowsDict = table['rowsdict']
        command = 'CREATE TABLE {} ('.format(tableName)  #CREATE TABLE table_name (column1 datatype, column2 datatype)
        for key in rowsDict.keys():
            command = command + key + ' ' + rowsDict[key] + ', '
        command = command[:-1] + ')'
        self.cursor.execute(command)


    def dbinit(self, listOftables): # listoftables = [{tablename = , rowsdict = {rowname1 = , rowname2 =  } }, {tablename = ... }]
        for table in listOftables:
            if not self.checkTable(table['tablename']):
                self.makeTable(table)

    def loadTableToDict(self):
        pass



#Общий класс для каждой информации которая храниться в списке (маржин позиции, список тикеров,
class ListHolder:
    def __init__(self, db):
        self.db = db
        self.dataList = [] # The info (list of dictionary)
        self.lastUpdateTime = 0 # Last update time reloaded in child
        self.listType = '' #for Type Of Info in the object
        self._init() #for reload
        pass

    def _init(self): #Must be reloaded !!!!
        pass

    def downloadFromBitfinex(self): # need to reload!!!!!
        print('Function not reloaded !!')
        return('Function not reloaded !!')

    def update(self): # Download from bitfinex return true if updated and set TimeUpdated
        isUpdated = self.downloadFromBitfinex()
        if isUpdated:
            self.lastUpdateTime = time.now()
        return isUpdated

    def getList(self):
        return self.dataList

#класс для хранения маржин позиций

class ListMarginPositions(ListHolder):
    def _init(self):
        self.tableName = 'positions'
        self.dataList, self.lastUpdateTime = self.loadFromDatabase()

    def downloadFromBitfinex(self):
        bf = BitfinexTradeClient()
        self.dataList = bf.getListOfMarginPositions() #TODO mind about how to chek of internet conn
        self.lastUpdateTime = time.now()

    def loadFromDatabase(self, db):  #TODO load from database
        #self.dataList = db.
        pass


# class for all data that i needed in app    =============== Main class of info =======================
class DataHolder():
    def __init__(self):
        self.db = Database()
        self.positions = ListMarginPositions(self.db)
        db = self.db
        #table list

    def checkForReload(self): #if more then 10 seconds from last reload - download new data
        #list of margin positions
        deltaTime = time.now() - self.positions.lastUpdateTime
        if deltaTime > 1000 : #TODO deltatime
            self.positions.downloadFromBitfinex()

    def getPositionsList(self):
        return self.positions




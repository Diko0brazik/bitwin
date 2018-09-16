from bitfinexclient import BitfinexClient as BitfinexTradeClient
from bitfinexclient import BitfinexClient as BitfinexInfoClient
from datetime import time
from datetime import timedelta
import sqlite3

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
tableList = [ 
    
    
    positions =     {   
                    'tableName' = 'positions'
                    'rowsList' =  [   
                        'id',
                        'symbol',
                        'status',
                        'base',
                        'amount',
                        'timestamp',
                        'swap',
                        'pl',
                        'price']
                    }
                    ]
'''

class Database(): #work with database
    DBFILE = 'data.db'
    def __init__(self):
        tableDict = {'lastUpdate':
                        {   'tableName': 'string',
                            'lastUpdated' : 'int'
                        },
                     'positions':   {
                                 'id' : 'int',
                                 'symbol' : 'string',
                                 'status' : 'string',
                                 'base' : 'float',
                                 'amount' : 'float',
                                 'timestamp' : 'int',
                                 'swap' : 'float',
                                 'pl' : 'blob',
                                 'price' : 'float'
                                    }
                     }
        self.dbfile = self.DBFILE
        conn = sqlite3.connect(self.dbfile)
        self.cursor = conn.cursor()
        cursor = self.cursor
        #global tableList = ['positions', 'valuts', 'tikers', 'updatetime'] #TODO table list
        self.dbinit(tableDict)

    def checkTable(self, tableName):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        if tableName in self.cursor.fetchall():
            return True
        else:
            return False

    def _makeTable(self, tableName, rowsDict): # table = { tableName = , rowsList = [row1, row2, ... ] }
        sql = 'CREATE TABLE IF NOT EXISTS ' + tableName + ' ('
        for key in rowsDict.keys():
            sql = sql + key + ', '
        sql = sql[:-2] + ')'
        print(sql)
        self.cursor.execute(sql)

    def dbinit(self, listOftables):
        for tableName, rowsDict  in listOftables.items():
            self._makeTable(tableName, rowsDict)

    def loadTableToDict(self, tableName):
        sql = 'select * from ' + tableName
        self.cursor.execute(sql)

        pass



#Общий класс для каждой информации которая храниться в списке (маржин позиции, список тикеров,
class ListHolder:
    def __init__(self, db):
        self.db = db
        self.dataList = [] # The info (list of dictionary)
        self.lastUpdateTime = 0 # Last update time reloaded in child
        self.listType = '' #for Type Of Info in the object
        self._init() #for reload set TableName
        self.loadFromDatabase()
        pass

    def _init(self): #Must be reloaded !!!!
        pass

    def downloadFromBitfinex(self): # need to reload!!!!!
        print('Function not reloaded !!')
        return('Function not reloaded !!')

    def update(self): # Download from bitfinex return true if updated and set TimeUpdated
        isUpdated = self.downloadFromBitfinex()
        if isUpdated:
            self.lastUpdateTime = time.time()
        return isUpdated

    def getList(self):
        self.update()
        return self.dataList

    def loadFromDatabase(self):  #TODO load from database
        self.dataList, self.lastUpdateTime = self.db.loadTableToDict(self.tableName)
        pass

#класс для хранения маржин позиций

class ListMarginPositions(ListHolder):
    def _init(self):
        self.tableName = 'positions'

    def downloadFromBitfinex(self):
        bf = BitfinexTradeClient()
        self.dataList = bf.getListOfMarginPositions() #TODO return false if not updated
        #self.lastUpdateTime = time.time()
        return True




# class for all data that i needed in app    =============== Main class of info =======================
class DataHolder():
    def __init__(self):
        self.db = Database()
        self.marginPositions = ListMarginPositions(self.db)
        self.listForReload = [] #список чего надо обновлять для итерации


    def checkForReload(self): #if more then 10 seconds from last reload - download new data
        #list of margin positions
        deltaTime = time.now() - self.marginPositions.lastUpdateTime
        if deltaTime > 1000 : #TODO deltatime
            self.marginPositions.downloadFromBitfinex()

    def getPositionsList(self):
        self.marginPositions.getList()
        return self.marginPositions


d = DataHolder()


d.getPositionsList()

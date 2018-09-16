import csv
from  datetime import datetime
from  datetime import timezone
import time
import json
import requests


# CLASS OHLC - начало, конец, таймфрейм, массив с данными

# classes  open high low close volume 


class ohlc:
	'''d_ohlc = list()
	tiker     = ''
	timeframe = ''
	starttime = datetime(2018, 1, 1, 0, 0, 0, 0, timezone.utc)
	endtime   = datetime(2018, 6, 1, 0, 0, 0, 0, timezone.utc)
	'''
	def __init__(self, tiker, timeframe, starttime = datetime(2018, 1, 1, 0, 0, 0, 0, timezone.utc), endtime = datetime(2018, 6, 1, 0, 0, 0, 0, timezone.utc) , data=[]):
		self.tiker     = tiker
		self.timeframe = timeframe
		self.d_ohlc    = data
		self.starttime = starttime
		self.endtime   = endtime
		self.URL       = 'https://api.bitfinex.com/v2/candles/trade:{}:t{}/hist'.format(timeframe, tiker)
		self.lURL      = 'https://api.bitfinex.com/v2/candles/trade:{}:t{}/last'.format(timeframe, tiker)
		self.TFMS      = self._tfms(timeframe)
		self.TF        = timeframe
		
	def _tfms(self, timeframe): #return timeframe in ms
		tfs = {'1m':60000, '5m':300000, '15m':900000, '30m':1800000, '1h':3600000, '3h':10800000, '6h':21600000, '12h':43200000, '1D':86400000,
			'7D':604800000, '14D':1209600000  }
		return tfs[timeframe]

	def _toms(self, dt): #return dt in  int ms
		return dt.timestamp()*1000

	def _todt(self, ms):
		ms = int(ms)
		return datetime.fromtimestamp(ms/1000, timezone.utc) 

	def writetofile(self,  fname = None  ): #=  self.tiker + "_" + self.timeframe + '.csv'  ):
		if fname is None: 
			fname = self.tiker + "_" + self.timeframe + '.csv' 
		csv.register_dialect('dotcomm', delimiter=';')
		with open(fname, "w", newline="") as file:
			writer = csv.writer(file, dialect='dotcomm')
			#for d in data:
			#d = data
			#print(data)
			writer.writerows(self.d_ohlc)
		return(True)

	def readfromfile(self, fname = None):
		if fname is None: 
			fname = self.tiker + "_" + self.timeframe + '.csv'
		csv.register_dialect('dotcomm', delimiter=';')
		#print(fname)
		with open(fname, "r") as file:
			reader = csv.reader(file, dialect='dotcomm')
			data = []
			#while(True):
			#	print(reader.next())
			for row in reader:
				#print(row)
				data.append(row)
			#print(data[0])
			self.d_ohlc = data
		return(data)

	def getstarttime(self):
		return self._todt(self.d_ohlc[0][0])
	
	def getendtime(self):
		return self._todt(self.d_ohlc[-1][0])	

	def putdata(self, data):
		self.d_ohlc = data

	def _make_series_ohlc(self):
		self.time = list()
		self.open = list()
		self.high = list()
		self.low  = list()
		self.close = list()
		for i in range(len(self.d_ohlc)):
			self.time.append(self.d_ohlc[i][0])
			self.open.append( self.d_ohlc[i][1])
			self.high.append(self.d_ohlc[i][2])
			self.low.append( self.d_ohlc[i][3])
			self.close.append( self.d_ohlc[i][4])
		
#	def setstartendtimefromdata(self):


	def _download_diapazon(self, startms, endms): # simple download one diapazon
		data =  []
		print('download diapazon', " ", self._todt(startms), ' ', self._todt(endms))
		#for i in self.make_list_time_diapasons(start_time, end_time):
		params = {'limit': 1000, 'start': startms, 'end': endms, 'sort': 1}
		data = json.loads(requests.get(self.URL, params).text)
		#print('__', data)
		print(type(data[0]))
		while type(data[0]) is not list :
			print('sleep in download diapazon')
			time.sleep(65)
			data = json.loads(requests.get(self.URL, params))
			#r = requests.get(self.URL, params)
			#data = json.loads(r.text)
		#print(data)
		return data

	def _make_list_time_diapasons(self, start_dt, end_dt): #return list of lists start,end ms by 1000
		start_time 				= self._toms(start_dt)
		end_time 				= self._toms(end_dt)
		tf1000 					= self.TFMS * 1000
		data 					= list()
		download_diapazon 		= list()
		while (start_time + tf1000) < end_time :
			download_diapazon = [start_time, start_time + tf1000]
			data.append(download_diapazon)
			start_time = start_time + tf1000 + self.TFMS
		download_diapazon = [start_time, end_time]
		data.append(download_diapazon)
		return data 

	def _put_date_after():
		if len(d_ohlc[0] == 6):
			for d in d_ohlc:
				print(d)
				d.append(self._todt(d[0]))

	def getFloatData(self):
		data = self.d_ohlc
		for row in data:
			for i in range(len(row)):
				row[i] = float(row[i])
		return data

	def download(self, start_dt = None, end_dt = None):
		if start_dt is None :
			start_dt = self.starttime
		if end_dt is None :
			end_dt = self.endtime
		diapazon_list = self._make_list_time_diapasons(start_dt, end_dt)
		#print(diapazon_list)
		#d_ohlc = list()
		for diapazon in diapazon_list:
			self.d_ohlc.extend( self._download_diapazon(diapazon[0], diapazon[1]) )
			#print( self._download_diapazon(diapazon[0], diapazon[1]) )
		return self.d_ohlc


	def __call__(self):
		return self.d_ohlc



'''
#start = datetime(2018, 1, 1, 0, 0, 0, 0, timezone.utc)
#end   = datetime(2018, 7, 25, 0, 0, 0, 0, timezone.utc)
b = ohlc('BTCUSD', '1D', datetime(2018, 1, 1, 0, 0, 0, 0, timezone.utc), datetime(2018, 7, 25, 0, 0, 0, 0, timezone.utc))

#b.download()

b.readfromfile()


for row in b():
	print(row)
b._make_series_ohlc()
for row in b.open:
	print(row)

#b.writetofile()

#print(b.getstarttime(), b.getendtime()) '''
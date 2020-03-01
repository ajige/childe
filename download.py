# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import Series
from pandas import DataFrame
import tushare as ts
from scipy.stats.stats import pearsonr 
import pdb 
#date = pd.date_range('10/01/2012', end='26/01/2017')
#sz50 = ts.get_hs300s();
#sz50code = sz50['code']

sz50code = ['000300']
	# print "%d finish download" % y

'''
df = ts.profit_data()
filename = "C:\invest\\basic\divid.csv"
df.to_csv(filename)
print "%s finish" % filename
'''	
def LoadCodelist(filename=''):
	codelist = []
	#codelist = GetHs300().index
	#codelist = GetZz500().index
	#codelist = ['000423', '600519']
	#codelist=['600000', '600036', '600016', '601818', '601998']
	#codelist = ['000538', '000423','000963', '600887', '601166', '601668', '600886', '600048','000069', '600066']
	#codelist = ['601668', '600887', '601166', '000001','600886', '000963','000423', '000625', '600066', '600048', '000538']
	#codelist = ['601166', '000001', '600036']
	#codelist = ['000900']
	
	if len(filename) == 0:
		#codelist = ['000625', '000423', '000963', '600066', '600048', '600887', '600340', '000538', '601668', '000001',  '601166', '600886', '600016', '600104', '000883']
		#codelist = ['000423', '000963', '000538', '600887', '000895', '600048', '600340', '601668', '000001', '601166', '600016', '600886', '600066', '000625', '600104', '000883']
		codelist = GetHs300().index
		#codelist = GetIndex().index
	else:
		fp = open("/home/invest/script/code/" + filename, 'r')
		for line in fp:
			line = line.strip('\r\n')
			if len(line) < 5:
				continue
			tokens = line.split(':')
			if len(tokens) > 0:
				codelist.append(tokens[0])
	return codelist
	
	#codelist=['000625', '000423', '000963', '600066', '600048', '600887', '600340', '000538', '601668', '601166']
	#codelist=['600015', '601166', '000001', '600000', '600036', '600016', '601818','601998']
	#codelist = ['601668', '600887', '601166', '000001','600886', '000963','000423', '000625', '600066', '600048', '600016', '000538']
	#codelist = ['000423', '000963', '000538', '600887', '000895', '600048', '600340', '601668', '000001', '601166', '600016', '600886', '600066', '000625', '600104', '000883'] ## my holding
	#codelist = ['600340', '601668']
	#codelist = ['601166', '000001', '600036', '600016', '600000']
	#codelist = ['000423', '000963', '600519']
	#codelist = ['601668', '601186', '601800', '601669', '600068']
	#print codelist
	#for code in ['000625', '000333', '600887', '600340', '000538', '000423', '600066', '601668', '601166', '600115']:
	#codelist = ['000900']

def GetHs300():
	hs300 = pd.read_csv('/home/invest/basic/hs300.csv', index_col=0, encoding='utf-8', dtype={'code':np.str})
	hs300 = hs300.set_index('code')
	return hs300

def GetSz50():
	#hs300 = pd.read_csv('c:\\invest\\basic\\sz50.csv', index_col=0, encoding='utf-8', dtype={'code':np.str})
	hs300 = pd.read_csv('/home/invest/basic/szc50.csv', index_col=0, encoding='utf-8', dtype={'code':np.str})
	hs300 = hs300.set_index('code')
	return hs300
	
def GetZz500():
	hs300 = pd.read_csv('/home/invest/basic/zz500.csv', index_col=0, encoding='utf-8', dtype={'code':np.str})
	hs300 = hs300.set_index('code')
	return hs300

def GetIndex():
	hs300 = pd.read_csv('/home/invest/basic/index.csv', index_col=0, encoding='utf-8', dtype={'code':np.str})
	hs300 = hs300.set_index('code')
	return hs300
	
def loadpv(filename='', indexflag = False):
	start = True	
	print pd.datetime.today().date().strftime('%Y-%m-%d')
	codelist = LoadCodelist(filename)
	if indexflag:
		codelist = ['000300', '000016', '000001', '399106', '399005', '399006']
	#codelist = ['000963', '600276']
	for code in codelist:
		print "code: %s" % code
		#if code == '600109':
		#	start = True
		if start:
			if indexflag:
				filename = "/home/invest/pv/%sidx.csv" % code
			else:
				filename = "/home/invest/pv/%s.csv" % code
			print filename
			#df = ts.get_h_data(code, start="2010-01-01",  end = pd.datetime.today().date().strftime('%Y-%m-%d'))
			df = ts.get_k_data(code, start="2000-01-01",  end = pd.datetime.today().date().strftime('%Y-%m-%d'), index = indexflag)
			df.to_csv(filename)
			print "%s finish" % filename

## return most recent 4 year, quarter pair, not including the current quarter	
def getrecentquarter():
	year = pd.datetime.today().year
	month = pd.datetime.today().month
	currentquarter = (month - 1) / 3 + 1
	pair =[(year - 1, 1), (year - 1, 2), (year - 1, 3), (year - 1, 4), (year, 1), (year, 2), (year, 3), (year, 4)]
	
	return pair[currentquarter - 1 : currentquarter - 1 + 4]
	
	
def loadprofit():
	quarterlist = getrecentquarter()
	for q in quarterlist:
		try:
			profit = ts.get_profit_data(q[0], q[1])
			filename = "/home/invest/basic/profit/%s%s.csv" % (q[0], q[1])
			print filename
			profit.to_csv(filename, encoding='utf-8')
		except Exception as e:
			print e, "get_profit_data", q

def loadgrowth():
	quarterlist = getrecentquarter()
	for q in quarterlist:
		try:
			profit = ts.get_growth_data(q[0], q[1])
			filename = "/home/invest/basic/growth/%s%s.csv" % (q[0], q[1])
			print filename
			profit.to_csv(filename, encoding='utf-8')
		except Exception as e:
			print e, "get_profit_data", q

		 
def loadreport():
	quarterlist = getrecentquarter()
	for q in quarterlist:
		try:
			profit = ts.get_report_data(q[0], q[1])
			filename = "/home/invest/basic/report/%s%s.csv" % (q[0], q[1])
			print filename
			profit.to_csv(filename, encoding='utf-8')
		except Exception as e:
			print e, "get_profit_data", q


def loadindustry(industry):
	gg = ts.get_industry_classified()
	gg.to_csv('/home/invest/basic/industry.csv', encoding='utf-8')
		

if __name__ == "__main__":		 
	#loadpv('holdings.txt')
	#loadpv('constructioncode.txt')
	#loadpv('realeastatecode')
	#loadpv('bankcode')
	
	loadpv(indexflag = False)
	#loadreport()
	#loadprofit()
	#loadgrowth()
	#loadindustry()
	
#code = 'sh'
#filename = "C:\invest\\tsdata\%s.csv" % code
#df = ts.get_hist_data(code, start="2012-01-01",  end="2016-11-20")
#df.to_csv(filename)
#print "%s finish" % filename

#classify = ts.get_industry_classified()
#filename = "C:\invest\\basic\\classified.csv"
#classify.to_csv(filename, encoding='utf-8')
	'''
	#hs300 = ts.get_hs300s()
	#hs300 =ts.get_h_data('399106', start="2012-01-01",  end="2017-01-26", index=True)
	hs300 = ts.get_hs300s()
	filename = "C:\invest\\basic\\hs300.csv"
	hs300.to_csv(filename, encoding = 'utf-8')

	sz50 = ts.get_sz50s()
	filename = "C:\invest\\basic\\sz50.csv"
	sz50.to_csv(filename, encoding='utf-8')

	#basic = ts.get_stock_basics()
	#filename = "C:\invest\\basic\\basic.csv"
	#basic.to_csv(filename)

	zz500 = ts.get_zz500s()
	# print zz500.sort(['weight'], ascending= False)
	filename = "C:\invest\\basic\\zz500.csv"
	zz500.to_csv(filename, encoding='utf-8')
	'''



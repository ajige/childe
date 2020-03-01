# coding=utf-8
from __future__ import division
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import Series
from pandas import DataFrame
import tushare as ts
import datetime
import pdb
from scipy.stats.stats import pearsonr 

def GetWindowCorr(s1, s2, period):
	ss = Series(index=s1.index)
	ii = period
	#pdb.set_trace()
	while ii <= len(s1.index):
		s3 = s1[ii - period: ii] * s2[ii - period : ii]
		cov = s3.mean() - s1[ii - period: ii].mean() * s2[ii - period : ii].mean()
		ss [ii - 1] = cov / (s1[ii - period: ii].std(ddof = 0) * s2[ii - period: ii].std(ddof = 0))
		if ss[ii-1] > 1:
			pdb.set_trace()
		ii += 1
        
	return ss

def GetSz50():
	sz50 = pd.read_csv('/home/invest/basic/szc50.csv', index_col=0, encoding='utf-8', dtype={'code':np.str})
	sz50.append({'code':'sh','name':'index'}, ignore_index = True)
	#print sz50
	sz50 = sz50.set_index('code')
	#print sz50
	return sz50
	
def GetHs300():
	hs300 = pd.read_csv('/home/invest/basic/hs300.csv', index_col=0, encoding='utf-8', dtype={'code':np.str})
	#hs300 = pd.read_csv('c:\\invest\\basic\\zz500.csv', index_col=0, encoding='utf-8', dtype={'code':np.str})
	#hs300 = hs300.append({'code':'sh', 'name':'index','date': '2016-08-01','weight':0}, ignore_index=True)
	#print hs300
	hs300 = hs300.set_index('code')	
	#print hs300
	return hs300

def GetIndex():
	index = pd.read_csv('/home/invest/basic/index.csv', index_col=0, encoding='utf-8', dtype={'code':np.str})
	#hs300 = pd.read_csv('c:\\invest\\basic\\zz500.csv', index_col=0, encoding='utf-8', dtype={'code':np.str})
	#hs300 = hs300.append({'code':'sh', 'name':'index','date': '2016-08-01','weight':0}, ignore_index=True)
	#print hs300
	index = index.set_index('code')	
	#print hs300
	return index
	
def GetZz500():
	zz500 = pd.read_csv('/home/invest/basic/zz500.csv', index_col=0, encoding='utf-8', dtype={'code':np.str})
	#hs300 = hs300.append({'code':'sh', 'name':'index','date': '2016-08-01','weight':0}, ignore_index=True)
	#print hs300
	zz500 = zz500.set_index('code')
	
	#hs300 = pd.read_csv('c:\\invest\\basic\\hs300.csv', index_col=0, encoding='utf-8', dtype={'code':np.str})
	#hs300 = hs300.set_index('code')
	#pdb.set_trace()
	#print zz500
	return zz500
	
## price['6000168'][20151201] = 10
## volume['600168'][20151201] = 10
## price['600168']['name'] = '中国建筑'	
def GetPriceVolume(code='', indexflag = False):	
	#date = pd.date_range('01/01/2011', end = pd.datetime.today())
	#date = pd.date_range('01/05/2016', end = pd.datetime.today())
	sz50 = GetHs300()
	sz50code = sz50.index
	df = DataFrame(columns=sz50.index)
	rawdict = {}
	nameseries = Series()
	
	if indexflag:
		index = GetIndex()
		for idx in range(0, index.index.size):
			code = index.index[idx]
			#pdb.set_trace()
			if isinstance(index['name'][code], Series):
				name = index['name'][code][0].decode('UTF-8')
			else: 
				name = index['name'][code].decode('UTF-8')
			
			filename = '/home/invest/pv/%sidx.csv' % (code)
			second = pd.read_csv(filename, encoding="gbk", index_col=1, parse_dates=True) ## previously index_col = 0
			rawdict[code] = second
			nameseries[code] = name
			
	else:
		if code=='':
			for idx in range(0, sz50.index.size):
				code = sz50.index[idx]
				#pdb.set_trace()
				if isinstance(sz50['name'][code], Series):
					name = sz50['name'][code][0].decode('UTF-8')
				else: 
					name = sz50['name'][code].decode('UTF-8')
				#name = sz50.ix[idx]['name']
				#print code, name
				if indexflag:
					filename = '/home/invest/pv/%sidx.csv' % (code)
				else:
					filename = '/home/invest/pv/%s.csv' % (code)
				second = pd.read_csv(filename, encoding="gbk", index_col=1, parse_dates=True) ## previously index_col = 0
				rawdict[code] = second
				nameseries[code] = name
				#print "code: %s, name %s finish loading" % (code, nameseries[code])
		else:
			if code in sz50['name']:
				name = sz50['name'][code].decode('UTF-8')
			else:
				name = code
			filename = '/home/invest/pv/%s.csv' % (code)		
			second = pd.read_csv(filename, encoding="gbk", index_col=1, parse_dates=True)
			rawdict[code] = second
			nameseries[code] = name
			#print "code: %s, name %s finish loading" % (code, nameseries[code])
	
	price = DataFrame({tick: data['close'] for tick, data in rawdict.iteritems()})
	##backfill
	price.fillna(method = 'ffill', inplace=True)
	
	#price.ix['name'] = namedf  ## add the name in end
	volume = DataFrame({tick: data['volume'] for tick, data in rawdict.iteritems()})
	volume.fillna(method = 'ffill', inplace=True)
	##backfill
	
	#volume.ix['name'] = namedf  ## add the name in end
	#final = DataFrame(columns= sz50code, index=sz50code)
	# print sz50code
	# print nameseries
	# print price
	# print volume 
	return sz50code, nameseries, price, volume
		
# code,代码
# name,名称
# industry,所属行业
# area,地区
# pe,市盈率
# outstanding,流通股本(亿)
# totals,总股本(亿)
# totalAssets,总资产(万)
# liquidAssets,流动资产
# fixedAssets,固定资产
# reserved,公积金
# reservedPerShare,每股公积金
# eps,每股收益
# bvps,每股净资
# pb,市净率
# timeToMarket,上市日期
# undp,未分利润
# perundp, 每股未分配
# rev,收入同比(%)
# profit,利润同比(%)
# gpr,毛利率(%)
# npr,净利润率(%)
# holders,股东人数

def GetBasic():
	sz50 = GetHs300()
	#basic = ts.get_stock_basics()
	filename="/home/invest/basic/basic.csv"
	basic = pd.read_csv(filename, encoding='utf-8', dtype={'code':np.str}, parse_dates=True)
	#print basic
	basic = basic.set_index('code')
	#extracted = DataFrame(columns = basic.columns)
	#for code in sz50['code']:
	#	extracted.ix[code] = basic.ix[code]
	
	return basic


## return quarterlist
def getquarterlist():
	currentyear = pd.datetime.today().year
	currentmonth = pd.datetime.today().month
	currentquarter = int((currentmonth - 1) / 3) + 1

	zzidx = []
	
	for year in range(2011, currentyear + 1):
		for quarter in range(1,5):
			if year == currentyear and quarter == currentquarter:
				break;
			#print currentyear, currentquarter, year, quarter
			zzidx.append((year, quarter))

	return zzidx
	
# code,代码
# name,名称
# eps,每股收益
# eps_yoy,每股收益同比(%)
# bvps,每股净资产
# roe,净资产收益率(%)
# epcf,每股现金流量(元). blank
# net_profits,净利润(万元)
# profits_yoy,净利润同比(%)，not reliable as investigated, some value are negative. I can calc it myself.
# distrib,分配方案
# report_date,发布日期
def GetReport(indicator):
	sz50 = GetHs300()
	zzidx = []

	zzidx = getquarterlist()
	#print zzidx
	
	profit = DataFrame(index = sz50.index, columns = [zz[0] * 10 + zz[1] for zz in zzidx])
	for (year,quarter) in zzidx:
		try:
			filename = '/home/invest/basic/report/%d%d.csv' % (year, quarter)
			df = pd.read_csv(filename, encoding='utf-8', index_col=0, dtype={'code':np.str})
			df = df.drop_duplicates(subset='code')
			df = df.set_index('code')
			#print df
			#print sz50.index
			#print df.index
			for code in profit.index:
				if code in df.index:
					profit[year*10 + quarter][code] = df[indicator][code]
		except Exception as exp:
			print exp, filename
					
	return profit	

##need modify for this one
#        code   name      roe  net_profit_ratio  gross_profit_rate       net_profits   eps  business_income     bips 
# code,代码
# name,名称
# roe,净资产收益率(%)
# net_profit_ratio,净利率(%)
# gross_profit_rate,毛利率(%)
# net_profits,净利润(万元)
# eps,每股收益
# business_income,营业收入(百万元)
# bips,每股主营业务收入(元)
def GetProfit(indicator):
	sz50 = GetHs300()
	zzidx = []

	zzidx = getquarterlist()
	
	profit = DataFrame(index = sz50.index, columns = [zz[0] * 10 + zz[1] for zz in zzidx])
	for (year,quarter) in zzidx:
		try:
			filename='/home/invest/basic/profit/%d%d.csv' % (year, quarter)
			df = pd.read_csv(filename, encoding='utf-8', index_col=0, dtype={'code':np.str})
			#print df
			df = df.set_index('code')
			df = df.drop_duplicates()
			#print df.ix['600837']
			#print sz50.index
			#print df.index
			for code in profit.index:
				if code in df.index:
					profit[year*10 + quarter][code] = df[indicator][code]
		except Exception as exp:
			print exp, filename
			
	return profit

# code,代码
# name,名称
# mbrg,主营业务收入增长率(%)
# nprg,净利润增长率(%)
# nav,净资产增长率
# targ,总资产增长率
# epsg,每股收益增长率
# seg,股东权益增长率
def GetGrowth(indicator):
	sz50 = GetHs300()
	zzidx = []
	zzidx = getquarterlist()
	profit = DataFrame(index = sz50.index, columns = [zz[0] * 10 + zz[1] for zz in zzidx])
	
	for (year,quarter) in zzidx:
		try:
			filename='/home/invest/basic/growth/%d%d.csv' % (year, quarter)
			df = pd.read_csv(filename, encoding='utf-8', index_col=0, dtype={'code':np.str})
			df = df.set_index('code')
			df = df.drop_duplicates()
			#print df.ix['600837']
			#print sz50.index
			#print df.index
			for code in profit.index:
				if code in df.index:
					profit[year*10 + quarter][code] = df[indicator][code]
		except Exception as exp:
			print exp, filename
	return profit

#code:股票代码
#name:股票名称
#year:分配年份
#report_date:公布日期
#divi:分红金额（每10股）
#shares:转增和送股数（每10股）	
def GetDiv(indicator):
	sz50 = GetHs300()
	zzidx = [2010,2011,2012,2013,2014,2015,2016,2017,2018,2019]
	
	ret = DataFrame(index = sz50.index, columns = zzidx)
	for year in zzidx:
		filename='c:\\invest\\basic\\div\\%d.csv' % (year)
		df = pd.read_csv(filename, encoding='utf-8', index_col=0, dtype={'code':np.str})
		df = df.drop_duplicates(subset='code', keep='first')
		df = df.set_index('code')
		
		for code in ret.index:
			if code in df.index:
				ret[year][code] = df[indicator][code]
				
	return ret

def GetIndustry(industry, subindustry=''):
	filename = 'c:\\invest\\basic\\industry.csv' 
	df = pd.read_csv(filename, encoding='utf-8', index_col=0, dtype={'code':np.str})
	df = df.drop_duplicates(subset='code', keep='first')	
	df = df.set_index('c_name')
	#print df.ix[industry]

	ret = []
	for idx, row in df.iterrows():
		if idx == industry:
			if len(subindustry) > 0: 
				if row['name'].find(subindustry) != -1:
					#print "%s:%s" %( row['code'],row['name'])
					ret.append((row['name'], row['code']))
			else:
				ret.append((row['name'], row['code']))
	print ret
	return ret

	
#filter function, do filter
def Filter(report, level):
	for code in report.index:
		flag = True
		for period in report.columns:
			# # #print profit[period][code]
			 if report[period][code] < level:
				 flag = False
		if flag == True:
			print code, sz50['name'][code]



def top(df, n=5, column1='pe', column2='pb'):
	abovezero = df[df[column1] > 0]
	abovezero = abovezero[abovezero[column2] > 0 ]
	#abovezero = abovezero.rank()
	#abovezero['area'] = abovezero['pb'] - abovezero['pe']
	abovezero['cc'] = abovezero['pb'] * abovezero['pe']
	return abovezero.sort_index(by='cc')[:n]
	
	
if __name__ == "__main__":
	GetIndustry(u'建筑建材')
	sz50 = GetHs300()
	profit = GetProfit('roe')  ## 净资产收益率
	#profit.to_csv("c:\\invest\\temp.txt")
	#print profit
	ret1 = set()
	for code in profit.index:
		flag = True
		for period in [20144,20154,20164,20174]:
			#pdb.set_trace()
			#print profit[period][code]
			if profit[period][code] < 9:
				flag = False
		if flag == True:
			print code, sz50['name'][code]
			ret1.add(code)
	print '-------roe > 9 percent----- %d'% len(ret1)
	
	growth = GetGrowth('nprg') ## 净利润增长率
	#profit.to_csv("c:\\invest\\temp.txt")
	#print profit
	sz50 = GetHs300()
	ret2 = set()
	for code in growth.index:
		flag = True
		for period in [20144, 20154,20164,20174]:
			#print profit[period][code]
			if growth[period][code] < 5:
				flag = False
		if flag == True:
			print code, sz50['name'][code]
			ret2.add(code)
	print '----nprg > 5 percent---------%d'%len(ret2)
	
	'''
	cashflow = GetReport('epcf')## 每股现金流
	ret3 = set()
	for code in cashflow.index:
		flag = True
		for period in [20144,20154,20163]:
			if cashflow[20163][code] < 0:
				flag = False
		if flag == True:
			print code, sz50['name'][code]
			ret3.add(code)
	print '---------epcf > 0 -------- %d' % len(ret3)
	'''
	
	retz = ret1&ret2			
	sz50code, namedf, price, volume = GetPriceVolume()
	dt = datetime.datetime(2018,01,12)
	eps = GetProfit('eps')
	bvps = GetBasic()
	for code in retz:
		#if code not in ['000625', '000423', '000963', '600066', '600048', '600887', '600340', '000538', '601668', '000001',  '601166', '600886', '600016', '600104']:
		print code, sz50['name'][code], price[code][dt]/eps[20173][code], price[code][dt]/bvps['bvps'][code], profit[20173][code], profit[20164][code], profit[20154][code], profit[20144][code], growth[20173][code], growth[20164][code], growth[20154][code], growth[20144][code]
	print '---------------------'
	
	
	odt = datetime.datetime(2014,01,13)
	for code in retz:
		print code, sz50['name'][code], price[code][dt] / price[code][odt]
	
	'''
	for code in retz:
		print code, sz50['name'][code], price[code][dt]/(4*(eps[20163][code]/3)), price[code][dt]/bvps['bvps'][code], profit[20163][code], profit[20154][code], profit[20144][code], growth[20163][code], growth[20154][code], growth[20144][code]
	print '--------------------------'
	
	for code in retz:
		if profit[20144][code] < profit[20154][code] and profit[20154][code] < profit[20163][code]/3*4:
			print code, sz50['name'][code], price[code][dt]/(4*(eps[20163][code]/3)), price[code][dt]/bvps['bvps'][code], profit[20144][code], profit[20154][code], profit[20163][code], growth[20144][code], growth[20154][code], growth[20163][code]
	
	print '---------------------'
	# for code in retz:
		# if growth[20144][code] < growth[20154][code] and growth[20154][code] < growth[20163][code]/3*4:
			# print code, sz50['name'][code], price[code][dt]/(4*(eps[20163][code]/3)), price[code][dt]/bvps['bvps'][code], profit[20144][code], profit[20154][code], profit[20163][code], growth[20144][code], growth[20154][code], growth[20163][code]	
		
	print '---------------------'	
	'''
	
	
	
def GetClose():
	global date,second
	ret = Series(index = date)
	prev = 0
	firstunzero = 0
	#print ret.index
	#print second.index
	
	#for d in ret.index:
	#	print d
	#for d in second.index:
	#	print d
		
	for d in ret.index:
		if d in second.index:
			#print second['close'][d]
			ret[d] = second['close'][d]
			#print d, ret[d]
			prev = ret[d]
			if firstunzero == 0:
				firstunzero = prev
		else:
			ret[d] = prev
	
	for d in date:
		if ret[d] == 0:
			ret[d] = firstunzero
	return ret
	
	
	# sz50code, namedf, price, volume = GetPriceVolume()
	# pricecorr = price.corr()
	# volumecorr = (price*volume).corr()
	
	# #for code in sz50code:
	# code = '600066'
	# print "for code %s, ticker: %s" % (code, namedf[code])
	# tempcorr = pricecorr[code]
	# tempcorr = tempcorr.sort(inplace=False)
	# smallest = tempcorr[:8]
	# largest = tempcorr[-8:]
	
	# for cd in smallest.index:
		# print cd, namedf[cd], smallest[cd]
		
	# for cd in largest.index:
		# print cd, namedf[cd], largest[cd]
	
	# print "\n"
	# tempcorr = volumecorr[code]
	# tempcorr = tempcorr.sort(inplace=False)
	# smallest = tempcorr[:8]
	# largest = tempcorr[-8:]
	
	# for cd in smallest.index:
		# print cd, namedf[cd], smallest[cd]
		
	# for cd in largest.index:
		# print cd, namedf[cd], largest[cd]
	
	
	# ret = basic.groupby('industry').apply(top, column1 ='pe', column2='pb')
	# print ret
	# ret[['name','pb', 'pe', 'cc']].to_csv("c:\\invest\\temp.txt")
	
	# dt = datetime.datetime(2016,11,18)
	# sz50code, namedf, price, volume = GetPriceVolume()
	#profit = GetProfit('eps')
	# epcf = GetReport('profits_yoy')[20163]
	# print epcf
		
	# final = epcf / price.ix[20161120]
	# print final
	
	# print report
			 
	# print profit
	#print report
	#compare
	# for idx in profit.index:
		# for col in profit.columns:
			# if report[col][idx] != profit[col][idx]:
				# print "col:%s, idx:%s, report[col][idx]:%s, profit[col][idx]:%s" %(col, idx, report[col][idx], profit[col][idx])
			# else:
				# print "same: col:%s, idx:%s, report[col][idx]:%s, profit[col][idx]:%s" %(col, idx, report[col][idx], profit[col][idx])
	
	# profit = GetGrowth('nprg')
	# profit.to_csv("c:\\invest\\temp.txt")
	# # #print profit
	
	# for code in profit.index:
		# flag = True
		# for period in profit.columns:
			# # #print profit[period][code]
			 # if profit[period][code] < 10:
				 # flag = False
		# if flag == True:
			 # print code, sz50['name'][code]


	# for code1 in s050code:
		# max = 0
		# maxcode=code1
		# min = 0
		# mincode = code1
		# print "code: %s, name: %s" % (code1, namedf[code1])
		# for code2 in sz50code:
			# if code2 == code1:
				# continue
			# if final[code1][code2] > max:
				# max = final[code1][code2]
				# maxcode = code2		
			# elif final[code1][code2] < min:
				# min = final[code1][code2]
				# mincode = code2		
			
		# print "max positive similarity: maxcode %s, maxname: %s, similarity: %f" % (maxcode, namedf[maxcode], max)
		# print "max negative similarity: mincode %s, minname: %s, similarity: %f" % (mincode, namedf[mincode], min)
	

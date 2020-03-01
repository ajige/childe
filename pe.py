# coding=utf-8
##plot the price, earning picture

import matplotlib
# chose a non-GUI backend
matplotlib.use( 'Agg' )

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from pandas import Series
from pandas import DataFrame
import tushare as ts
import datetime
import getdata
import download

import pdb
#pdb.set_trace()
genddate = pd.datetime.today().date().strftime('%Y-%m-%d')
#genddate = '2017-12-31'
startdate = '01/01/2014'

font2 = {'family' : 'Times New Roman',
'weight' : 'normal',
'size'   : 25,
}


def getlastquarter(date):
	year = date.year
	month = date.month
	currentquarter = int((month - 1) / 3) + 1
	pair =[(year-1, 3), (year - 1, 4), (year, 1), (year, 2), (year, 3)]
	
	return pair[currentquarter]

def getsecondlastquarter(date):
	year = date.year
	month = date.month
	currentquarter = int((month - 1) / 3) + 1
	pair =[(year-1, 3), (year - 1, 4), (year, 1), (year, 2), (year, 3)]
	
	return pair[currentquarter - 1]


sz50code, namedf, price, volume = getdata.GetPriceVolume()
daterange = pd.date_range(startdate, end = genddate, freq='B')
convertrange = daterange.to_pydatetime()
price = price.ix[convertrange[0]:convertrange[-1]]

def getvalue(tsseries, date):
	quarter = int((date.month - 1) / 3) + 1
	lastq = getlastquarter(date)
	
	if date.year == 2011:
		earning = tsseries[20114]
		
	## data for most recent days, first check wheter value of last quarter is valid, if yes, use last quarter;
	## if not, use second last quarter			
	elif date > convertrange[-180]:
		if not np.isnan(tsseries[lastq[0] * 10 + lastq[1]]):
			if lastq[1] == 4:
				earning = tsseries[lastq[0]* 10 + 4]
			else:
				earning = tsseries[lastq[0] * 10 + lastq[1]] + tsseries[(lastq[0] - 1) * 10 + 4] - tsseries[(lastq[0] - 1) * 10 + lastq[1]]
		else:
			lastq = getsecondlastquarter(date)
			if lastq[1] == 4:
				earning = tsseries[lastq[0]* 10 + 4]
			else:
				earning = tsseries[lastq[0] * 10 + lastq[1]] + tsseries[(lastq[0] - 1) * 10 + 4] - tsseries[(lastq[0] - 1) * 10 + lastq[1]]
				
	else:	
		if lastq[1] == 4:
			earning = tsseries[lastq[0]* 10 + 4]
		else:
			earning = tsseries[lastq[0] * 10 + lastq[1]] + tsseries[(lastq[0] - 1) * 10 + 4] - tsseries[(lastq[0] - 1) * 10 + lastq[1]]
			
	return earning
	

def plotpe(code, ax, name):
	global profit, hs300, basic, retpearray
	#sz50code, namedf, price, volume = getdata.GetPriceVolume(code)
	print "PE: %s: %s" % (code, name)
	
	netprofit = profit.ix[code]/basic[code]/100
	
	#pdb.set_trace()
	#print netprofit	
	#print price
	
	peseries = Series()
	earningseries = Series()
	#mostrecentquarter = getmostrecentquarter()
	prevvalid = np.nan
	
	for date in convertrange:
		earning = getvalue(netprofit, date)

		if date in price.index:
			prevvalid = price[code][date]
			validprice = prevvalid
		else:##backfill logic
			validprice = prevvalid
			
		temp = validprice / earning
		#print date, validprice, "%.2f" % earning
		peseries[date] = temp
		earningseries[date] = earning
	
	#print peseries.min(), peseries.max(), peseries.mean(), peseries.median()	
	#normalizedpe = (peseries - peseries.min()) / (peseries.max() - peseries.min())
	normalizedpe = peseries
	#print normalizedpe
	
	xlabel = "\nPE=%.2f, PE_Mean_3Y=%.2f(%.2f), PE_Mean_5Y=%.2f(%.2f)" % (normalizedpe.ix[-1], normalizedpe.values[-250*3:].mean(), normalizedpe.ix[-1] / normalizedpe.values[-250*3:].mean(), normalizedpe.values[-250*5:].mean(), normalizedpe.ix[-1] / normalizedpe.values[-250*5:].mean() )	
	print xlabel
	sortedpe = normalizedpe.sort_values()
	print code, normalizedpe.ix[-1] / sortedpe[sortedpe.index[0]], sortedpe.index[0], sortedpe[sortedpe.index[0]], sortedpe.index[-1], sortedpe[sortedpe.index[-1]]
		
	#retpearray[code] = normalizedpe.ix[-1] / sortedpe[sortedpe.index[0]]
	
	#ax = plt.axes()
	
	ax.set_xlabel(xlabel, font2)
	ax.grid()
	ax.set_title(code + ' PE ' + genddate )
	#np.log(price).plot(ax = ax, kind = 'hist')
	normalizedpe.plot(ax = ax, label = "PE")
	del normalizedpe, peseries, earningseries
	#normalizedpe.plot(ax = ax, kind = 'hist', label = "PE")
	print '------------------------------------------'


def plotpb(code, ax, name):
	global profit, hs300, basic, roe, retpbarray, growth_nav
	#sz50code, namedf, price, volume = getdata.GetPriceVolume(code)
	print "PB: %s: %s" % (code, name)
	

	netprofit = profit.ix[code]/basic[code]/100
	roeix = roe.ix[code]   ## roe 是全面摊薄净资产收益率， 不知怎么计算的
	#print roeix
	#growth_nav = growth_nav.ix[code]
	
	#print netprofit
	#print roeix
	#print growth_nav
	#price = price.ix[convertrange[-1]:convertrange[0]]
	
	pbseries = Series()
	earningseries = Series()
	prevvalid = np.nan
	
	for date in convertrange:
		earning = getvalue(netprofit, date)
		temproe = getvalue(roeix, date)

		if date in price.index:
			prevvalid = price[code][date]
			validprice = prevvalid
		else:##backfill logic
			validprice = prevvalid
			
		book = earning*100 / temproe
		
		temp = validprice / book
		#print code, date, price[code][date]
		pbseries[date] = temp
		#print date, earning, temproe, book, price[code][date], temp
		earningseries[date] = earning
			
	normalizedpe = pbseries
	
	
	xlabel = "\n%s, PB=%.2f, PB_Mean_3Y=%.2f(%.2f), PB_Mean_5Y=%.2f(%.2f)" % (code, normalizedpe.ix[-1], normalizedpe.values[-250*3:].mean(),  normalizedpe.ix[-1] / normalizedpe.values[-250*3:].mean(), normalizedpe.values[-250*5:].mean(), normalizedpe.ix[-1] / normalizedpe.values[-250*5:].mean() )	
	print xlabel
	
	sortedpe = normalizedpe.sort_values()
	print code, normalizedpe.ix[-1] /sortedpe[sortedpe.index[0]],  sortedpe.index[0], sortedpe[sortedpe.index[0]], sortedpe.index[-1], sortedpe[sortedpe.index[-1]]
	
	#retpbarray[code] = normalizedpe.ix[-1] / sortedpe[sortedpe.index[0]]
	ax.set_title(code + ' PB ' + genddate)
	ax.set_xlabel(xlabel, font2)
	ax.grid()
	normalizedpe.plot(ax = ax, label = "PB")
	
	#normalizedpe = (peseries - peseries.min()) / (peseries.max() - peseries.min()) 
	#normalizedearning = (earningseries - earningseries.min()) / (earningseries.max() - earningseries.min())
	
	#ax.set_yticks(np.arange(0.,1.3,0.1))
	#normalizedprice.plot(ax = ax,  label="Price")
	del normalizedpe, pbseries, earningseries
	print '------------------------------------------'	
	

def plotprice(code, ax, name):
	global profit, hs300, basic, retpearray
	#sz50code, namedf, price, volume = getdata.GetPriceVolume(code)
	print "Price %s: %s" % (code, name)
		
	#print price
	
	priceseries = Series()
	prevvalid = np.nan
	for date in convertrange:
		if date in price.index:
			prevvalid = price[code][date]
			validprice = prevvalid
		else:##backfill logic
			validprice = prevvalid
			
		temp = validprice
		#print date, validprice, "%.2f" % earning
		priceseries[date] = temp
	
	#print peseries.min(), peseries.max(), peseries.mean(), peseries.median()	
	#normalizedpe = (peseries - peseries.min()) / (peseries.max() - peseries.min())
	normalizedpe = priceseries
	#print normalizedpe
	
	xlabel = "\nPrice=%.2f, Price_20D=%.2f(%0.2f), Price_60D=%.2f(%.2f), \n Price_120D=%.2f(%.2f), Price_250D=%.2f(%.2f),\n " % (
	 normalizedpe.ix[-1], normalizedpe.values[-21:].mean(), normalizedpe.ix[-1]/normalizedpe.values[-21:].mean(),
      			   normalizedpe.values[-63:].mean(), normalizedpe.ix[-1]/normalizedpe.values[-63:].mean(),
                           normalizedpe.values[-125:].mean(), normalizedpe.ix[-1]/normalizedpe.values[-125:].mean(),
                           normalizedpe.values[-250:].mean(), normalizedpe.ix[-1]/normalizedpe.values[-250:].mean(),
  )	
	sortedpe = normalizedpe.sort_values()
	print code, normalizedpe.ix[-1] / sortedpe[sortedpe.index[0]], sortedpe.index[0], sortedpe[sortedpe.index[0]], sortedpe.index[-1], sortedpe[sortedpe.index[-1]]
		
	#retpearray[code] = normalizedpe.ix[-1] / sortedpe[sortedpe.index[0]]
	ax.grid()
	ax.set_xlabel(xlabel, font2)
	ax.set_title(code + ' Price')
	#np.log(price).plot(ax = ax, kind = 'hist')
	normalizedpe.plot(ax = ax, label = "PRice")
	del normalizedpe, priceseries
	#normalizedpe.plot(ax = ax, kind = 'hist', label = "PE")
	print '------------------------------------------'


def plotgrowth(code, ax):
	global profit, hs300, roe, growth_mbrg, growth_nprg
	print hs300['name'][code].decode('UTF-8')
	print growth_mbrg.ix[code]
	#print growth_nprg.ix[code]
	#ax.plot(growth_mbrg.ix[code], color='b', marker='o')
	#ax.plot(growth_nprg.ix[code], color='r', marker='o')
	#ax.set_title(code + ' growth')
	#print '------------------------------------------'	
 
def plotcorrelation():
	code1 = '601668'
	sz50code1, namedf1, price1, volume1 = getdata.GetPriceVolume()
	price1 = price1['601668'].pct_change()[1:]
	#price1 = price1.apply(lambda x: (x - np.mean(x)) / (np.max(x) - np.min(x)))
	volume1 = volume1.apply(lambda x: (x - np.mean(x)) / (np.max(x) - np.min(x)))
	volume_ma = pd.rolling_mean(volume1, window = 30)
	#price_ma = pd.rolling_mean(price1, window = 30)
	#ss = getdata.GetWindowCorr(price_ma[code1], volume_ma[code1], 90)
	#price_ma[code1].plot(color='r')
	price1.plot(label = "PE")
	#volume_ma[code1].plot(color='y')
	#ss.plot(color='b')
	plt.show()

	
if __name__ == "__main__":
	global profit, hs300,roe, growth_mbrg, growth_nprg, growth_nav
	
	profit = getdata.GetProfit('net_profits')
	basic = getdata.GetBasic()['totals']
	roe = getdata.GetProfit('roe')
	growth_mbrg = getdata.GetGrowth('mbrg')
	growth_nprg = getdata.GetGrowth('nprg')
	
	#growth_nav = getdata.GetGrowth('nav')
	
	hs300 = getdata.GetHs300()
	zz500 = getdata.GetZz500()
	
	#retpearray = Series()
	#retpbarray = Series()
	#plotcorrelation()
	
	#plot use subplot
	#fig, axes = plt.subplots(1,1)
	#plotpe('000538', axes)
	#plt.show()
	#fig, axes = plt.subplots(2,2)
	
	excludecodelist = download.LoadCodelist('bankcode')
	#codelist = codelist[:-1]  ## skip 000883, since it's not in hs300
	#codelist = ['000001','600036']
	#codelist = ['000651', '601166']	
	#codelist = ['601668', '600887']	
	#codelist = download.LoadCodelist('constructioncode.txt')
	#codelist = download.LoadCodelist('realeastatecode')
	codelist = download.LoadCodelist()
	#codelist = ['600100']
	plt.rc('figure', figsize=(40, 40))
	font_options = {'size' : '18'}
	plt.rc('font', **font_options)
	cnt = 0
	for code in codelist:
		if code in excludecodelist:
			continue
	        fig, axes = plt.subplots(2, 2)
		if code in hs300.index:
			name = hs300['name'][code].decode('UTF-8')
		elif code in zz500.index:
			name = zz500['name'][code].decode('UTF-8')
		else:
		      print "name is not in list %s" % code
		      name = code
		plotpe(code, axes[0][0], name)
		plotpb(code, axes[0][1], name)
		
		plotprice(code, axes[1][0], name)
		plotprice(code, axes[1][1], name)
		#plotgrowth(code, axes[0][cnt])
		cnt = cnt + 1
		plt.savefig( "/var/www/html/img/%s.png" % code, format='png')
		

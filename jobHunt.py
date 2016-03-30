# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 13:23:45 2016

@author: Jordan

EXAMPLE USAGE:


"""

import requests
from bs4 import BeautifulSoup
import time
import re
import csv
from string import punctuation

class FundHunt:
    def __init__(self, tickers):
        cleantickers = list(set(tickers))
        self.tickers = sorted(cleantickers)
        self.baseURL = 'http://whalewisdom.com'
        self.holdingsURL = self.baseURL + 'holdings'

    def _getIDs(self):
        wwids = []
        a = re.compile(r'\d+')
        if (len(self.tickers) > 20):
            print("This might take a while...")
        print("Getting lookup IDs from 13F filings...")
        for i, item in enumerate(self.tickers):
            stockURL = "%s/stock/%s" % (self.baseURL, item)
            response = requests.get(stockURL).text
            soup = BeautifulSoup(response, "lxml")
            tableID = soup.find(attrs={
                "xmlns": "http://www.w3.org/1999/html"
                }).string
            tickerID = str(a.findall(tableID)[0])
            wwids.append(tickerID)
            time.sleep(0.25)
        print(wwids)
        return wwids

    def getInfo(self, holdingPercentages, statesList, minAUM):
        stockIDs = self._getIDs()
        fundInfo = []

        for i, item in enumerate(stockIDs):
            print("Getting holding info for: ", self.tickers[i])
            holdingsURL = "%s/stock/holdings" % (self.baseURL)
            p = {
                'id': item,
                'q1': '60',
                'change_filter': '1,2,3,4,5',
                '_search': 'false',
                'rows': '15',
                'page': '1',
                'sidx': 'current_percent_of_portfolio',
                'sord': 'desc'
                }
            response = requests.get(holdingsURL, params=p).json()
            for x, row in enumerate(response['rows']):
                if (isinstance(row['current_percent_of_portfolio'], float) and
                        len(response['rows']) > 0):
                    pass
                else:
                    print('''there was an error with the current percent of
                        portfolio row at index {:d}'''.format(x))
                    print("error with stock {:d}: ".format(i), self.tickers[i])
                    continue
                info = dict()
                added = False
                print(row['name'])
                if (int(row['current_percent_of_portfolio']) <= holdingPercentages[1] and
                        int(row['current_percent_of_portfolio']) >= holdingPercentages[0] and
                        row['state'] in statesList):
                    info['name'] = row['name']
                    info['state'] = row['state']
                    info['count'] = 1
                    info['cumulative'] = row['current_percent_of_portfolio']
                    info['companies'] = [self.tickers[i]]
                    if (len(fundInfo) == 0):
                        fundInfo.append(info)
                        added = True
                    else:
                        for z in fundInfo:
                            if (z['name'] == info['name']):
                                z['count'] += 1
                                z['cumulative'] += info['cumulative']
                                z['companies'].append(self.tickers[i])
                                added = True
                    if (added is not True):
                        fundInfo.append(info)
        return fundInfo

    def exportToCSV(self, data):
        with open('data.csv', 'w') as csvfile:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')

            writer.writeheader()
            for i, data in enumerate(data):
                writer.writerow(data)
# public companies from VCs I respect (Sutter Hill, Accel, Sequoia, A16Z, etc.)
tickerList = ['pstg']
''', 'infn', 'pacb-2', 'vbay', 'xlrn-2', 'ptla-2', 'rkus',
              'hznp', 'yoku', 'sq', 'run', 'pypl', 'hubs','jmei', 'nmbl',
              'cuda', 'rng', 'feye-2', 'trla', 'twtr', 'baba-4', 'hdp',
              'newr', 'zen', 'grub', 'wix', 'fnjn', 'mrin', 'amba-2',
              'pfpt', 'yelp', 'amzn', 'z', 'zip', 'ondk', 'bv', 'ntra', 'fb',
              'team', 'etsy', 'opwr', 'vrns-2', 'yume', 'rvbd', 'tsla',
              'modn', 'nflx', 'goog', 'msft', 'nvda', 'gddy', 'adbe', 'crm',
              'gimo', 'elnk', 'gib', 'dox', 'infy', 'acn', 'hckt',
              'caci', 'ctsh', 'mant', 'wit', 'tsri', 'elli', 'akam', 'vrnt',
              'ftnt', 'opwv', 'sncr', 'panw', 'vdsi', 'avgo', 'cvg', 'gpn',
              'gsb', 'jcom', 'jkhy', 'lrcx', 'ma', 'ntes', 'payx', 'tss',
              'txn', 'v', 'googl', 'anet', 'aten', 'fuel-3', 'ubnt', 'frf',
              'flt-2', 'bsft', 'lnkd', 'aapl', 'eqix', 'ebix', 'qlik',
              'athn', 'ebay', 'adbe']'''

# places wife and I are okay with living
statesList = ['CA', 'MA', 'CT', 'NY', 'IL', 'TX']

# % holding collar (min, max)
holdingPercentages = (1.5, 70)
minAUM = 400

x = FundHunt(tickerList)
y = x.getInfo(holdingPercentages, statesList, minAUM)
x.exportToCSV(y)
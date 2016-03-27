# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 13:23:45 2016

@author: Jordan
"""

import requests
from bs4 import BeautifulSoup
import time
import re


class getFirms:
    def __init__(self, tickers):
        self.tickers = tickers
        self.baseURL = 'http://whalewisdom.com/stock/'
        self.holdingsURL = self.baseURL + 'holdings'

    def _getIDs(self):
        wwids = []
        a = re.compile(r'\d+')

        for i, item in enumerate(self.tickers):
            response = requests.get(self.baseURL + self.tickers[i]).text
            soup = BeautifulSoup(response, "lxml")
            tableID = soup.find(attrs={
                "xmlns": "http://www.w3.org/1999/html"
                }).string
            tickerID = str(a.findall(tableID)[0])
            wwids.append(tickerID)
            time.sleep(0.5)

        return wwids

    def holdingFirms(self, percentHigh, percentLow, statesList):
        stockIDs = self._getIDs()
        holdingFirms = []

        for i, item in enumerate(stockIDs):
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
            response = requests.get(self.holdingsURL, params=p).json()
            time.sleep(0.5)

            for x, row in enumerate(response['rows']):
                info = dict()
                added = False
                if (row['current_percent_of_portfolio'] <= percentHigh and
                        row['current_percent_of_portfolio'] >= percentLow and
                        row['state'] in statesList):
                    info['name'] = row['name']
                    info['state'] = row['state']
                    info['count'] = 1
                    info['cumulative'] = row['current_percent_of_portfolio']
                    info['companies'] = [self.tickers[i]]
                    if (len(holdingFirms) == 0):
                        holdingFirms.append(info)
                        added = True
                    else:
                        for z in holdingFirms:
                            if (z['name'] == info['name']):
                                z['count'] += 1
                                z['cumulative'] += info['cumulative']
                                z['companies'].append(self.tickers[i])
                                added = True
                    if (added is not True):
                        holdingFirms.append(info)

        return holdingFirms


# public companies from VCs I respect (Sutter Hill, Accel, Sequoia, A16Z, etc.)
testList = ['googl', 'team', 'rng', 'nvda', 'vbay']
'''tickerList = ['pstg', 'infn', 'pacb-2', 'vbay', 'xlrn-2', 'ptla-2', 'rkus',
              'hznp', 'yoku', 'sq', 'run', 'pypl', 'ntra', 'hubs', 'ydle',
              'jmei', 'nmbl', 'cuda', 'rng', 'feye-2', 'trla', 'twtr', 'baba-4',
              'hdp', 'newr', 'zen', 'grub', 'wix', 'fnjn', 'mrin', 'amba-2',
              'pfpt', 'yelp', 'amzn', 'z', 'zip', 'ondk', 'bv', 'ntra', 'fb',
              'team', 'run', 'etsy', 'ydle', 'opwr', 'vrns-2', 'nmbl', 'yume',
              'modn', 'nflx', 'goog', 'msft', 'nvda', 'gddy', 'adbe', 'crm',
              'gimo', 'cksw', 'elnk', 'gib', 'dox', 'infy', 'acn', 'hckt',
              'caci', 'ctsh', 'mant', 'wit', 'tsri', 'elli', 'akam', 'vrnt',
              'ftnt', 'opwv', 'sncr', 'panw', 'vdsi', 'avgo', 'cvg', 'gpn',
              'gsb', 'jcom', 'jkhy', 'lrcx', 'ma', 'ntes', 'payx', 'tss',
              'txn', 'v', 'googl', 'anet', 'aten', 'fuel-3', 'ubnt', 'frf',
              'flt-2', 'bsft']'''

# places wife and I are okay with living
statesList = ['CA', 'MA', 'CT', 'NY', 'IL', 'TX']

# % holding collar
percentLow = 1.5
percentHigh = 70

x = getFirms(testList)
y = x.holdingFirms(percentHigh, percentLow, statesList)
print(y)
